# The Form Module

## Overview

The Form module allows us to create multi-step forms with sophisticated conditional logic. We can use it to both define form templates, track user submissions and return user-specific views of forms via GraphQL. It is deliberately kept generic so it can be used for all forms in this application and potentially shared with other applications in the future.

## Core Concepts

This module maintains a strict separation between **form templates**, which are shared across users, and **user-specific forms**.

## Form templates

Forms follow a hierarchical structure:

```
MRForm (top-level form)
  └── Step (top-level steps)
      ├── Question (questions within step)
      └── Step (substeps - nested steps)
          └── Question (questions within substep)
```

-   **MRForm**: the root object for a form, identified by name. This will be versioned in the future so we can create new versions of the same form over time without affecting existing submissions.
-   **Step**: a section within a form, can be top-level or nested as substeps. In addition to questions, steps may contain `StepInfoQuestion` and `StepInfoText` objects for displaying information to users.
-   **Question**: represents a single question within a step, of various types (text, number, select, etc).

In principle, there is no limit to the depth of step nesting, but in practice we usually keep it to 1-2 levels for usability. GraphQL enforces a practical limit on nesting depth, as you cannot query infinitely deep structures.

### Questions

The module currently supports six question types. All inherit from **BaseQuestion**, which defines common fields such as `text`, `step`, `description`, and `required`. Like **MRForm** and **Step**, questions are shared across users and considered part of the form template.

The following question types are available:

1. **TextQuestion**: Free-form text input
2. **NumberQuestion**: Numeric input
3. **TrueFalseQuestion**: Boolean choice
4. **DateQuestion**: Date picker
5. **SelectQuestion**: Dropdown or multi-select
6. **FileUploadQuestion**: File attachment

Each question type may have additional fields specific to its behavior (e.g. options for `SelectQuestion`, or file type restrictions for `FileUploadQuestion`).

## User-specific forms

Once a user has interacted with a form, we create a user-specific view of that form, taking into account their previous answers and the conditional logic defined in the template. This is done via two main components: the data models that store **user submissions and answers**, and the services that generate and serialize a **user-specific form structure**.

### Submissions and answers

To keep track of the user's progression through a form, two models are used: **UserFormSubmission** and **QuestionResponse**.

**UserFormSubmission** tracks a user's progress through a form. It provides a reference to the user and the form (template), along with some metadata (timestamps for start and completion). It also serves as a parent object for all the user's answers.

**QuestionResponse** stores the user's answer to a specific question within a submission. It includes: a link to the submission, the question answered and some metadata. Because the same question can be repeated multiple times (due to conditional logic), `repeat_index` is used to distinguish instances.

The `answer_data` field is a JSON object that stores the actual answer in a flexible format, depending on the question type. In the future, this may be replaced by a more structured approach, e.g. subtypes for each question type. For now, however, a single JSON field is used to store answers to each question type.

Answer formats by question type:

```json
TextQuestion:       {"value": "user text"}
NumberQuestion:     {"value": 42}
TrueFalseQuestion:  {"value": true}
DateQuestion:       {"value": "2025-12-31"}
SelectQuestion:     {"option_ids": [1, 3]}
FileUploadQuestion: {"file_url": "/path/to/file"}
```

### User-specific form structure

The **FormEvaluator** and **UserFormResolver** services work together to create a user-specific view of a form, taking into account the user's previous answers and the conditional logic defined in the form template. The resolver takes the evaluator as its input. They are designed to be independent of any specific serialization format (e.g. GraphQL), allowing for flexibility in how user forms are presented.

-   **FormEvaluator**: This service evaluates which steps and questions should be shown to the user based on their previous answers. It performs the following tasks:

    -   Creates a tree-like structure representing the form, steps, and questions.
    -   Retrieves an existing user submission or creates a new one if requested.
    -   Evaluates conditional logic to determine visibility and repetition of steps/questions.
    -   Remains agnostic to serialization/output formats.
    -   Caches question responses for efficient lookups during evaluation.

-   **UserFormResolver**: This service takes the output from the FormEvaluator and constructs a complete user-specific form structure in GraphQL types. It recursively builds the step and question hierarchy, including all repeated instances, and attaches the user's answers to each question instance.

### GraphQL Types

The user-specific form structure is represented in GraphQL using the following types.

-   **UserFormType**: represents the entire user-specific form, containing top-level steps.
-   **StepType**: represents a step within the user form, including substeps and questions. It also includes `repeat_index` for repeated instances.
-   Various question types:
    -   **TextQuestionType**
    -   **NumberQuestionType**
    -   **TrueFalseQuestionType**
    -   **DateQuestionType**
    -   **SelectQuestionType**
    -   **FileUploadQuestionType**

Each question type implements **BaseQuestionInterface**, which contains common fields such as `text`, `description`, `required` and the user's `answer`. In addition, the field `question_id` refers back to the template question, while `repeat_index` indicates which instance of a repeated question this is.

## Conditional Logic

The conditional logic system allows steps and questions to be shown, hidden, or repeated based on user responses to other questions.

### Condition Types

Both **QuestionCondition** and **StepCondition** inherit from **BaseCondition** and support four condition types:

1. **show**: display the target only when the condition is met.
2. **hide**: hide the target when the condition is met.
3. **repeat**: repeat the target a fixed number of times when triggered.
4. **repeat_dynamic**: repeat the target based on the answer value (e.g., "How many children?" → repeat child info questions).

Visibility is determined according to the following rules.

1. If both show and hide conditions exist, **show conditions take precedence**
2. If only show conditions exist, the target is visible if **at least one show condition is met**
3. If only hide conditions exist, the target is hidden if **at least one hide condition is met**
4. If no conditions exist, the target is **visible by default**

### Condition Structure

Each condition defines:

-   **trigger_question**: the question whose answer determines if this condition activates.
-   **target_question** or **target_step**: the question or step affected by this condition.
-   **condition_type**: one of the condition types above (`show`/`hide`/`repeat`/`repeat_dynamic`).
-   **trigger_value**: the answer criteria that activates this condition (see Trigger Values below).
-   **repeat_count**: for static repeats, how many times to repeat.
-   **use_answer_as_count**: for dynamic repeats, whether to use the answer's value as the repeat count.

### Trigger Values

The `trigger_value` field is a JSON object defining when a condition activates. The format depends on the question type of the `trigger_question`.

1. TextQuestion: string matching

```json
{ "value": "expected text" }
```

2. NumberQuestion: numeric comparisons, using `min`, `max` or `exact`

```json
{"min": 5}           // Answer >= 5
{"max": 10}          // Answer <= 10
{"exact": 7}         // Answer == 7
```

3. TrueFalseQuestion: boolean matching

```json
{ "value": true }
```

4. DateQuestion: string matching

```json
{ "value": "2025-12-19" }
```

5. SelectQuestion: option ID matching

```json
{ "option_ids": [1, 3] }
```

If multiple option IDs are provided in the same condition, **all** must be present in the user's answer for the condition to be met. If the user selects additional options beyond those specified, the condition is still considered met.

If you wish to implement a condition that triggers if **any** of a set of options are selected,
create multiple conditions with the same target and different single option IDs.

6. BooleanQuestion: boolean matching

```json
{ "value": true }
```

7. Any question type: non-empty answer

```json
{}
```

Conditions with this value are always considered met.

### Repetition

Conditions of type `repeat` and `repeat_dynamic` allow steps or questions to be repeated multiple times based on user input. The steps and questions returned to the user will include multiple instances, each with a unique `repeat_index` starting from 0. The repeat index also features in the slug of the `StepType`, which is used in the URL of the step.

#### Static Repeats

When the trigger question's answer matches `trigger_value`, the target appears `repeat_count` times.

```python
# Condition configuration
condition_type = "repeat"
trigger_value = {"value": true}  # When checkbox is checked
repeat_count = 3                  # Create 3 instances
```

#### Dynamic Repeats

The numeric value from the trigger question's answer determines the repeat count.

```python
# Condition configuration
condition_type = "repeat_dynamic"
trigger_value = {}                # Any answer triggers
use_answer_as_count = True        # Use answer value
```

A good use case could be:

```
Question: "How many collaborators do you have?"
Answer: 3
Result: The "Collaborator Information" step repeats 3 times
```

For safety, the number of repeated instances is constrained to 1-10 (see `MAX_REPEAT_LIMIT`).


## Updating form fixtures

The application comes with a fixture with a very basic sample form for the Wegwijzer located at `form/fixtures/wegwijzer.json`. To use it, load it into your database with:

```bash
python manage.py loaddata form/fixtures/wegwijzer.json
```

Update the form in Django Admin as you wish. Once you're satisfied, update the fixture by running:

```bash
python manage.py dumpdata form --output form/fixtures/wegwijzer.json --indent 4
```
