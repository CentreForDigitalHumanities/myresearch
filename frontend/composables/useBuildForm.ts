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

export type TextQuestionWithValue = TextQuestionType & { value: string; };
export type NumberQuestionWithValue = NumberQuestionType & { value: number; };
export type TrueFalseQuestionWithValue = TrueFalseQuestionType & {
    value: boolean;
};
export type FileUploadQuestionWithValue = FileUploadQuestionType & {
    value: File | null;
};
export type DateQuestionWithValue = DateQuestionType & { value: string; };
export type SelectQuestionWithValue = SelectQuestionType & {
    value: string;
};

type QuestionWithValue =
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

/**
 * Transforms a `QueriedForm` object into a `FormWithValues` object by adding a
 * `value` field to each question within the form's steps and substeps.
 *
 * @param queriedForm - The form data retrieved from a query
 * @returns A new `FormWithValues` object where each question includes an 
 * additional `value` field.
 */
function useBuildForm(queriedForm: QueriedForm): FormWithValues {
    const newFormObject: FormWithValues = {
        ...queriedForm,
        steps: queriedForm.steps.map((step) => ({
            ...step,
            questions: step.questions.map((question) =>
                addValueField(question),
            ),
            substeps: step.substeps.map((substep) => ({
                ...substep,
                questions: substep.questions.map((question) =>
                    addValueField(question),
                ),
            })),
        })),
    };
    return newFormObject;
}

function addValueField(question: QuestionType): QuestionWithValue {
    switch (question.__typename) {
        case "TextQuestionType":
            return { ...question, value: "" };
        case "NumberQuestionType":
            return { ...question, value: 0 };
        case "TrueFalseQuestionType":
            return { ...question, value: question.defaultValue };
        case "FileUploadQuestionType":
            return { ...question, value: null };
        case "DateQuestionType":
            return { ...question, value: "" };
        case "SelectQuestionType":
            return { ...question, value: "" };
    }
}

export { useBuildForm };
