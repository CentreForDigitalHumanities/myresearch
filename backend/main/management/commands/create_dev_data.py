from typing import Any, Type, Type
from django.conf import settings
from django.db import transaction
from django.db.models import Model
from django.core.management.base import BaseCommand, CommandError
from tqdm import tqdm
from faker import Faker

from form.models import (
    DateQuestion,
    FileUploadQuestion,
    Form,
    FormConfig,
    NumberQuestion,
    SelectOption,
    SelectQuestion,
    Step,
    StepInfo,
    StepInfoQuestion,
    StepInfoText,
    TextQuestion,
    TrueFalseQuestion,
)


NUMBER_OF_FORMS = 10
MIN_STEPS_PER_FORM = 3
MAX_STEPS_PER_FORM = 10
MIN_SUBSTEPS_PER_STEP = 0
MAX_SUBSTEPS_PER_STEP = 5
MIN_QUESTIONS_PER_STEP = 1
MAX_QUESTIONS_PER_STEP = 5

ALL_QUESTIONS = ["select", "text", "true_false", "date", "number", "file_upload"]


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

        with transaction.atomic():
            self._generate_form(options)
            self._generate_steps(options)
            self._generate_questions(options)

    def _generate_form(self, options) -> None:
        """
        Generate FormConfig and associated form.
        """

        form_config = FormConfig.objects.create(
            name="Mock Form Config",
            version="1.0",
        )

        Form.objects.create(
            name_nl=self.faker_nl.sentence(nb_words=5),
            name_en=self.faker_en.sentence(nb_words=5),
            description_nl=self.faker_nl.paragraph(),
            description_en=self.faker_en.paragraph(),
            config=form_config,
        )

    def _generate_steps(self, options) -> None:
        for form in tqdm(Form.objects.all(), desc="Generating steps..."):
            number_of_steps = self.faker.random_int(
                MIN_STEPS_PER_FORM, MAX_STEPS_PER_FORM
            )
            for step_index in range(number_of_steps):
                step = Step.objects.create(
                    form=form,
                    form_order=step_index,
                    slug=self.faker.slug(),
                    name_nl=self.faker_nl.sentence(nb_words=5),
                    name_en=self.faker_en.sentence(nb_words=5),
                    description_nl=self.faker_nl.paragraph(),
                    description_en=self.faker_en.paragraph(),
                )

                number_of_substeps = self.faker.random_int(
                    MIN_SUBSTEPS_PER_STEP, MAX_SUBSTEPS_PER_STEP
                )

                if self.faker.pybool():
                    # Generate step info.
                    self._create_step_info(step)

                for substep_index in range(number_of_substeps):
                    substep = Step.objects.create(
                        parent=step,
                        form_order=substep_index,
                        slug=self.faker.slug(),
                        name_nl=self.faker_nl.sentence(nb_words=5),
                        name_en=self.faker_en.sentence(nb_words=5),
                        description_nl=self.faker_nl.paragraph(),
                        description_en=self.faker_en.paragraph(),
                    )

                    if self.faker.pybool():
                        # Generate step info.
                        self._create_step_info(substep)

    def _create_step_info(self, step: Step) -> None:
        """Generates step information for a given step."""
        step_info = StepInfo.objects.create(step=step)

        def generate_step_info_text() -> None:
            """Generates 1-3 pieces of StepInfoText for a given step info."""
            for _ in range(self.faker.random_int(1, 3)):
                StepInfoText.objects.create(
                    step_info=step_info,
                    text_nl=self.faker_nl.paragraph(),
                    text_en=self.faker_en.paragraph(),
                )

        def generate_step_info_questions() -> None:
            """Generates 1-3 pieces of StepInfoQuestion for a given step info."""
            for _ in range(self.faker.random_int(1, 3)):
                StepInfoQuestion.objects.create(
                    step_info=step_info,
                    text_nl=self.faker_nl.sentence(),
                    text_en=self.faker_en.sentence(),
                    link=self.faker.url(),
                )

        choice = self.faker.random_element(["text", "questions", "both"])

        if choice == "text":
            generate_step_info_text()
        elif choice == "questions":
            generate_step_info_questions()
        else:
            generate_step_info_text()
            generate_step_info_questions()

    def _generate_questions(self, options) -> None:
        def _base_question_fields(step: Step) -> dict:
            return {
                "text_nl": self.faker_nl.sentence().replace(".", "?"),
                "text_en": self.faker_en.sentence().replace(".", "?"),
                "step": step,
                "description_nl": self.faker_nl.paragraph(),
                "description_en": self.faker_en.paragraph(),
                "required": self.faker.pybool(),
            }

        def _create_select_question(step: Step) -> None:
            select_question = SelectQuestion.objects.create(
                **_base_question_fields(step),
                multiple=self.faker.pybool(),
            )

            for _ in range(self.faker.random_int(2, 5)):
                SelectOption.objects.create(
                    label_nl=self.faker_nl.word(),
                    label_en=self.faker_en.word(),
                    question=select_question,
                )

        def _create_text_question(step: Step) -> None:
            TextQuestion.objects.create(
                **_base_question_fields(step),
                placeholder_nl=self.faker_nl.sentence(),
                placeholder_en=self.faker_en.sentence(),
            )

        def _create_true_false_question(step: Step) -> None:
            TrueFalseQuestion.objects.create(
                **_base_question_fields(step), default_value=self.faker.pybool()
            )

        def _create_date_question(step: Step) -> None:
            DateQuestion.objects.create(
                **_base_question_fields(step), future_only=self.faker.pybool()
            )

        def _create_number_question(step: Step) -> None:
            NumberQuestion.objects.create(
                **_base_question_fields(step), positive_only=self.faker.pybool()
            )

        def _create_file_upload_question(step: Step) -> None:
            FileUploadQuestion.objects.create(
                **_base_question_fields(step), size_limit=1024
            )

        for step in tqdm(Step.objects.all(), desc="Generating questions..."):
            number_of_questions = self.faker.random_int(
                MIN_QUESTIONS_PER_STEP, MAX_QUESTIONS_PER_STEP
            )
            for _question_index in range(number_of_questions):
                question_type = self.faker.random_element(ALL_QUESTIONS)

                match question_type:
                    case "select":
                        _create_select_question(step)
                    case "text":
                        _create_text_question(step)
                    case "true_false":
                        _create_true_false_question(step)
                    case "date":
                        _create_date_question(step)
                    case "number":
                        _create_number_question(step)
                    case "file_upload":
                        _create_file_upload_question(step)
