import { helpers, required } from "@vuelidate/validators";
import type {
    Substep,
    QueriedForm,
    Step,
} from "~/components/shared/FormWrapper";
import type {
    TextQuestionType,
    NumberQuestionType,
    TrueFalseQuestionType,
    FileUploadQuestionType,
    DateQuestionType,
    SelectQuestionType,
    QuestionType,
} from "~/generated/gql/graphql";
import { i18n } from "@/plugins/i18n";
import type { ValidationRuleWithParams } from "@vuelidate/core";

// Augmented Question types with two additional properties:
// - location: a string representing the path to the question's value in the validation object;
// - value: the actual answer value, with a type corresponding to the question type;
interface LocatedQuestion {
    location: string; // e.g., "steps.0.substeps.1.questions.2"
}

export type TextQuestionWithValue = TextQuestionType &
    LocatedQuestion & {
        value: string;
    };
export type NumberQuestionWithValue = NumberQuestionType &
    LocatedQuestion & {
        value: number;
    };
export type TrueFalseQuestionWithValue = TrueFalseQuestionType &
    LocatedQuestion & {
        value: boolean;
    };
export type FileUploadQuestionWithValue = FileUploadQuestionType &
    LocatedQuestion & {
        value: File | null;
    };
export type DateQuestionWithValue = DateQuestionType &
    LocatedQuestion & {
        value: string;
    };
export type SelectQuestionWithValue = SelectQuestionType &
    LocatedQuestion & {
        value: string;
    };

export type QuestionWithValue =
    | TextQuestionWithValue
    | NumberQuestionWithValue
    | TrueFalseQuestionWithValue
    | FileUploadQuestionWithValue
    | DateQuestionWithValue
    | SelectQuestionWithValue;

type SubstepWithValues = Omit<Substep, "questions"> & {
    questions: QuestionWithValue[];
};

type StepWithValues = Omit<Step, "questions" | "substeps"> & {
    questions: QuestionWithValue[];
    substeps: SubstepWithValues[] | null;
};

export type CombinedStepWithValues = StepWithValues | SubstepWithValues;

export type FormWithValues = Omit<QueriedForm, "steps"> & {
    steps: CombinedStepWithValues[];
};

// Validation-related types
type QuestionValidationRule = {
    value: Record<string, ValidationRuleWithParams>;
};

type SubstepValidationRules = {
    questions: QuestionValidationRule[];
};

type StepValidationRules = {
    questions: QuestionValidationRule[];
    substeps: SubstepValidationRules[];
};

type FormValidationRules = {
    steps: StepValidationRules[];
};

interface FormAndValidation {
    formWithValues: FormWithValues;
    validationRules: FormValidationRules;
}

/**
 * Processes a queried form (QueriedForm) to produce two derivates:
 *
 * 1. A form structure with default values for each question (FormWithValues).
 *   This is the same object as the QueriedForm object, but with added `value`
 *   and `location` properties to each question.
 *
 *      The `value` property holds the value of the question, initialized to a
 *      default value based on the question type.
 *
 *      The `location` property is a string that represents the path to the
 *      question's value in the form structure. We need this to find the
 *      corresponding value in the validation object.
 *
 * 2. A validation object (ValidationRules) containing the rules needed to
 * validate the form. This object mirrors the structure of the form, as
 * required by Vuelidate.
 *
 * @param queriedForm - The form data retrieved from a query
 * @returns An object containing the form with value attributes and the
 * validation rules.
 */
function useProcessForm(queriedForm: QueriedForm): FormAndValidation {
    const { t } = i18n.global;

    return {
        formWithValues: buildFormWithValues(queriedForm),
        validationRules: buildValidationRules(queriedForm, t),
    };
}

function buildFormWithValues(queriedForm: QueriedForm): FormWithValues {
    return {
        ...queriedForm,
        steps: queriedForm.steps.map((step, stepIndex) => ({
            ...step,
            questions: step.questions.map((q, qIndex) =>
                addValueToQuestion(q, qIndex, stepIndex),
            ),
            substeps: step.substeps.map((substep, substepIndex) => ({
                ...substep,
                questions: substep.questions.map((q, qIndex) =>
                    addValueToQuestion(q, qIndex, stepIndex, substepIndex),
                ),
            })),
        })),
    };
}

function getDefaultValueForQuestion(question: QuestionType): unknown {
    switch (question.__typename) {
        case "TextQuestionType":
        case "DateQuestionType":
        case "SelectQuestionType":
            return "";
        case "NumberQuestionType":
            return 0;
        case "TrueFalseQuestionType":
            return question.defaultValue;
        case "FileUploadQuestionType":
            return null;
    }
}

function addValueToQuestion(
    question: QuestionType,
    questionIndex: number,
    stepIndex: number,
    substepIndex?: number,
): QuestionWithValue {
    const locationParts: string[] = ["steps", stepIndex.toString()];
    if (substepIndex !== undefined) {
        locationParts.push("substeps", substepIndex.toString());
    }
    locationParts.push("questions", questionIndex.toString(), "value");

    const location = locationParts.join(".");

    return {
        ...question,
        location,
        value: getDefaultValueForQuestion(question) as never,
    };
}

function buildValidationRules(
    queriedForm: QueriedForm,
    t: (key: string) => string,
): FormValidationRules {
    return {
        steps: queriedForm.steps.map((step) => ({
            questions: step.questions.map((q) =>
                addValidationForQuestion(q, t),
            ),
            substeps: step.substeps.map((substep) => ({
                questions: substep.questions.map((q) =>
                    addValidationForQuestion(q, t),
                ),
            })),
        })),
    };
}

function addValidationForQuestion(
    question: QuestionType,
    t: (key: string) => string,
): QuestionValidationRule {
    const rules: Record<string, ValidationRuleWithParams> = {};

    // General validation rules
    if (question.required) {
        rules.required = helpers.withMessage(
            t("This field is required"),
            required,
        );
    }

    // Question-type specific rules. This is an example. Add more as needed.
    switch (question.__typename) {
        case "NumberQuestionType":
            // Example: Add min/max value validation if needed
            if (question.positiveOnly) {
                rules.positiveOnly = helpers.withMessage(
                    t("The number must be positive"),
                    (value: number) => value >= 0,
                );
            }
    }

    return {
        value: rules,
    };
}

export { useProcessForm };
