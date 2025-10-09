<script lang="ts" setup>
import { mockQuestions } from "~/shared/mockData";

interface Props {
    questionsGroup: FrequentQuestionKey;
    title: string;
}
const props = defineProps<Props>();

export type FrequentQuestionKey =
    | "processingRegistry"
    | "ethicalCommission"
    | "other";

/** One or more FrequentAnswerParts form a FrequentAnswer.
 * @text If url is not null then text is assumed to be the url text */
interface FrequentAnswerPart {
    text: string | null;
    url: string | null;
    image: {
        src: string;
        altText: string;
    } | null;
}
export type FrequentAnswer = FrequentAnswerPart[];

const questionAnswers: Record<string, FrequentAnswer> =
    mockQuestions[props.questionsGroup];
</script>

<template>
    <div class="mw-100">
        <h2 class="uu-sidebar-header-linked">
            {{ $t(title) }}
        </h2>
        <div :id="'accordion' + questionsGroup" class="accordion mw-100">
            <div
                v-for="(answer, question, index) in questionAnswers"
                :key="questionsGroup + index"
                class="mw-100"
            >
                <div class="accordion-item mw-100">
                    <h2 class="accordion-header">
                        <button
                            class="accordion-button"
                            type="button"
                            data-bs-toggle="collapse"
                            :data-bs-target="
                                '#collapse' + questionsGroup + index
                            "
                            aria-expanded="false"
                            :aria-controls="'collapse' + questionsGroup + index"
                        >
                            {{ $t(question) }}
                        </button>
                    </h2>
                    <div
                        :id="'collapse' + questionsGroup + index"
                        class="accordion-collapse collapse mw-100"
                        :data-bs-parent="'#accordion' + questionsGroup"
                    >
                        <div class="accordion-body mw-100">
                            <template
                                v-for="(answerPart, answerIndex) in answer"
                                :key="
                                    'collapse' +
                                    questionsGroup +
                                    index +
                                    answerIndex
                                "
                            >
                                <a
                                    v-if="answerPart.url != null"
                                    :href="$t(answerPart.url)"
                                    target="_blank"
                                >
                                    <template v-if="answerPart.text != null">
                                        {{ $t(answerPart.text) }}
                                    </template>
                                </a>
                                <img
                                    v-else-if="answerPart.image != null"
                                    :src="answerPart.image.src"
                                    :alt="answerPart.image.altText"
                                />
                                <template v-else-if="answerPart.text != null">
                                    {{ $t(answerPart.text) }}
                                </template>
                                {{ " " }}
                            </template>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
