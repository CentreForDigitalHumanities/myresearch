import { useTranslateableAttribute } from "~/composables/useLocalisation";
import type { SelectQuestionWithValue } from "~/composables/useProcessForm";

/**
 * Returns a string representation of the selected options for a select question, or null if none are selected.
 */
export function useSelectLabel(
    question: SelectQuestionWithValue,
): string | null {
    const answers = question.value.split(",").map((answer) => answer.trim());
    const labels = answers
        .map((answer) =>
            question.options.find((option) => answer.includes(option.id)),
        )
        .filter((option) => option !== undefined)
        .map((option) => useTranslateableAttribute(option, "label"));
    return labels.length > 0 ? labels.join(", ") : null;
}
