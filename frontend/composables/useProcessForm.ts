import { helpers, required } from "@vuelidate/validators";
import type { Substep, QueriedForm, Step } from "~/components/form/FormWrapper";
import type { ErrorObject } from "@vuelidate/core";
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
    errors?: ErrorObject[];
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
    hasErrors?: boolean;
};

export type StepWithValues = Omit<Step, "questions" | "substeps"> & {
    questions: QuestionWithValue[];
    substeps: SubstepWithValues[] | null;
    hasErrors?: boolean;
};

export type CombinedStepWithValues = StepWithValues | SubstepWithValues;

export type FormWithValues = Omit<QueriedForm, "steps"> & {
    steps: StepWithValues[];
};

// Validation-related types
type ValidationRule = {
    value: Record<string, ValidationRuleWithParams>;
};

type SubstepValidationRules = {
    questions: ValidationRule[];
};

type StepValidationRules = {
    questions: ValidationRule[];
    substeps: SubstepValidationRules[];
};

export type FormValidationRules = {
    steps: StepValidationRules[];
};

interface FormAndValidation {
    formWithValues: FormWithValues;
    validationRules: FormValidationRules;
}

/**
 * Processes a queried form (QueriedForm) to produce two derived structures:
 *
 * 1. **Form structure with default values** (FormWithValues):
 *    - Augmented QueriedForm with `value` and `location` properties for each question.
 *    - `value`: initialized to a type-appropriate default (empty string, 0, false, null, etc.).
 *    - `location`: dot-notation path to the question's value (e.g. "steps.0.substeps.1.questions.2.value").
 *      This path enables mapping between form values and validation rules.
 *
 * 2. **Validation rules object** (FormValidationRules):
 *    - Mirrors the form structure as required by Vuelidate.
 *    - Contains validation rules for each question (e.g. required, positiveOnly).
 *    - Rules are based on question properties and type-specific constraints.
 *
 * @param queriedForm - The form data retrieved from a GraphQL query
 * @returns An object containing:
 *  - `formWithValues`: The augmented form structure with value/location properties.
 *  - `validationRules`: The Vuelidate-compatible validation rules object.
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

/**
 * Formats and returns a string representing the location of a question within a nested form structure, e.g. `"steps.0.substeps.1.questions.2.value"` for the value of the 3rd question in the 2nd substep of the 1st step.
 */
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

/**
 * Parses the answer JSON string and returns a typed value.
 * Falls back to default values when answer is null/undefined.
 */
function parseAnswer<ReturnType>(
    answer: QuestionType["answer"],
    typename: QuestionType["__typename"],
    defaultValue?: boolean,
): ReturnType {
    if (answer) {
        try {
            const parsed: unknown = JSON.parse(answer);
            // The answer object typically has a 'value' key
            if (
                parsed &&
                typeof parsed === "object" &&
                "value" in parsed &&
                (typeof parsed.value === "string" ||
                    typeof parsed.value === "number" ||
                    typeof parsed.value === "boolean")
            ) {
                return parsed.value as ReturnType;
            }
            if (
                parsed &&
                typeof parsed === "object" &&
                "value" in parsed &&
                Array.isArray(parsed.value)
            ) {
                return parsed.value.join(", ") as ReturnType;
            }
            // Unexpected format, return type-appropriate default
            return getDefaultAnswer(typename, defaultValue) as ReturnType;
        } catch (e) {
            // If parsing fails, return type-appropriate default
            return getDefaultAnswer(typename, defaultValue) as ReturnType;
        }
    }

    // Return type-appropriate defaults when no answer exists
    return getDefaultAnswer(typename, defaultValue) as ReturnType;
}

// Helper to get type-appropriate default answer
function getDefaultAnswer(
    typename: QuestionType["__typename"],
    defaultValue?: boolean,
): string | number | boolean | null {
    switch (typename) {
        case "TextQuestionType":
        case "DateQuestionType":
        case "SelectQuestionType":
            return "";
        case "NumberQuestionType":
            return 0;
        case "TrueFalseQuestionType":
            return defaultValue ?? false;
        case "FileUploadQuestionType":
            return null;
        default:
            return "";
    }
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
                value: parseAnswer<string>(
                    question.answer,
                    question.__typename,
                ),
            };
        case "NumberQuestionType":
            return {
                ...question,
                location,
                value: parseAnswer<number>(
                    question.answer,
                    question.__typename,
                ),
            };
        case "TrueFalseQuestionType":
            return {
                ...question,
                location,
                value: parseAnswer<boolean>(
                    question.answer,
                    question.__typename,
                    question.defaultValue,
                ),
            };
        case "FileUploadQuestionType":
            return {
                ...question,
                location,
                value: parseAnswer<null>(question.answer, question.__typename),
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
                addValidationRule(question, t),
            ),
            substeps: step.substeps.map((substep) => ({
                questions: substep.questions.map((q) =>
                    addValidationRule(q, t),
                ),
            })),
        })),
    };
}

function addValidationRule(
    question: QuestionType,
    t: (key: string) => string,
): ValidationRule {
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
                    () => t("The number must be positive"),
                    (value: number) => value >= 0,
                );
            }
    }

    return {
        value: rules,
    };
}

export { useProcessForm };
