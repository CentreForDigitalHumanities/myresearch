import json
from django.core.management.base import BaseCommand
from django.core.management import call_command

EXCLUDED_MODELS = [
    "form.QuestionResponse",
    "form.UserFormSubmission",
    "form.MRDocument",
    "form.RepeatIndex",
]

EXCLUDED_FIELDS = {
    "form.basequestion": [
        "repeat_indices",
    ],
    "form.step": [
        "repeat_indices",
    ],
}


class Command(BaseCommand):
    """
    This custom fixture dump command is needed to correctly preserve the _order
    attribute of certain models. By default, Django's dumpdata will dump models
    sorted by model primarily and then sorted by pk. When we then load this data,
    models get loaded in this order, and this will override the explicit _order
    attribute that we use to order certain models.

    With this command, we ensure that our fixture gets dumped in the order of the
    _order attribute for the models where this is relevant.

    This is done by running dumpdata, loading the json and
    reordering it with custom logic and then writing that to the json file.
    It writes to our vwr.json fixture by default, but you can specify the
    output path with the --output argument for testing.
    """

    help = "Dump form app data, excluding specified models, sorted by _order field"

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            type=str,
            default="form/fixtures/vwr.json",
            help="Output file path",
        )

    def handle(self, *args, **options):
        output_path = options["output"]

        # Call dumpdata for the form app
        try:
            exclude_args = []
            for model in EXCLUDED_MODELS:
                exclude_args.extend(["--exclude", model])

            # First create a default dump
            call_command(
                "dumpdata",
                "form",
                *exclude_args,
                output=output_path,
                indent=4,
            )

            # Post-process to sort by _order field
            self.stdout.write("Sorting by _order attribute...")
            with open(output_path, "r") as f:
                dumped_data = json.load(f)

            # Group objects by model in a dictionary
            models_by_name = {}
            for item in dumped_data:
                model = item.get("model")
                if model not in models_by_name:
                    models_by_name[model] = []
                models_by_name[model].append(item)

            models_by_name = exclude_fields(models_by_name)
            models_by_name = sort_by_order(models_by_name)

            # Flatten back to list, maintaining model order
            sorted_data = []
            for model in sorted(models_by_name.keys()):
                sorted_data.extend(models_by_name[model])

            # Write to final output
            with open(output_path, "w") as f:
                json.dump(sorted_data, f, indent=4)

            self.stdout.write(
                self.style.SUCCESS(f"Successfully dumped fixture to {output_path}")
            )
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error dumping data: {str(e)}"))


def exclude_fields(models_by_name):
    """
    Remove certain fields from a model. Modifies the
    dict in place.
    """
    for model in models_by_name:
        if not model in EXCLUDED_FIELDS:
            continue
        objects = models_by_name[model]
        excluded = EXCLUDED_FIELDS[model]
        for obj in objects:
            for exclusion in excluded:
                obj["fields"].pop(exclusion, None)

    return models_by_name


def sort_by_order(models_by_name):

    # Define sorting keys for specific models
    # models are sorted based on these keys
    # eg. basequestion gets sorted by step first, then by _order
    sort_keys = {
        "form.basequestion": ("step", "_order"),
        "form.selectoption": ("question", "_order"),
        "form.step": ("form", "parent", "_order"),
    }

    # Sort each model's objects
    for model in models_by_name:
        objects = models_by_name[model]

        if model in sort_keys:
            sort_key_fields = sort_keys[model]
            models_by_name[model] = sorted(
                objects,
                key=lambda x: tuple(
                    x.get("fields", {}).get(field, float("inf")) or float("-inf")
                    for field in sort_key_fields
                ),
            )

    return models_by_name
