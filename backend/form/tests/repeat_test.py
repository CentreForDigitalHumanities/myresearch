import pytest
import json
from copy import deepcopy
from form.models import Step, UserFormSubmission, RepeatableStep
from research.tests import normal_user, test_study

from pprint import pprint


def find_steps(content):
    return content["data"]["form"]["steps"]


def findkey(d, key):
    """
    Finds all the values for a given key in d, at any depth of dict or
    list. Returns a list of dicts in which the found value belongs to a
    top-level key.
    """
    if type(d) == dict:
        if key in d:
            # Found a value for our key!
            found = [deepcopy(d)]
            # But we'll also keep looking inside our found value, while
            # removing it from the remaining pool. We make another copy
            # to not mutate the original dict.
            copy = deepcopy(d)
            item = copy.pop(key)
            return found + findkey([item, copy], key)
        else:
            # Not in this dict, but maybe there's more dicts hidden
            # in the values here. So we set the remainder to the list
            # of those values
            return findkey(list(d.values()), key)
    # Lists are the only other type we look into
    elif type(d) == list:
        if d == []:
            # Empty list, stop looking
            return []
        # Continue looking in the first item of the list
        copy = deepcopy(d)
        item = copy.pop()
        return findkey(item, key) + findkey(copy, key)
    # If d is neither a list or dict, we call it a day
    return []


GetFormQuery = """
query GetForm($submissionId: ID!) {
    form(submissionId: $submissionId, mrPermission: "Edit") {
        formId
        steps {
            stepId
            slug
            nameEn
            background
            repeatIndex
            questions {
                questionId
                repeatIndex
                answer
                responseId
                __typename
            }
            substeps {
                stepId
                slug
                nameEn
                background
                repeatIndex
                questions {
                    questionId
                    repeatIndex
                    answer
                    responseId
                    __typename
                }
            }
        }
    }
}
"""


@pytest.mark.django_db(transaction=True)
def test_repeatable_step(
    client_query,
    test_user,
    submission,
    step,
    form,
    test_study,
    repeatable_step,
):
    response = client_query(
        GetFormQuery,
        user=test_user,
        variables={
            "submissionId": submission.id,
        },
    )
    content = json.loads(response.content)
    assert "errors" not in content
    # There should be two steps in here
    found = findkey(content, "background")
    assert len(found) == 2
    # Assert that the repeatable stap has background=True,
    # while the other does not.
    for step in found:
        step_id = int(step["stepId"])
        if step_id == repeatable_step.id:
            assert step["background"] == True
        else:
            assert step["background"] == False


CreateRepeatQuery = """
mutation CreateRepeat($repeatable_id: ID! $submission_id: ID! $parent_id: ID) {
  createRepeat(repeatableId: $repeatable_id, userFormId: $submission_id, parentId: $parent_id) {
    errors {
      field
      messages
    }
    newRepeatIndex
  }
}
"""


@pytest.mark.django_db(transaction=True)
def test_create_repeat(
    client_query,
    test_user,
    submission,
    step,
    form,
    test_study,
    repeatable_step,
):
    repeatable_id = repeatable_step.repeatable_ptr.pk
    response = client_query(
        CreateRepeatQuery,
        user=test_user,
        variables={
            "submission_id": submission.id,
            "repeatable_id": repeatable_id,
        },
    )
    content = json.loads(response.content)
    assert "errors" not in content
    new_index = int(content["data"]["createRepeat"]["newRepeatIndex"])
    # Now let's get the form again.
    response = client_query(
        GetFormQuery,
        user=test_user,
        variables={
            "submissionId": submission.id,
        },
    )
    content = json.loads(response.content)
    assert "errors" not in content
    # Find all items in content with a stepId key
    found = findkey(content, "stepId")
    assert len(found) == 3
    # Assert that one of the repeatable steps has background=True,
    # and the other carries our new repeatIndex
    # while the other does not.
    passed = 0
    for step in found:
        step_id = int(step["stepId"])
        if step_id == repeatable_step.id:
            if step["repeatIndex"] == new_index:
                assert step["background"] == False
                passed += 1
            else:
                assert step["background"] == True
                passed += 1
        else:
            assert step["background"] == False
            passed += 1
    # Check that all three above cases happened independently
    assert passed == 3


@pytest.mark.django_db(transaction=True)
def test_substep_repeat(
    client_query,
    test_user,
    submission,
    step,
    form,
    test_study,
    repeatable_step,
):
    repeatable_substep = RepeatableStep(
        name="Repeatable substep",
        slug="sub_rep",
        form=form,
        parent=repeatable_step,
    )
    repeatable_substep.save()
    substep_id = repeatable_substep.repeatable_ptr.pk
    # Get the form again
    response = client_query(
        GetFormQuery,
        user=test_user,
        variables={
            "submissionId": submission.id,
        },
    )
    content = json.loads(response.content)
    assert "errors" not in content
    # Find all items in content with a stepId key
    # The substep and its repeat should not be present
    found = findkey(content, "stepId")
    assert len(found) == 2
    step_id = repeatable_step.repeatable_ptr.pk
    # Create a repeat for the main step
    response = client_query(
        CreateRepeatQuery,
        user=test_user,
        variables={
            "submission_id": submission.id,
            "repeatable_id": step_id,
        },
    )
    content = json.loads(response.content)
    new_index = int(content["data"]["createRepeat"]["newRepeatIndex"])
    # Create a repeat for the substep
    response = client_query(
        CreateRepeatQuery,
        user=test_user,
        variables={
            "submission_id": submission.id,
            "repeatable_id": substep_id,
            "parent_id": new_index,
        },
    )
    content = json.loads(response.content)
    assert "errors" not in content
    # Get the form again
    response = client_query(
        GetFormQuery,
        user=test_user,
        variables={
            "submissionId": submission.id,
        },
    )
    content = json.loads(response.content)
    assert "errors" not in content
    # Now we should have five
    found = findkey(content, "stepId")
    assert len(found) == 5
