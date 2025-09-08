from tqdm import tqdm
from faker import Faker

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from form.models import (
    DateQuestion,
    FileUploadQuestion,
    FormInfoText,
    MRForm,
    NumberQuestion,
    SelectOption,
    SelectQuestion,
    FormInfoQuestion,
    TextQuestion,
    TrueFalseQuestion,
)

# Min/max number of subforms for the top-level form.
MIN_FORMS_IN_ROOT_FORM = 3
MAX_FORMS_IN_ROOT_FORM = 5

# Min/max number of subforms in a subform.
MIN_FORMS_IN_SUBFORM = 0
MAX_FORMS_IN_SUBFORM = 5

# Min/max number of questions per form.
MIN_QUESTIONS_IN_FORM = 1
MAX_QUESTIONS_IN_FORM = 5

# Limits nested subforms to avoid infinite recursion.
MAX_SUBFORM_DEPTH = 3


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
            form = self._generate_root_form(options)
            self._generate_forms(options, form, 0)
            self._generate_questions(options, form)

    def _generate_root_form(self, options) -> MRForm:
        """
        Generate a root/top-level MRForm.
        """

        print("Generating root/top-level form...")

        form = MRForm.objects.create(
            name_nl=self.faker_nl.sentence(nb_words=5),
            name_en=self.faker_en.sentence(nb_words=5),
            description_nl=self.faker_nl.paragraph(),
            description_en=self.faker_en.paragraph(),
            slug=self.faker.unique.slug(),
            version="1.0",
        )

        print("Done!")

        return form

    def _generate_forms(self, options, form: MRForm, depth: int) -> None:
        """
        Generate a root form and its subforms recursively, up to a certain depth.
        """
        if depth >= MAX_SUBFORM_DEPTH:
            return

        if depth == 0:
            num_subforms = self.faker.random_int(
                MIN_FORMS_IN_ROOT_FORM, MAX_FORMS_IN_ROOT_FORM
            )
        else:
            num_subforms = self.faker.random_int(
                MIN_FORMS_IN_SUBFORM, MAX_FORMS_IN_SUBFORM
            )

        for _ in tqdm(
            range(num_subforms),
            desc=f"Generating subforms for form {form.name[:10]} (depth: {depth})",
        ):
            subform = MRForm.objects.create(
                parent=form,
                name_nl=self.faker_nl.sentence(nb_words=5),
                name_en=self.faker_en.sentence(nb_words=5),
                description_nl=self.faker_nl.paragraph(),
                description_en=self.faker_en.paragraph(),
                slug=self.faker.unique.slug(),
                version=form.version,
            )

            forms_in_subform = self.faker.random_int(
                MIN_FORMS_IN_SUBFORM, MAX_FORMS_IN_SUBFORM
            )

            if self.faker.pybool():
                # Generate step info.
                self._create_form_info(subform)

            self._generate_forms(options, subform, depth + 1)

    def _create_form_info(self, form: MRForm) -> None:
        """Generates form information for a given form."""

        def generate_form_info_text() -> None:
            """Generates 1-3 pieces of FormInfoText for a given form."""
            for _ in range(self.faker.random_int(1, 3)):
                FormInfoText.objects.create(
                    form=form,
                    text_nl=self.faker_nl.paragraph(),
                    text_en=self.faker_en.paragraph(),
                )

        def generate_form_info_questions() -> None:
            """Generates 1-3 pieces of FormInfoQuestion for a given form."""
            for _ in range(self.faker.random_int(1, 3)):
                FormInfoQuestion.objects.create(
                    form=form,
                    text_nl=self.faker_nl.sentence(),
                    text_en=self.faker_en.sentence(),
                    link=self.faker.url(),
                )

        choice = self.faker.random_element(["text", "questions", "both"])

        if choice == "text":
            generate_form_info_text()
        elif choice == "questions":
            generate_form_info_questions()
        else:
            generate_form_info_text()
            generate_form_info_questions()

    def _generate_questions(self, options, form: MRForm) -> None:
        def _base_question_fields(form: MRForm, order: int) -> dict:
            return {
                "text_nl": self.faker_nl.sentence().replace(".", "?"),
                "text_en": self.faker_en.sentence().replace(".", "?"),
                "form": form,
                "description_nl": self.faker_nl.paragraph(),
                "description_en": self.faker_en.paragraph(),
                "required": self.faker.pybool(),
            }

        def _create_select_question(form: MRForm, index: int) -> None:
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

        def _create_text_question(form: MRForm, index: int) -> None:
            TextQuestion.objects.create(
                **_base_question_fields(form, index),
                placeholder_nl=self.faker_nl.sentence(),
                placeholder_en=self.faker_en.sentence(),
                lines=self.faker.random_int(1, 5),
            )

        def _create_true_false_question(form: MRForm, index: int) -> None:
            TrueFalseQuestion.objects.create(
                **_base_question_fields(form, index), default_value=self.faker.pybool()
            )

        def _create_date_question(form: MRForm, index: int) -> None:
            DateQuestion.objects.create(
                **_base_question_fields(form, index), future_only=self.faker.pybool()
            )

        def _create_number_question(form: MRForm, index: int) -> None:
            NumberQuestion.objects.create(
                **_base_question_fields(form, index), positive_only=self.faker.pybool()
            )

        def _create_file_upload_question(form: MRForm, index: int) -> None:
            FileUploadQuestion.objects.create(
                **_base_question_fields(form, index), size_limit=1024
            )

        def _get_all_subforms(current_form: MRForm) -> list[MRForm]:
            """Recursively gather all subforms of a given form."""
            all_subforms: list[MRForm] = []
            subforms = MRForm.objects.filter(parent=current_form)
            for subform in subforms:
                all_subforms.append(subform)
                all_subforms.extend(_get_all_subforms(subform))
            return all_subforms

        all_forms = _get_all_subforms(form)

        for step in tqdm(all_forms, desc="Generating questions..."):
            number_of_questions = self.faker.random_int(
                MIN_QUESTIONS_IN_FORM, MAX_QUESTIONS_IN_FORM
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

    # def _check_all_models_implemented(
    #     self,
    # ):
    #     """
    #     Gather all models from LOCAL_APPS and check if they are all present in
    #     dev_data_models.
    #     """

    #     all_mr_models = []

    #     for app in settings.LOCAL_APPS:
    #         for mr_model in apps.get_app_config(app).get_models():
    #             all_mr_models.append(mr_model)

    #     for mr_model in all_mr_models:
    #         if mr_model not in self.dev_data_models:
    #             raise CommandError(
    #                 f"The model {mr_model} is not yet represented in the dev "
    #                 "data creation."
    #             )
