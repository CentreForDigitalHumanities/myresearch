from django.forms import ModelForm, CharField, ValidationError, Textarea

from form.models import Step


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

    class Meta:
        model = Step
        fields = []

    # Prepopulate question_order with current order if editing a step.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            current_order = self.instance.get_basequestion_order()
            if current_order:
                self.initial["question_order"] = ",".join(map(str, current_order))

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

        if commit:
            instance.save()
        return instance
