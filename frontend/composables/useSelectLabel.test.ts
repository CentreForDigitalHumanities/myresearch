import { describe, it, expect } from "vitest";
import { useSelectLabel } from "~/composables/useSelectLabel";

const createQuestion = (value: string): SelectQuestionWithValue => ({
    __typename: "SelectQuestionType",
    questionId: "question1",
    textEn: "Question 1",
    textNl: "Vraag 1",
    descriptionEn: "Description 1",
    descriptionNl: "Beschrijving 1",
    hasConditions: false,
    multiple: true,
    repeatIndex: 0,
    required: false,
    location: "location1",
    value,
    options: [
        {
            __typename: "SelectOptionType",
            id: "1",
            labelEn: "Option 1",
            labelNl: "Optie 1",
            defaultSelected: false,
        },
        {
            __typename: "SelectOptionType",
            id: "2",
            labelEn: "Option 2",
            labelNl: "Optie 2",
            defaultSelected: false,
        },
        {
            __typename: "SelectOptionType",
            id: "3",
            labelEn: "Option 3",
            labelNl: "Optie 3",
            defaultSelected: false,
        },
    ],
});

describe("useSelectLabel", () => {
    it("returns the correct label for a single selected option", () => {
        const question = createQuestion("1");
        const label = useSelectLabel(question);
        expect(label).toBe("Option 1");
    });

    it("returns the correct labels for multiple selected options", () => {
        const question = createQuestion("1,2");
        const label = useSelectLabel(question);
        expect(label).toBe("Option 1, Option 2");
    });

    it("returns null when no options are selected", () => {
        const question = createQuestion("");
        const label = useSelectLabel(question);
        expect(label).toBeNull();
    });

    it("returns null when selected options do not match any available options", () => {
        const question = createQuestion("4");
        const label = useSelectLabel(question);
        expect(label).toBeNull();
    });
});
