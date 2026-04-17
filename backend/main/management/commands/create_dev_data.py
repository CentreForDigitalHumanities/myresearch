from tqdm import tqdm
from faker import Faker

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.core.management import call_command

from research.other_models.reviews import StatusChange, SubmissionStatus
from main.models import User
from research.models import Study
from form.models import (
    MRForm,
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

# Min/max number of studies per user
MIN_STUDIES_PER_USER = 1
MAX_STUDIES_PER_USER = 4


class Command(BaseCommand):
    help = "Create dev dataset for myresearch"

    faker = Faker(["en_GB", "nl_NL"])
    faker_nl = faker["nl_NL"]
    faker_en = faker["en_GB"]

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true")
        parser.add_argument("--silent", action="store_true")

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
            form = self._generate_form(options)
            self._create_submissions_and_studies(options, form)
            self._generate_steps(options, form)
            self._generate_questions(options, form)

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
                    form=None,
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

    def _create_step_info(self, step: Step) -> None:
        """Generates side information for a given step."""

        def generate_form_info_text() -> None:
            for _ in range(self.faker.random_int(1, 3)):
                StepInfoText.objects.create(
                    step=step,
                    text_nl=self.faker_nl.paragraph(),
                    text_en=self.faker_en.paragraph(),
                )

        if self.faker.pybool():
            generate_form_info_text()

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

            for _ in range(self.faker.random_int(2, 5)):
                SelectOption.objects.create(
                    label_nl=self.faker_nl.word(),
                    label_en=self.faker_en.word(),
                    question=select_question,
                )

        def _create_text_question(form: Step, index: int) -> None:
            TextQuestion.objects.create(
                **_base_question_fields(form, index),
                placeholder_nl=self.faker_nl.sentence(),
                placeholder_en=self.faker_en.sentence(),
                lines=self.faker.random_int(1, 5),
            )

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

        def _get_all_steps(form: MRForm) -> list[Step]:
            """Recursively gather all steps and substeps of a given form."""

            def _get_all_substeps(step: Step) -> list[Step]:
                """Recursively gather all substeps of a given step."""
                all_substeps: list[Step] = []
                substeps = Step.objects.filter(parent=step)
                for substep in substeps:
                    all_substeps.append(substep)
                    all_substeps.extend(_get_all_substeps(substep))
                return all_substeps

            all_steps: list[Step] = []

            steps = Step.objects.filter(form=form)
            for step in steps:
                all_steps.append(step)
                all_steps.extend(_get_all_substeps(step))

            return all_steps

        all_steps = _get_all_steps(form)

        for step in tqdm(
            all_steps, desc="Generating questions...", disable=options["silent"]
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
        Create mock studies for each user
        """

        for user in tqdm(
            User.objects.all(), "Generating studies ...", disable=options["silent"]
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

                UserFormSubmission.objects.create(
                    user=user,
                    form=form,
                    study=study,
                )
