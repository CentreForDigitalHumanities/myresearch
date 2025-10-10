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

interface FormDerivates {
    formWithValues: FormWithValues;
    validationRules: FormValidationRules;
}

/**
 * Transforms a `QueriedForm` object into a `FormWithValues` object by adding a
 * `value` field to each question within the form's steps and substeps, and
 * generates validation rules for required questions.
 *
 * @param queriedForm - The form data retrieved from a query
 * @returns An object containing the form with values and validation rules
 */
function useBuildForm(queriedForm: QueriedForm): FormDerivates {
    const { t } = i18n.global;

    return {
        formWithValues: buildFormWithValues(queriedForm),
        validationRules: buildValidationRules(queriedForm, t),
    };
}

function buildValidationRules(
    queriedForm: QueriedForm,
    t: (key: string) => string,
): FormValidationRules {
    return {
        steps: queriedForm.steps.map((step) => addValidationForStep(step, t)),
    };
}

function addValidationForStep(
    step: Step,
    t: (key: string) => string,
): StepValidationRules {
    return {
        questions: step.questions.map((question) =>
            addValidationForQuestion(question, t),
        ),
        substeps: step.substeps.map((substep) =>
            addValidationForSubstep(substep, t),
        ),
    };
}

function addValidationForSubstep(
    substep: Substep,
    t: (key: string) => string,
): SubstepValidationRules {
    return {
        questions: substep.questions.map((question) =>
            addValidationForQuestion(question, t),
        ),
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

    // Question-type specific rules
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
function buildFormWithValues(queriedForm: QueriedForm): FormWithValues {
    const formWithValues: FormWithValues = {
        ...queriedForm,
        steps: queriedForm.steps.map((step, stepIndex) =>
            addValuesToStep(step, stepIndex),
        ),
    };
    return formWithValues;
}

function addValuesToStep(step: Step, stepIndex: number): StepWithValues {
    return {
        ...step,
        questions: step.questions.map((question, questionIndex) =>
            addValueToQuestion(question, questionIndex, stepIndex),
        ),
        substeps: step.substeps.map((substep, substepIndex) =>
            addValuesToSubstep(substep, stepIndex, substepIndex),
        ),
    };
}

function addValuesToSubstep(
    substep: Substep,
    stepIndex: number,
    substepIndex: number,
): SubstepWithValues {
    return {
        ...substep,
        questions: substep.questions.map((question, questionIndex) =>
            addValueToQuestion(
                question,
                questionIndex,
                stepIndex,
                substepIndex,
            ),
        ),
    };
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

    switch (question.__typename) {
        case "TextQuestionType":
            return { ...question, location, value: "" };
        case "NumberQuestionType":
            return { ...question, location, value: 0 };
        case "TrueFalseQuestionType":
            return { ...question, location, value: question.defaultValue };
        case "FileUploadQuestionType":
            return { ...question, location, value: null };
        case "DateQuestionType":
            return { ...question, location, value: "" };
        case "SelectQuestionType":
            return { ...question, location, value: "" };
    }
}

export { useBuildForm };
