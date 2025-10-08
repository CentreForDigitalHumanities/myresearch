<script lang="ts" setup>
import { type MockQuestionKey, mockQuestions } from "~/shared/mockData";

interface Props {
    questionsGroup: MockQuestionKey;
    title: string;
}
const props = defineProps<Props>();

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

const isLinkData = (obj: LinkData | string | ImageData): obj is LinkData => {
    return obj.hasOwnProperty("url");
};
const isImageData = (obj: LinkData | string | ImageData): obj is ImageData => {
    return obj.hasOwnProperty("imageUrl");
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
                                <!-- I just want a space here there has to be a better way to do this. -->
                            </template>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
