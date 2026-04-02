from django.forms import ModelForm, CharField, ValidationError, Textarea
from form.models import Step

class SelectQuestionAdminForm(ModelForm):
    select_options_order = CharField(
        max_length=255,
        help_text="Comma-separated list of question IDs in desired order, e.g. '3,1,2'.",
        label="Select Option order",
        required=False,
        widget=Textarea(attrs={"cols": "75", "rows": "1"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            current_order = self.instance.get_selectoption_order()
            if current_order:
                self.initial["select_options_order"] = ",".join(map(str, current_order))

    def clean_select_options_order(self):
        """
        Make sure that the provided question IDs are valid and exist.
        """
        order: str = self.cleaned_data.get("select_options_order", "")
        if not order:
            return order

        # Get the requested order of question IDs as a list of integers.
        requested_order = []
        for id_str in order.split(","):
            id_str = id_str.strip()
            if not id_str:
                continue
            if not id_str.isdigit():
                raise ValidationError(
                    f"Invalid question ID format: '{id_str}'. Must be numeric."
                )
            requested_order.append(int(id_str))

        # Validate that the provided IDs exist.
        available_ids = [question.id for question in self.instance.select_options.all()]
        #in instance.NAME.all(), NAME is the verbose name
        invalid_ids = [
            question_id
            for question_id in requested_order
            if question_id not in available_ids
        ]

        if invalid_ids:
            raise ValidationError(
                f"Invalid IDs: {', '.join(map(str, invalid_ids))}. "
                f"Available IDs: {', '.join(map(str, available_ids))}"
            )

        # Make sure that all available IDs are included.
        missing_ids = set(available_ids) - set(requested_order)

        if missing_ids:
            raise ValidationError(
                f"Missing IDs: {', '.join(map(str, missing_ids))}. "
                f"Available IDs: {', '.join(map(str, available_ids))}"
            )
        return order

    def save(self, commit=True):
        instance = super().save(commit=False)
        order = self.cleaned_data.get("select_options_order", "")

        if order:
            requested_order = [
                int(id_str)
                for id_str in order.split(",")
                if id_str.strip().isdigit()
            ]
            instance.set_selectoption_order(requested_order)
        if commit:
            instance.save()
        return instance

class StepAdminForm(ModelForm):
    """
    Custom form for Steps in the Django Admin interface. Adds a field 'question
    order' to the form, which allows a user to set the order of questions
    within a step.
    """

    question_order = CharField(
        max_length=255,
        help_text="Comma-separated list of question IDs in desired order, e.g. '3,1,2'.",
        label="Question order",
        required=False,
        widget=Textarea(attrs={"cols": "75", "rows": "1"}),
    )

    substep_order = CharField(
        max_length=255,
        help_text="Comma-separated list of substep IDs in desired order, e.g. '3,1,2'.",
        label="Substep order",
        required=False,
        widget=Textarea(attrs={"cols": "75", "rows": "1"}),
    )

    class Meta:
        model = Step
        fields = []

    # Prepopulate question_order and substep_order with current order if editing a step.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            current_order = self.instance.get_basequestion_order()
            if current_order:
                self.initial["question_order"] = ",".join(map(str, current_order))

            current_substep_order = self.instance.get_step_order()
            if current_substep_order:
                self.initial["substep_order"] = ",".join(
                    map(str, current_substep_order)
                )

    def clean_question_order(self):
        """
        Make sure that the provided question IDs are valid and exist.
        """
        question_order: str = self.cleaned_data.get("question_order", "")
        if not question_order:
            return question_order

        # Get the requested order of question IDs as a list of integers.
        requested_order = []
        for id_str in question_order.split(","):
            id_str = id_str.strip()
            if not id_str:
                continue
            if not id_str.isdigit():
                raise ValidationError(
                    f"Invalid question ID format: '{id_str}'. Must be numeric."
                )
            requested_order.append(int(id_str))

        # Validate that the provided IDs exist.
        available_ids = [question.id for question in self.instance.questions.all()]
        invalid_ids = [
            question_id
            for question_id in requested_order
            if question_id not in available_ids
        ]

        if invalid_ids:
            raise ValidationError(
                f"Invalid question IDs: {', '.join(map(str, invalid_ids))}. "
                f"Available IDs: {', '.join(map(str, available_ids))}"
            )

        # Make sure that all available IDs are included.
        missing_ids = set(available_ids) - set(requested_order)

        if missing_ids:
            raise ValidationError(
                f"Missing IDs: {', '.join(map(str, missing_ids))}. "
                f"Available IDs: {', '.join(map(str, available_ids))}"
            )
        return question_order

    def clean_substep_order(self):
        """
        Make sure that the provided substep IDs are valid and exist.
        """
        substep_order: str = self.cleaned_data.get("substep_order", "")
        if not substep_order:
            return substep_order

        # Get the requested order of substep IDs as a list of integers.
        requested_order = []
        for id_str in substep_order.split(","):
            id_str = id_str.strip()
            if not id_str:
                continue
            if not id_str.isdigit():
                raise ValidationError(
                    f"Invalid substep ID format: '{id_str}'. Must be numeric."
                )
            requested_order.append(int(id_str))

        # Validate that the provided IDs exist.
        available_ids = [substep.id for substep in self.instance.substeps.all()]
        invalid_ids = [
            substep_id
            for substep_id in requested_order
            if substep_id not in available_ids
        ]

        if invalid_ids:
            raise ValidationError(
                f"Invalid substep IDs: {', '.join(map(str, invalid_ids))}. "
                f"Available IDs: {', '.join(map(str, available_ids))}"
            )

        # Make sure that all available IDs are included.
        missing_ids = set(available_ids) - set(requested_order)

        if missing_ids:
            raise ValidationError(
                f"Missing IDs: {', '.join(map(str, missing_ids))}. "
                f"Available IDs: {', '.join(map(str, available_ids))}"
            )
        return substep_order

    def save(self, commit=True):
        instance = super().save(commit=False)
        question_order = self.cleaned_data.get("question_order", "")

        if question_order:
            requested_order = [
                int(id_str)
                for id_str in question_order.split(",")
                if id_str.strip().isdigit()
            ]
            instance.set_basequestion_order(requested_order)

        substep_order = self.cleaned_data.get("substep_order", "")

        if substep_order:
            requested_substep_order = [
                int(id_str)
                for id_str in substep_order.split(",")
                if id_str.strip().isdigit()
            ]
            instance.set_step_order(requested_substep_order)

        if commit:
            instance.save()
        return instance
