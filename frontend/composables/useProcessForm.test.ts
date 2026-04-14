import { describe, it, expect, vi } from "vitest";
import { useProcessForm } from "./useProcessForm";
import type { QueriedForm } from "~/components/form/FormWrapper";
import type {
    TextQuestionType,
    NumberQuestionType,
    TrueFalseQuestionType,
    FileUploadQuestionType,
    DateQuestionType,
    SelectQuestionType,
} from "~/generated/gql/graphql";

// Mock the i18n plugin
vi.mock("@/plugins/i18n", () => ({
    i18n: {
        global: {
            t: (key: string) => key,
        },
    },
}));

describe("useProcessForm", () => {
    // Test fixtures
    const createTextQuestion = (
        id: string,
        required = false,
        lines = 1,
        answer: string | null = null,
    ): TextQuestionType => ({
        __typename: "TextQuestionType",
        questionId: id,
        repeatIndex: 0,
        answer,
        textEn: "Text question",
        textNl: "Tekstvraag",
        descriptionEn: "Description text",
        descriptionNl: "Beschrijving tekst",
        lines,
        required,
        placeholderEn: "",
        placeholderNl: "",
        hasConditions: false,
    });

    const createNumberQuestion = (
        id: string,
        required = false,
        positiveOnly = false,
        answer: string | null = null,
    ): NumberQuestionType => ({
        __typename: "NumberQuestionType",
        questionId: id,
        repeatIndex: 0,
        answer,
        textEn: "Number question",
        textNl: "Nummervraag",
        descriptionEn: "Description number",
        descriptionNl: "Beschrijving nummer",
        required,
        positiveOnly,
        hasConditions: false,
    });

    const createTrueFalseQuestion = (
        id: string,
        required = false,
        defaultValue = false,
        answer: string | null = null,
    ): TrueFalseQuestionType => ({
        __typename: "TrueFalseQuestionType",
        questionId: id,
        repeatIndex: 0,
        answer,
        textEn: "True/False question",
        textNl: "Ja/nee-vraag",
        descriptionEn: "Description true/false",
        descriptionNl: "Beschrijving ja/nee",
        required,
        defaultValue,
        hasConditions: false,
    });

    const createFileUploadQuestion = (
        id: string,
        required = false,
        answer: string | null = null,
    ): FileUploadQuestionType => ({
        __typename: "FileUploadQuestionType",
        questionId: id,
        repeatIndex: 0,
        answer,
        textEn: "File upload question",
        textNl: "Bestandsuploadvraag",
        descriptionEn: "Description file upload",
        descriptionNl: "Beschrijving bestandsupload",
        sizeLimit: 99999999,
        required,
        hasConditions: false,
    });

    const createDateQuestion = (
        id: string,
        required = false,
        futureOnly = false,
        answer: string | null = null,
    ): DateQuestionType => ({
        __typename: "DateQuestionType",
        questionId: id,
        repeatIndex: 0,
        answer,
        textEn: "Date question",
        textNl: "Datumvraag",
        descriptionEn: "Description date",
        descriptionNl: "Beschrijving datum",
        futureOnly,
        required,
        hasConditions: false,
    });

    const createSelectQuestion = (
        id: string,
        required = false,
        multiple = false,
        answer: string | null = null,
    ): SelectQuestionType => ({
        __typename: "SelectQuestionType",
        questionId: id,
        repeatIndex: 0,
        answer,
        textEn: "Select question",
        textNl: "Selectievraag",
        descriptionEn: "Description select",
        descriptionNl: "Beschrijving selectie",
        multiple,
        required,
        hasConditions: false,
        options: [
            {
                __typename: "SelectOptionType",
                id: "option1",
                labelEn: "Option 1",
                labelNl: "Optie 1",
                defaultSelected: true,
            },
            {
                __typename: "SelectOptionType",
                id: "option2",
                labelEn: "Option 2",
                labelNl: "Optie 2",
                defaultSelected: false,
            },
        ],
    });

    const createQueriedForm = (): QueriedForm => ({
        __typename: "UserFormType",
        formId: "form1",
        nameEn: "Test Form",
        nameNl: "Testformulier",
        submissionId: "sub1",
        steps: [
            {
                __typename: "StepType",
                stepId: "step1",
                repeatIndex: 0,
                slug: "step1",
                nameEn: "Step 1",
                nameNl: "Step 1",
                descriptionEn: "Step 1 description",
                descriptionNl: "Beschrijving step 1",
                questions: [
                    createTextQuestion("q1", true),
                    createNumberQuestion("q2", false, true),
                ],
                substeps: [
                    {
                        __typename: "StepType",
                        stepId: "substep1",
                        repeatIndex: 0,
                        slug: "substep1",
                        nameEn: "Substep 1",
                        nameNl: "Substep 1",
                        descriptionEn: "Substep 1 description",
                        descriptionNl: "Beschrijving substep 1",
                        questions: [
                            createTrueFalseQuestion("q3", true, true),
                            createFileUploadQuestion("q4", false),
                        ],
                    },
                ],
            },
            {
                __typename: "StepType",
                stepId: "step2",
                repeatIndex: 0,
                slug: "step2",
                nameEn: "Step 2",
                nameNl: "Step 2",
                descriptionEn: "Step 2 description",
                descriptionNl: "Beschrijving step 2",
                questions: [
                    createDateQuestion("q5", true),
                    createSelectQuestion("q6", false),
                ],
                substeps: [],
            },
        ],
    });

    describe("useProcessForm main function", () => {
        it("should return both formWithValues and validationRules", () => {
            const queriedForm = createQueriedForm();
            const result = useProcessForm(queriedForm);

            expect(result).toHaveProperty("formWithValues");
            expect(result).toHaveProperty("validationRules");
        });

        it("should preserve form metadata", () => {
            const queriedForm = createQueriedForm();
            const { formWithValues } = useProcessForm(queriedForm);

            expect(formWithValues.formId).toBe("form1");
            expect(formWithValues.nameEn).toBe("Test Form");
        });
    });

    describe("buildFormWithValues", () => {
        it("should add value and location to all questions in steps", () => {
            const queriedForm = createQueriedForm();
            const { formWithValues } = useProcessForm(queriedForm);

            const step1Question1 = formWithValues.steps[0].questions[0];
            expect(step1Question1).toHaveProperty("value");
            expect(step1Question1).toHaveProperty("location");
            expect(step1Question1.location).toBe("steps.0.questions.0.value");
        });

        it("should add value and location to all questions in substeps", () => {
            const queriedForm = createQueriedForm();
            const { formWithValues } = useProcessForm(queriedForm);

            const substep1Question1 =
                // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
                formWithValues.steps[0].substeps![0].questions[0];
            expect(substep1Question1).toHaveProperty("value");
            expect(substep1Question1).toHaveProperty("location");
            expect(substep1Question1.location).toBe(
                "steps.0.substeps.0.questions.0.value",
            );
        });
    });

    describe("addValueAndLocationToQuestion", () => {
        it("should add empty string value to TextQuestionType when no answer is provided by the backend.", () => {
            const queriedForm = createQueriedForm();
            const { formWithValues } = useProcessForm(queriedForm);

            const textQuestion = formWithValues.steps[0].questions[0];
            expect(textQuestion.__typename).toBe("TextQuestionType");
            expect(textQuestion.value).toBe("");
        });

        it("should use answer value for TextQuestionType when answer exists", () => {
            const form = createQueriedForm();
            form.steps[0].questions[0] = createTextQuestion(
                "q1",
                true,
                1,
                JSON.stringify({ value: "prefilled text" }),
            );
            const { formWithValues } = useProcessForm(form);

            const textQuestion = formWithValues.steps[0].questions[0];
            expect(textQuestion.value).toBe("prefilled text");
        });

        it("should add zero value to NumberQuestionType when no answer is provided by the backend.", () => {
            const queriedForm = createQueriedForm();
            const { formWithValues } = useProcessForm(queriedForm);

            const numberQuestion = formWithValues.steps[0].questions[1];
            expect(numberQuestion.__typename).toBe("NumberQuestionType");
            expect(numberQuestion.value).toBe(0);
        });

        it("should use answer value for NumberQuestionType when answer exists", () => {
            const form = createQueriedForm();
            form.steps[0].questions[1] = createNumberQuestion(
                "q2",
                false,
                true,
                JSON.stringify({ value: 42 }),
            );
            const { formWithValues } = useProcessForm(form);

            const numberQuestion = formWithValues.steps[0].questions[1];
            expect(numberQuestion.value).toBe(42);
        });

        it("should add defaultValue to TrueFalseQuestionType when no answer is provided by the backend.", () => {
            const queriedForm = createQueriedForm();
            const { formWithValues } = useProcessForm(queriedForm);

            const trueFalseQuestion =
                // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
                formWithValues.steps[0].substeps![0].questions[0];
            expect(trueFalseQuestion.__typename).toBe("TrueFalseQuestionType");
            expect(trueFalseQuestion.value).toBe(true);
        });

        it("should use answer value for TrueFalseQuestionType when answer exists", () => {
            const form = createQueriedForm();
            form.steps[0].substeps[0].questions[0] = createTrueFalseQuestion(
                "q3",
                true,
                true,
                JSON.stringify({ value: false }),
            );
            const { formWithValues } = useProcessForm(form);

            const trueFalseQuestion =
                // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
                formWithValues.steps[0].substeps![0].questions[0];
            expect(trueFalseQuestion.value).toBe(false);
        });

        it("should add null value to FileUploadQuestionType", () => {
            const queriedForm = createQueriedForm();
            const { formWithValues } = useProcessForm(queriedForm);

            const fileUploadQuestion =
                // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
                formWithValues.steps[0].substeps![0].questions[1];
            expect(fileUploadQuestion.__typename).toBe(
                "FileUploadQuestionType",
            );
            expect(fileUploadQuestion.value).toBe(null);
        });

        it("should add empty string value to DateQuestionType when no answer", () => {
            const queriedForm = createQueriedForm();
            const { formWithValues } = useProcessForm(queriedForm);

            const dateQuestion = formWithValues.steps[1].questions[0];
            expect(dateQuestion.__typename).toBe("DateQuestionType");
            expect(dateQuestion.value).toBe("");
        });

        it("should add empty string value to SelectQuestionType when no answer", () => {
            const queriedForm = createQueriedForm();
            const { formWithValues } = useProcessForm(queriedForm);

            const selectQuestion = formWithValues.steps[1].questions[1];
            expect(selectQuestion.__typename).toBe("SelectQuestionType");
            expect(selectQuestion.value).toBe("");
        });
    });

    describe("formatQuestionLocation", () => {
        it("should format location for step questions correctly", () => {
            const queriedForm = createQueriedForm();
            const { formWithValues } = useProcessForm(queriedForm);

            expect(formWithValues.steps[0].questions[0].location).toBe(
                "steps.0.questions.0.value",
            );
            expect(formWithValues.steps[0].questions[1].location).toBe(
                "steps.0.questions.1.value",
            );
        });

        it("should format location for substep questions correctly", () => {
            const queriedForm = createQueriedForm();
            const { formWithValues } = useProcessForm(queriedForm);

            expect(
                // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
                formWithValues.steps[0].substeps![0].questions[0].location,
            ).toBe("steps.0.substeps.0.questions.0.value");
            expect(
                // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
                formWithValues.steps[0].substeps![0].questions[1].location,
            ).toBe("steps.0.substeps.0.questions.1.value");
        });
    });

    describe("buildValidationRules", () => {
        it("should create validation rules structure matching form structure", () => {
            const queriedForm = createQueriedForm();
            const { validationRules } = useProcessForm(queriedForm);

            expect(validationRules.steps).toHaveLength(2);
            expect(validationRules.steps[0].questions).toHaveLength(2);
            expect(validationRules.steps[0].substeps).toHaveLength(1);
            expect(validationRules.steps[0].substeps[0].questions).toHaveLength(
                2,
            );
        });

        it("should handle empty substeps array", () => {
            const queriedForm = createQueriedForm();
            const { validationRules } = useProcessForm(queriedForm);

            expect(validationRules.steps[1].substeps).toHaveLength(0);
        });
    });

    describe("addValidationForQuestion", () => {
        it("should add required validation when question is required", () => {
            const queriedForm = createQueriedForm();
            const { validationRules } = useProcessForm(queriedForm);

            const requiredQuestionRules =
                validationRules.steps[0].questions[0].value;
            expect(requiredQuestionRules).toHaveProperty("required");
        });

        it("should not add required validation when question is not required", () => {
            const queriedForm = createQueriedForm();
            const { validationRules } = useProcessForm(queriedForm);

            const notRequiredQuestionRules =
                validationRules.steps[0].questions[1].value;
            expect(notRequiredQuestionRules).not.toHaveProperty("required");
        });

        it("should add positiveOnly validation for NumberQuestionType when positiveOnly is true", () => {
            const queriedForm = createQueriedForm();
            const { validationRules } = useProcessForm(queriedForm);

            const numberQuestionRules =
                validationRules.steps[0].questions[1].value;
            expect(numberQuestionRules).toHaveProperty("positiveOnly");
        });

        it("should not add positiveOnly validation when positiveOnly is false", () => {
            const form: QueriedForm = {
                __typename: "UserFormType",
                formId: "form1",
                nameEn: "Test Form",
                nameNl: "Testformulier",
                submissionId: "sub1",
                steps: [
                    {
                        __typename: "StepType",
                        stepId: "step1",
                        repeatIndex: 0,
                        slug: "step1",
                        nameEn: "Step 1",
                        nameNl: "Step 1",
                        descriptionEn: "Step 1 description",
                        descriptionNl: "Beschrijving step 1",
                        questions: [createNumberQuestion("q1", false, false)],
                        substeps: [],
                    },
                ],
            };

            const { validationRules } = useProcessForm(form);
            const numberQuestionRules =
                validationRules.steps[0].questions[0].value;
            expect(numberQuestionRules).not.toHaveProperty("positiveOnly");
        });

        it("should validate positive numbers correctly", () => {
            const queriedForm = createQueriedForm();
            const { validationRules } = useProcessForm(queriedForm);

            const numberQuestionRules =
                validationRules.steps[0].questions[1].value;
            const positiveValidator =
                numberQuestionRules.positiveOnly.$validator;

            expect(positiveValidator(0, null, null)).toBe(true);
            expect(positiveValidator(10, null, null)).toBe(true);
            expect(positiveValidator(-5, null, null)).toBe(false);
        });
    });
});
