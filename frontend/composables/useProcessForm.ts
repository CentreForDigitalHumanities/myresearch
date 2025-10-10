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

// Augmented question types
interface LocatedQuestion {
    location: string; // Should be something like "steps.0.substeps.1.questions.2"
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

export type SubstepWithValues = Omit<Substep, "questions"> & {
    questions: QuestionWithValue[];
};

export type StepWithValues = Omit<Step, "questions" | "substeps"> & {
    questions: QuestionWithValue[];
    substeps: SubstepWithValues[] | null;
};

export type CombinedStepWithValues = StepWithValues | SubstepWithValues;

export type FormWithValues = Omit<QueriedForm, "steps"> & {
    steps: StepWithValues[];
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
 * Processes a queried form (QueriedForm) to produce two derivatives:
 *
 * 1. **Form structure with default values** (FormWithValues):
 *    - Augments the QueriedForm with `value` and `location` properties for each question.
 *    - `value`: initialized to a type-appropriate default (empty string, 0, false, null, etc.)
 *    - `location`: dot-notation path to the question's value (e.g. "steps.0.substeps.1.questions.2.value")
 *      This path enables mapping between form values and validation rules.
 *
 * 2. **Validation rules object** (FormValidationRules):
 *    - Mirrors the form structure as required by Vuelidate
 *    - Contains validation rules for each question (e.g. required, positiveOnly)
 *    - Rules are based on question properties and type-specific constraints
 *
 * @param queriedForm - The form data retrieved from a GraphQL query
 * @returns An object containing:
 *  - `formWithValues`: The augmented form structure with value/location properties
 *  - `validationRules`: The Vuelidate-compatible validation rules object
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
            questions: step.questions.map((question, questionIndex) =>
                addValueAndLocationToQuestion(
                    question,
                    questionIndex,
                    stepIndex,
                ),
            ),
            substeps: step.substeps.map((substep, substepIndex) => ({
                ...substep,
                questions: substep.questions.map((question, questionIndex) =>
                    addValueAndLocationToQuestion(
                        question,
                        questionIndex,
                        stepIndex,
                        substepIndex,
                    ),
                ),
            })),
        })),
    };
}

function formatQuestionLocation(
    questionIndex: number,
    stepIndex: number,
    substepIndex?: number,
): string {
    const locationParts: string[] = ["steps", stepIndex.toString()];
    if (substepIndex !== undefined) {
        locationParts.push("substeps", substepIndex.toString());
    }
    locationParts.push("questions", questionIndex.toString(), "value");

    return locationParts.join(".");
}

function addValueAndLocationToQuestion(
    question: QuestionType,
    questionIndex: number,
    stepIndex: number,
    substepIndex?: number,
): QuestionWithValue {
    const location = formatQuestionLocation(
        questionIndex,
        stepIndex,
        substepIndex,
    );

    switch (question.__typename) {
        case "TextQuestionType":
        case "DateQuestionType":
        case "SelectQuestionType":
            return {
                ...question,
                location,
                value: "",
            };
        case "NumberQuestionType":
            return {
                ...question,
                location,
                value: 0,
            };
        case "TrueFalseQuestionType":
            return {
                ...question,
                location,
                value: question.defaultValue,
            };
        case "FileUploadQuestionType":
            return {
                ...question,
                location,
                value: null,
            };
    }
}

function buildValidationRules(
    queriedForm: QueriedForm,
    t: (key: string) => string,
): FormValidationRules {
    return {
        steps: queriedForm.steps.map((step) => ({
            questions: step.questions.map((question) =>
                addValidationForQuestion(question, t),
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
