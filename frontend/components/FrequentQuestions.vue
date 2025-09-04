<script lang="ts" setup>
import { mockData } from "~/shared/mockData";

interface Props {
  questionsGroup: string;
  title: string;
}
const props = defineProps<Props>();

const questionAnswers: Map<string, string> | undefined =
  mockData.getQuestionAnswers(props.questionsGroup);

if (questionAnswers === undefined) {
  console.log(
    "undefined questionGroup found for the frequentQuestions component",
  );
}
</script>

<template>
  <div class="mw-100">
    <h2 class="uu-sidebar-header-linked">
      {{ $t(title) }}
    </h2>
    <div class="accordion mw-100" v-bind:id="'accordion' + questionsGroup">
      <div
        class="mw-100"
        v-for="(questionAnswer, index) in questionAnswers"
        :key="questionsGroup + index"
      >
        <div class="accordion-item mw-100">
          <h2 class="accordion-header">
            <button
              class="accordion-button"
              type="button"
              data-bs-toggle="collapse"
              v-bind:data-bs-target="'#collapse' + questionsGroup + index"
              aria-expanded="false"
              v-bind:aria-controls="'collapse' + questionsGroup + index"
            >
              {{ $t(questionAnswer[0]) }}
            </button>
          </h2>
          <div
            v-bind:id="'collapse' + questionsGroup + index"
            class="accordion-collapse collapse mw-100"
            v-bind:data-bs-parent="'#accordion' + questionsGroup"
          >
            <div class="accordion-body mw-100">
              {{ $t(questionAnswer[1]) }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
