from tqdm import tqdm
from faker import Faker

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from django.db import transaction
from django.core.management import call_command

from form.models.questions import RepeatableStepQuestion
from form.services.form_evaluator import FormEvaluator
from research.models.reviews import StatusChange, SubmissionStatus
from research.models.study import Study
from main.models import User
from form.models import (
    BaseQuestion,
    MRForm,
    QuestionResponse,
    Step,
    StepInfoText,
    FileUploadQuestion,
    NumberQuestion,
    DateQuestion,
    RepeatIndex,
    SelectOption,
    SelectQuestion,
    TextQuestion,
    TrueFalseQuestion,
    UserFormSubmission,
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

# Min/max number of repeatable steps.
MIN_REPEATABLE_STEPS = 1
MAX_REPEATABLE_STEPS = 3

# Limits nested steps to avoid infinite recursion.
MAX_STEP_DEPTH = 3


ALL_QUESTIONS = [
    "select",
    "text",
    "true_false",
    "date",
    "number",
    "file_upload",
]

REPEATABLE_QUESTIONS = ["text"]

# These are the question annotation_keys that are used in the app.
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
                self._generate_repeatable_steps(options, form)
                self._generate_overview_step(options, form)
                self._generate_step_infos(options, form)
                self._generate_questions(options, form)

        self._create_submissions_and_studies(options, form)
        call_command("loaddata", "notes/fixtures/initial.json")

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
                    description_nl=f"<p>{self.faker_nl.paragraph()}</p>",
                    description_en=f"<p>{self.faker_en.paragraph()}</p>",
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
                description_nl=f"<p>{self.faker_nl.paragraph()}</p>",
                description_en=f"<p>{self.faker_en.paragraph()}</p>",
                slug=self.faker.unique.slug(),
            )
            _generate_substeps(step, 1)

    def _generate_repeatable_steps(self, options, form: MRForm) -> None:
        """
        Generate repeatable steps for the provided form.
        """
        num_repeatable_steps = self.faker.random_int(
            MIN_REPEATABLE_STEPS, MAX_REPEATABLE_STEPS
        )

        for _ in tqdm(
            range(num_repeatable_steps),
            desc="Generating repeatable steps...",
            disable=options["silent"],
        ):
            repeatable_step = Step.objects.create(
                form=form,
                name_nl=self.faker_nl.sentence(nb_words=5),
                name_en=self.faker_en.sentence(nb_words=5),
                description_nl=f"<p>{self.faker_nl.paragraph()}</p>",
                description_en=f"<p>{self.faker_en.paragraph()}</p>",
                slug=self.faker.unique.slug(),
                is_repeatable=True,
                # For now, we will only create repeatable steps at the top
                # level, but this could be extended to substeps in the future.
                parent=None,
            )
            # Every repeatable step needs a RepeatableStepQuestion (RSQ) to manage its instances.
            self._generate_rsq(repeatable_step)

    def _generate_overview_step(self, options, form: MRForm) -> None:
        """Generate an overview step for the form."""
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

    def _generate_rsq(self, repeatable_step: Step) -> None:
        """
        Generate a RepeatableStepQuestion (RSQ) for a repeatable step so instances of the step can be created or deleted.
        """
        host_step = Step.objects.exclude(id=repeatable_step.pk).first()

        assert host_step is not None, "No host step found to attach the RSQ to."

        RepeatableStepQuestion.objects.create(
            text=f"Manage instances of {repeatable_step.name}",
            text_en=f"Manage instances of {repeatable_step.name}",
            text_nl=f"Beheer stappen van {repeatable_step.name}",
            description=f"This question allows you to manage instances of the repeatable step {repeatable_step.name}.",
            description_en=f"This question allows you to manage instances of the repeatable step {repeatable_step.name}.",
            description_nl=f"Deze vraag stelt u in staat om instanties van de herhaalbare stap {repeatable_step.name} te beheren.",
            repeatable_step=repeatable_step,
            step=host_step,
            form=host_step.form,
            create_text="Create new instance",
            create_text_en="Create new instance",
            create_text_nl="Nieuwe stap toevoegen",
            none_yet_text="No instances yet",
            none_yet_text_en="No instances yet",
            none_yet_text_nl="Geen stappen toegevoegd",
        )

    def _generate_step_infos(self, options, form: MRForm) -> None:
        """
        Generate side information for each step in the form, in around 50% of cases.
        """

        def _generate_step_info_text(step: Step) -> None:
            """Generates side information for a given step."""

            if not self.faker.pybool():
                return

            for _ in range(self.faker.random_int(1, 3)):
                StepInfoText.objects.create(
                    step=step,
                    text_nl=self.faker_nl.sentence().replace(".", "?"),
                    text_en=self.faker_en.sentence().replace(".", "?"),
                    content_nl=f"<p>{self.faker_nl.paragraph()}</p>",
                    content_en=f"<p>{self.faker_en.paragraph()}</p>",
                )

        for step in tqdm(
            Step.objects.filter(form=form),
            desc="Generating step infos...",
            disable=options["silent"],
        ):
            _generate_step_info_text(step)

    def _generate_questions(self, options, form: MRForm) -> None:
        def _base_question_fields(step: Step, order: int) -> dict:
            return {
                "text_nl": self.faker_nl.sentence().replace(".", "?"),
                "text_en": self.faker_en.sentence().replace(".", "?"),
                "step": step,
                "description_nl": f"<p>{self.faker_nl.paragraph()}</p>",
                "description_en": f"<p>{self.faker_en.paragraph()}</p>",
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

        def _create_text_question(
            form: Step,
            index: int,
            is_repeatable=False,
        ) -> None:
            tq = TextQuestion.objects.create(
                **_base_question_fields(form, index),
                placeholder_nl=self.faker_nl.sentence(),
                placeholder_en=self.faker_en.sentence(),
                lines=self.faker.random_int(1, 5),
                is_repeatable=is_repeatable,
            )
            # For 10% of tq's make them override the step name
            if self.faker.boolean(10):
                try:
                    tq.step_name_override = True
                    tq.save()
                except ValidationError:
                    pass
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
            Step.objects.filter(form=form),
            desc="Generating questions...",
            disable=options["silent"],
        ):
            number_of_questions = self.faker.random_int(
                MIN_QUESTIONS_IN_STEP, MAX_QUESTIONS_IN_STEP
            )
            for question_index in range(number_of_questions):
                question_type = self.faker.random_element(ALL_QUESTIONS)

                # Make question repeatable in 10% of cases.
                repeatable = (
                    question_type in REPEATABLE_QUESTIONS and self.faker.pybool(10)
                )

                match question_type:
                    case "select":
                        _create_select_question(step, question_index)
                    case "text":
                        _create_text_question(step, question_index, repeatable)
                    case "true_false":
                        _create_true_false_question(step, question_index)
                    case "date":
                        _create_date_question(step, question_index)
                    case "number":
                        _create_number_question(step, question_index)
                    case "file_upload":
                        _create_file_upload_question(step, question_index)
                    case _:
                        raise ValueError(f"Unknown question type: {question_type}")

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

                # Create one UserFormSubmission per study (for now)

                # For 30% of studies, create a submitted StatusChange and a complete submission
                if self.faker.boolean(30):
                    # These will be filled in perfectly
                    self._create_user_form_submission(user, form, study, complete=True)
                    StatusChange.objects.create(
                        status=SubmissionStatus.SUBMITTED, created_by=user, study=study
                    )
                    if self.faker.boolean(50):
                        # mark some of these as seen
                        study.is_seen = True
                        study.save()
                else:
                    # Non submitted studies will not be filled in perfectly
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
        # Note: these do not correspond to actually uploaded files, so the
        # frontend will not be able to retrieve them.
        return {
            "value": f"{self.faker.uuid4()}",
            "name": self.faker.file_name(),
            "size": self.faker.random_int(min=1, max=question.size_limit),
        }

    def _generate_answer_for_question(self, question: BaseQuestion) -> dict:
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

    def _create_repeat_index(
        self,
        repeatable,
        submission: UserFormSubmission,
        parent: RepeatIndex | None = None,
    ) -> RepeatIndex:
        repeat_index = RepeatIndex.objects.create(parent=parent)
        repeat_index.submissions.add(submission)
        repeatable.repeat_indices.add(repeat_index)
        return repeat_index

    def _generate_repeat_indices_for_step(
        self,
        step: Step,
        submission: UserFormSubmission,
        parent: RepeatIndex | None = None,
    ) -> list[RepeatIndex | None]:
        """
        Generates repeat indices for a step in a submission. If the step is
        repeatable, it will generate 1-3 repeat indices for that step.

        For each generated repeat index, this function will recursively
        generate repeat indices for any substeps of the step.
        """
        repeat_indices: list[RepeatIndex | None] = []

        if not step.is_repeatable:
            repeat_indices = [parent]
        else:
            # For each step, generate 1-3 repeat indices (repeated instances).
            for _ in range(self.faker.random_int(1, 3)):
                repeat_index = self._create_repeat_index(
                    step,
                    submission,
                    parent,
                )
                repeat_indices.append(repeat_index)

        # For each repeated step, generate repeat indices for its substeps.
        for repeat_index in repeat_indices:
            for substep in Step.objects.filter(parent=step):
                self._generate_repeat_indices_for_step(
                    substep,
                    submission,
                    repeat_index,
                )

        return repeat_indices

    def _get_step_instance_indices(
        self,
        step: Step,
        submission: UserFormSubmission,
    ) -> list[RepeatIndex | None]:
        """
        Get the repeat indices for a step in a submission.
        """
        parent_indices: list[RepeatIndex | None] = [None]

        # If the step has a parent, get the repeat indices for the parent step.
        if step.parent is not None:
            parent_indices = self._get_step_instance_indices(
                step.parent,
                submission,
            )

        # If the step is not repeatable, we just return the parent indices.
        if not step.is_repeatable:
            return parent_indices

        # If the step is repeatable, get the repeat indices for the step itself.
        return [
            repeat_index
            for parent_index in parent_indices
            for repeat_index in step.repeat_indices_for_submission(
                submission,
                parent_index,
            )
        ]

    def _generate_repeat_indices_and_responses(
        self,
        submission: UserFormSubmission,
        form: MRForm,
        complete: bool,
    ) -> None:
        """
        Create repeat markers and indexed responses for one submission.
        """
        top_level_steps = Step.objects.filter(form=form, parent__isnull=True)
        for step in top_level_steps:
            self._generate_repeat_indices_for_step(step, submission)

        for step in Step.objects.filter(form=form):
            enclosing_indices = self._get_step_instance_indices(step, submission)

            for question in BaseQuestion.objects.filter(step=step):
                question = question.get_subclass()
                if isinstance(question, RepeatableStepQuestion):
                    continue

                if question.is_repeatable:
                    for parent_index in enclosing_indices:
                        for _ in range(self.faker.random_int(1, 3)):
                            repeat_index = self._create_repeat_index(
                                question,
                                submission,
                                parent_index,
                            )
                            if complete or self.faker.pybool(truth_probability=75):
                                response = QuestionResponse.objects.create(
                                    question=question,
                                    answer=self._generate_answer_for_question(question),
                                    repeat_index=repeat_index,
                                )
                                response.submissions.add(submission)
                    continue

                for repeat_index in enclosing_indices:
                    if not complete and self.faker.pybool(truth_probability=25):
                        continue
                    response = QuestionResponse.objects.create(
                        question=question,
                        answer=self._generate_answer_for_question(question),
                        repeat_index=repeat_index,
                    )
                    response.submissions.add(submission)

    def _create_user_form_submission(
        self,
        user: User,
        form: MRForm,
        study: Study,
        complete: bool = False,
    ) -> None:
        submission = UserFormSubmission.objects.create(
            user=user,
            form=form,
            study=study,
        )

        self._generate_repeat_indices_and_responses(submission, form, complete)

        form_questions = form.questions.all()  # type: ignore

        # Evaluate the submission
        evaluator = FormEvaluator(submission)

        # Remove responses for questions that are not visible based on the generated answers.
        for question in form_questions:
            if not evaluator.is_question_visible(question):
                QuestionResponse.objects.filter(
                    submissions__in=[submission],
                    question=question,
                ).delete()
