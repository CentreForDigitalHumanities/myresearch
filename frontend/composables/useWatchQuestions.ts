import type { QuestionWithValue } from "~/composables/useProcessForm";
import type { Ref } from "vue";

type QuestionTypeName = QuestionWithValue["__typename"];

const DEBOUNCED_QUESTION_TYPES: readonly QuestionTypeName[] = [
    "TextQuestionType",
    "NumberQuestionType",
] as const;

const DEBOUNCE_TIME_MS = 300;

/**
 * Watches questions for changes and triggers form submission with appropriate
 * debouncing based on question type.
 */
export function useWatchQuestions(
    watchedQuestions: Ref<QuestionWithValue[]>,
    submit: () => void,
) {
    // Used to keep track of the last submission to determine when values
    // have changed.
    const questionValuesSnapshot = ref<Map<string, unknown>>(
        createSnapshot(watchedQuestions.value),
    );
    const debounceTimerRef = ref<ReturnType<typeof setTimeout> | null>(null);

    // Clean up the timer when the component is unmounted.
    onBeforeUnmount(() => {
        if (debounceTimerRef.value) {
            clearTimeout(debounceTimerRef.value);
        }
    });

    // Watch for changes.
    watchEffect(() => {
        let updateMode: "none" | "debounce-submit" | "submit" = "none";

        for (const question of watchedQuestions.value) {
            const key = questionKey(question);
            const currentValue = question.value;
            const previousValue = questionValuesSnapshot.value.get(key);

            // No change: skip.
            if (previousValue === currentValue) {
                continue;
            }

            // Found a change.
            updateMode = DEBOUNCED_QUESTION_TYPES.includes(question.__typename)
                ? "debounce-submit"
                : "submit";

            // No need to check further questions if we already know we are
            // going to submit with debounce.
            if (updateMode === "debounce-submit") {
                break;
            }
        }

        // Update snapshot
        questionValuesSnapshot.value = createSnapshot(watchedQuestions.value);

        if (updateMode === "none") {
            return;
        }

        if (updateMode === "debounce-submit") {
            debounceSubmit();
        } else {
            submit();
        }
    });

    function debounceSubmit(): void {
        if (debounceTimerRef.value) {
            clearTimeout(debounceTimerRef.value);
        }
        debounceTimerRef.value = setTimeout(() => {
            submit();
            debounceTimerRef.value = null;
        }, DEBOUNCE_TIME_MS);
    }

    function questionKey(question: QuestionWithValue): string {
        if (question.repeatIndex) {
            return `${question.questionId}-${question.repeatIndex.toString()}`;
        } else {
            return question.questionId;
        }
    }

    function createSnapshot(
        questions: QuestionWithValue[],
    ): Map<string, unknown> {
        const snapshot = new Map<string, unknown>();
        for (const question of questions) {
            snapshot.set(questionKey(question), question.value);
        }
        return snapshot;
    }
}
