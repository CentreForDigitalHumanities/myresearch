<script setup lang="ts">
import { mockData } from "~/shared/mockData";

const props = defineProps({
  questionsGroup: String,
  title: String,
});

let groupName = "";
let questionsList = <string[]>[""];
let answersList = <string[]>[""];

if (props.questionsGroup == "processingRegister") {
  groupName = props.questionsGroup;
  questionsList = mockData.questionsProcessingRegister;
  answersList = mockData.answersProcessingRegister;
} else if (props.questionsGroup == "ethicalCommission") {
  groupName = props.questionsGroup;
  questionsList = mockData.questionsEthicalCommission;
  answersList = mockData.answersEthicalCommission;
}
const accordionItems = <any>[];
for (let i = 0; i < questionsList.length; i++) {
  accordionItems.push({
    id: groupName + i,
    question: questionsList[i],
    answer: answersList[i],
  });
}
</script>

<template>
  <div class="mw-100">
    <h2 v-if="props.title" class="uu-sidebar-header-linked">
      {{ $t(props.title) }}
    </h2>
    <!-- warning: translations inside this accordion do not change until page is reloaded -->
    <div class="accordion mw-100" v-bind:id="'accordion' + groupName">
      <div
        class="mw-100"
        v-for="accordionItem in accordionItems"
        :key="accordionItem.id"
      >
        <div class="accordion-item mw-100">
          <h2 class="accordion-header">
            <button
              class="accordion-button"
              type="button"
              data-bs-toggle="collapse"
              v-bind:data-bs-target="'#collapse' + accordionItem.id"
              aria-expanded="false"
              v-bind:aria-controls="'collapse' + accordionItem.id"
            >
              {{ accordionItem.question }}
            </button>
          </h2>
          <div
            v-bind:id="'collapse' + accordionItem.id"
            class="accordion-collapse collapse mw-100"
            v-bind:data-bs-parent="'#accordion' + groupName"
          >
            <div class="accordion-body mw-100">{{ accordionItem.answer }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
