from typing import TypeAlias

from tqdm import tqdm
from faker import Faker
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.core.management import call_command

from form.services.form_evaluator import FormEvaluator
from research.models.reviews import StatusChange, SubmissionStatus
from research.models.study import Study
from main.models import User
from form.models import (
    MRForm,
    QuestionResponse,
    Step,
    StepInfoText,
    FileUploadQuestion,
    NumberQuestion,
    DateQuestion,
    SelectOption,
    SelectQuestion,
    TextQuestion,
    TrueFalseQuestion,
    UserFormSubmission,
)

AnyQuestion: TypeAlias = (
    SelectQuestion
    | TrueFalseQuestion
    | TextQuestion
    | NumberQuestion
    | DateQuestion
    | FileUploadQuestion
)


# Min/max number of steps for the (top-level) form.
MIN_STEPS_IN_ROOT_FORM = 3
MAX_STEPS_IN_ROOT_FORM = 5

# Min/max number of substeps in a step.
MIN_SUBSTEPS_IN_STEP = 0
MAX_SUBSTEPS_IN_STEP = 5

# Min/max number of questions per step.
MIN_QUESTIONS_IN_STEP = 1
MAX_QUESTIONS_IN_STEP = 5

# Limits nested steps to avoid infinite recursion.
MAX_STEP_DEPTH = 3


ALL_QUESTIONS = ["select", "text", "true_false", "date", "number", "file_upload"]

# These are the question annotation_keys that are used in the app
TEXT_ANNOTATION_KEYS = ["title"]
SELECT_ANNOTATION_KEYS = ["faculty"]

# Min/max number of studies per user
MIN_STUDIES_PER_USER = 1
MAX_STUDIES_PER_USER = 4


class Command(BaseCommand):
    help = "Create dev dataset for myresearch"

    faker = Faker(["en_GB", "nl_NL"])
    faker_nl = faker["nl_NL"]
    faker_en = faker["en_GB"]

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force execution even if DEBUG = False in settings.py",
        )
        parser.add_argument(
            "--silent",
            action="store_true",
            help="Suppress output during data generation.",
        )
        parser.add_argument(
            "--vwr",
            action="store_true",
            help="Use the VWR fixture for the form instead of generating a random one.",
        )

    def print(self, options, *args, **kwargs):
        if not options["silent"]:
            print(*args, **kwargs)

    def handle(self, *args, **options):
        if not settings.DEBUG and not options["force"]:
            raise CommandError(
                "Refusing to execute command unless DEBUG = True in settings.py"
            )

        # As we loop over users for generating certain objects, we'll need
        # to ensure we have some users.
        call_command("load_fixtures", "--users-only", "--force")

        with transaction.atomic():
            if options["vwr"]:
                self.print(options, "Loading VWR fixture for form...")
                call_command("loaddata", "form/fixtures/vwr.json")
                form = MRForm.objects.get(name_en="Processing Registry")
            else:
                self.print(options, "Generating random form and associated data...")
                form = self._generate_form(options)
                self._generate_steps(options, form)
                self._generate_questions(options, form)

        self._create_submissions_and_studies(options, form)

        self.print(options, "Dev data generation complete!")

    def _generate_form(self, options) -> MRForm:
        """
        Generate a root MRForm with top-level steps.
        """

        self.print(options, "Generating root form with top-level steps...")

        form = MRForm.objects.create(
            name_nl=self.faker_nl.sentence(nb_words=5),
            name_en=self.faker_en.sentence(nb_words=5),
        )

        self.print(options, "Done!")

        return form

    def _generate_steps(self, options, form: MRForm) -> None:
        """
        Generate steps and substeps, up to a certain depth.
        """

        def _generate_substeps(step: Step, depth: int) -> None:
            """
            Generate substeps recursively for a given step, up to a certain depth.
            """

            if depth >= MAX_STEP_DEPTH:
                return

            num_substeps = self.faker.random_int(
                MIN_SUBSTEPS_IN_STEP, MAX_SUBSTEPS_IN_STEP
            )

            for _ in tqdm(
                range(num_substeps),
                desc=f"Generating substeps for step {step.name[:10]} (depth: {depth})",
                disable=options["silent"],
            ):
                substep = Step.objects.create(
                    parent=step,
                    form=step.form,
                    name_nl=self.faker_nl.sentence(nb_words=5),
                    name_en=self.faker_en.sentence(nb_words=5),
                    description_nl=self.faker_nl.paragraph(),
                    description_en=self.faker_en.paragraph(),
                    slug=self.faker.unique.slug(),
                )

                _generate_substeps(substep, depth + 1)

        # Generate top-level steps for the form.
        num_steps = self.faker.random_int(
            MIN_STEPS_IN_ROOT_FORM, MAX_STEPS_IN_ROOT_FORM
        )

        for _ in tqdm(
            range(num_steps),
            desc="Generating top-level steps...",
            disable=options["silent"],
        ):
            step = Step.objects.create(
                form=form,
                name_nl=self.faker_nl.sentence(nb_words=5),
                name_en=self.faker_en.sentence(nb_words=5),
                description_nl=self.faker_nl.paragraph(),
                description_en=self.faker_en.paragraph(),
                slug=self.faker.unique.slug(),
            )
            _generate_substeps(step, 1)

        # Add an overview substep (in about 80% of cases)
        if self.faker.pybool(truth_probability=80):
            Step.objects.create(
                form=form,
                name_nl="Overzicht",
                name_en="Overview",
                description_nl=self.faker_nl.paragraph(),
                description_en=self.faker_en.paragraph(),
                slug=f"overview-{self.faker.unique.slug()}",
                is_overview=True,
            )

    def _create_step_info(self, step: Step) -> None:
        """Generates side information for a given step."""

        if not self.faker.pybool():
            return

        for _ in range(self.faker.random_int(1, 3)):
            StepInfoText.objects.create(
                step=step,
                text_nl=self.faker_nl.paragraph(),
                text_en=self.faker_en.paragraph(),
            )

    def _generate_questions(self, options, form: MRForm) -> None:
        def _base_question_fields(step: Step, order: int) -> dict:
            return {
                "text_nl": self.faker_nl.sentence().replace(".", "?"),
                "text_en": self.faker_en.sentence().replace(".", "?"),
                "step": step,
                "description_nl": self.faker_nl.paragraph(),
                "description_en": self.faker_en.paragraph(),
                "required": self.faker.pybool(),
            }

        def _create_select_question(form: Step, index: int) -> None:
            select_question = SelectQuestion.objects.create(
                **_base_question_fields(form, index),
                multiple=self.faker.pybool(),
            )

            if SELECT_ANNOTATION_KEYS:
                select_question.annotation_key = SELECT_ANNOTATION_KEYS.pop()
                select_question.save()

            for _ in range(self.faker.random_int(2, 5)):
                SelectOption.objects.create(
                    label_nl=self.faker_nl.word(),
                    label_en=self.faker_en.word(),
                    question=select_question,
                )

        def _create_text_question(form: Step, index: int) -> None:
            tq = TextQuestion.objects.create(
                **_base_question_fields(form, index),
                placeholder_nl=self.faker_nl.sentence(),
                placeholder_en=self.faker_en.sentence(),
                lines=self.faker.random_int(1, 5),
            )
            if TEXT_ANNOTATION_KEYS:
                tq.annotation_key = TEXT_ANNOTATION_KEYS.pop()
                tq.save()

        def _create_true_false_question(form: Step, index: int) -> None:
            TrueFalseQuestion.objects.create(
                **_base_question_fields(form, index), default_value=self.faker.pybool()
            )

        def _create_date_question(form: Step, index: int) -> None:
            DateQuestion.objects.create(
                **_base_question_fields(form, index), future_only=self.faker.pybool()
            )

        def _create_number_question(form: Step, index: int) -> None:
            NumberQuestion.objects.create(
                **_base_question_fields(form, index), positive_only=self.faker.pybool()
            )

        def _create_file_upload_question(form: Step, index: int) -> None:
            FileUploadQuestion.objects.create(
                **_base_question_fields(form, index), size_limit=1024
            )

        for step in tqdm(
            form.steps.all(), desc="Generating questions...", disable=options["silent"]
        ):
            number_of_questions = self.faker.random_int(
                MIN_QUESTIONS_IN_STEP, MAX_QUESTIONS_IN_STEP
            )
            for question_index in range(number_of_questions):
                question_type = self.faker.random_element(ALL_QUESTIONS)

                match question_type:
                    case "select":
                        _create_select_question(step, question_index)
                    case "text":
                        _create_text_question(step, question_index)
                    case "true_false":
                        _create_true_false_question(step, question_index)
                    case "date":
                        _create_date_question(step, question_index)
                    case "number":
                        _create_number_question(step, question_index)
                    case "file_upload":
                        _create_file_upload_question(step, question_index)

    def _create_submissions_and_studies(self, options, form):
        """
        Mock UserFormSubmissions and create studies for each user.

        For now, we only create one submission per study.
        """

        for user in tqdm(
            User.objects.all(),
            "Generating studies and submissions...",
            disable=options["silent"],
        ):
            num_studies = self.faker.random_int(
                MIN_STUDIES_PER_USER, MAX_STUDIES_PER_USER
            )

            for _ in range(num_studies):
                study = Study.objects.create(
                    created_by=user,
                )

                # Create a StatusChange
                StatusChange.objects.create(
                    status=SubmissionStatus.DRAFT, created_by=user, study=study
                )
                # Create one submission per study (for now).
                self._create_user_form_submission(user, form, study)

    def _generate_text_answer(self, question: TextQuestion) -> dict:
        return {"value": self.faker.sentence()}

    def _generate_number_answer(self, question: NumberQuestion) -> dict:
        min = 1 if question.positive_only else -100
        return {"value": self.faker.random_int(min=min, max=100)}

    def _generate_select_answer(self, question: SelectQuestion) -> dict:
        options = list(SelectOption.objects.filter(question=question))
        if not options:
            return {"value": []}
        max_selected = len(options) if question.multiple else 1
        num_selected = self.faker.random_int(min=0, max=max_selected)
        selected_options = self.faker.random_elements(
            elements=options, length=num_selected, unique=True
        )
        return {"value": [option.pk for option in selected_options]}

    def _generate_true_false_answer(self, question: TrueFalseQuestion) -> dict:
        return {"value": self.faker.pybool()}

    def _generate_date_answer(self, question: DateQuestion) -> dict:
        start_date = "today" if question.future_only else "-5y"
        end_date = "+5y" if question.future_only else "today"
        return {
            "value": self.faker.date_between(
                start_date=start_date, end_date=end_date
            ).isoformat()
        }

    def _generate_file_upload_answer(self, question: FileUploadQuestion) -> dict:
        filename = f"{self.faker.word()}_{self.faker.word()}.pdf"
        file_url = f"/uploads/{self.faker.uuid4()}/{filename}"
        return {"value": file_url}

    def _generate_answer_for_question(self, question: AnyQuestion) -> dict:
        if isinstance(question, TextQuestion):
            return self._generate_text_answer(question)
        if isinstance(question, SelectQuestion):
            return self._generate_select_answer(question)
        if isinstance(question, TrueFalseQuestion):
            return self._generate_true_false_answer(question)
        if isinstance(question, DateQuestion):
            return self._generate_date_answer(question)
        if isinstance(question, NumberQuestion):
            return self._generate_number_answer(question)
        if isinstance(question, FileUploadQuestion):
            return self._generate_file_upload_answer(question)

        raise ValueError(f"Unsupported question type: {type(question)}")

    def _create_user_form_submission(
        self, user: User, form: MRForm, study: Study
    ) -> None:
        submission = UserFormSubmission.objects.create(
            user=user,
            form=form,
            study=study,
        )

        form_questions = form.questions.all()

        # First generate answers for all questions, regardless of visibility.
        for question in form_questions:
            question = question.get_subclass()
            if self.faker.random_element([True, False, False, False]):
                # 25% chance to leave the question unanswered.
                continue

            answer_data = self._generate_answer_for_question(question)

            response = QuestionResponse.objects.create(
                question=question,
                answer=answer_data,
            )
            response.submissions.add(submission)

        # Evaluate the submission
        evaluator = FormEvaluator(submission)

        # Remove responses for questions that are not visible based on the generated answers.
        for question in form_questions:
            if not evaluator.is_question_visible(question):
                QuestionResponse.objects.filter(
                    submissions__in=[submission],
                    question=question,
                ).delete()
