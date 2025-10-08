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

export type Answer = (string | LinkData | ImageData)[];

type LinkData = {
    text: string;
    url: string;
};

type ImageData = {
    imageUrl: string;
    altText: string;
};

const questionAnswers: Record<string, Answer> =
    mockQuestions[props.questionsGroup];

const isLinkData = (
    answerPart: LinkData | string | ImageData,
): answerPart is LinkData => {
    return answerPart.hasOwnProperty("url");
};

const isImageData = (
    answerPart: LinkData | string | ImageData,
): answerPart is ImageData => {
    return answerPart.hasOwnProperty("imageUrl");
};
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
                                <template v-if="isLinkData(answerPart)">
                                    <a
                                        :href="$t(answerPart.url)"
                                        target="_blank"
                                    >
                                        {{ $t(answerPart.text) }}
                                    </a>
                                </template>
                                <template v-else-if="isImageData(answerPart)">
                                    <img
                                        :src="answerPart.imageUrl"
                                        :alt="answerPart.altText"
                                    />
                                </template>
                                <template v-else>
                                    {{ $t(answerPart) }}
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
