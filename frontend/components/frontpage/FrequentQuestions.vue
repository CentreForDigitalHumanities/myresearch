<script lang="ts" setup>
import { MockData, type MockQuestionKey } from "~/shared/mockData";

interface Props {
  questionsGroup: MockQuestionKey;
  title: string;
}
const props = defineProps<Props>();

const questionAnswers: Record<string, string> =
  MockData.mockQuestions[props.questionsGroup];
</script>

<template>
  <div class="mw-100">
    <h2 class="uu-sidebar-header-linked">
      {{ $t(title) }}
    </h2>
    <div class="accordion mw-100" :id="'accordion' + questionsGroup">
      <div
        class="mw-100"
        v-for="(answer, question, index) in questionAnswers"
        :key="questionsGroup + index"
      >
        <div class="accordion-item mw-100">
          <h2 class="accordion-header">
            <button
              class="accordion-button"
              type="button"
              data-bs-toggle="collapse"
              :data-bs-target="'#collapse' + questionsGroup + index"
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
              {{ $t(answer) }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
