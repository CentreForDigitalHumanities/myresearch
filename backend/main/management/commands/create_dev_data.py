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
    MRForm,
    MRFormConfig,
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
            form = self._generate_form(options)
            self._generate_steps(options, form)
            self._generate_questions(options, form)

    def _generate_form(self, options) -> MRForm:
        """
        Generate FormConfig and associated Form.
        """

        print("Generating FormConfig and Form...")

        form_config = MRFormConfig.objects.create(
            name="Mock Form Config",
            version="1.0",
        )

        form = MRForm.objects.create(
            name_nl=self.faker_nl.sentence(nb_words=5),
            name_en=self.faker_en.sentence(nb_words=5),
            description_nl=self.faker_nl.paragraph(),
            description_en=self.faker_en.paragraph(),
            config=form_config,
        )

        print("Done!")

        return form

    def _generate_steps(self, options, form: MRForm) -> None:
        number_of_steps = self.faker.random_int(MIN_STEPS_PER_FORM, MAX_STEPS_PER_FORM)

        for step_index in tqdm(range(number_of_steps), desc="Generating steps..."):
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
                    parent_order=substep_index,
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

    def _generate_questions(self, options, form: MRForm) -> None:
        def _base_question_fields(step: Step, order: int) -> dict:
            return {
                "text_nl": self.faker_nl.sentence().replace(".", "?"),
                "text_en": self.faker_en.sentence().replace(".", "?"),
                "step": step,
                "step_order": order,
                "description_nl": self.faker_nl.paragraph(),
                "description_en": self.faker_en.paragraph(),
                "required": self.faker.pybool(),
            }

        def _create_select_question(step: Step, index: int) -> None:
            select_question = SelectQuestion.objects.create(
                **_base_question_fields(step, index),
                multiple=self.faker.pybool(),
            )

            for _ in range(self.faker.random_int(2, 5)):
                SelectOption.objects.create(
                    label_nl=self.faker_nl.word(),
                    label_en=self.faker_en.word(),
                    question=select_question,
                )

        def _create_text_question(step: Step, index: int) -> None:
            TextQuestion.objects.create(
                **_base_question_fields(step, index),
                placeholder_nl=self.faker_nl.sentence(),
                placeholder_en=self.faker_en.sentence(),
                lines=self.faker.random_int(1, 5),
            )

        def _create_true_false_question(step: Step, index: int) -> None:
            TrueFalseQuestion.objects.create(
                **_base_question_fields(step, index), default_value=self.faker.pybool()
            )

        def _create_date_question(step: Step, index: int) -> None:
            DateQuestion.objects.create(
                **_base_question_fields(step, index), future_only=self.faker.pybool()
            )

        def _create_number_question(step: Step, index: int) -> None:
            NumberQuestion.objects.create(
                **_base_question_fields(step, index), positive_only=self.faker.pybool()
            )

        def _create_file_upload_question(step: Step, index: int) -> None:
            FileUploadQuestion.objects.create(
                **_base_question_fields(step, index), size_limit=1024
            )

        # Only create questions for the form that was just created.
        form_steps = Step.objects.filter(form=form)

        for step in tqdm(form_steps, desc="Generating questions..."):
            number_of_questions = self.faker.random_int(
                MIN_QUESTIONS_PER_STEP, MAX_QUESTIONS_PER_STEP
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
