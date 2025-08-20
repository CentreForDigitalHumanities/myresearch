<script setup lang="ts">
import { mockData } from "~/shared/mockData";

const props = defineProps({
  QuestionsGroup: String,
});

let groupName = "";

let questionsList = <string[]>[""];
let answersList = <string[]>[""];
let id = 0;

if (props.QuestionsGroup == "processingRegister") {
  groupName = props.QuestionsGroup;
  questionsList = mockData.questionsVerwerkingsregister;
  answersList = mockData.answersVerwerkingsregister;
} else if (props.QuestionsGroup == "ethicalCommission") {
  groupName = props.QuestionsGroup;
  questionsList = mockData.questionsEthicalCommission;
  answersList = mockData.answersEthicalCommission;
}
const accordionItems = <any>[];
for (let i = 0; i < questionsList.length; i++) {
  accordionItems.push({
    id: groupName + id++,
    question: questionsList[i],
    answer: answersList[i],
  });
}
</script>

<template>
  <div class="col-12">
    <!-- without col-12 the accordion can shrink if the accordion-body has little content-->
    <div class="accordion" id="questionsMenu">
      <div v-for="accordionItem in accordionItems" :key="accordionItem.id">
        <div class="accordion-item">
          <!-- TODO: id's are dynamic but the other accordions also collapse when an item is openend-->
          <h2
            class="accordion-header"
            v-bind:id="'header' + 'accordion' + accordionItem.id"
          >
            <button
              class="accordion-button collapsed"
              type="button"
              data-bs-toggle="collapse"
              v-bind:data-bs-target="'#' + 'accordion' + accordionItem.id"
              aria-expanded="true"
              v-bind:aria-controls="'accordion' + accordionItem.id"
            >
              {{ accordionItem.question }}
            </button>
          </h2>
          <div
            v-bind:id="'accordion' + accordionItem.id"
            class="accordion-collapse collapse"
            v-bind:aria-labelledby="'header' + 'accordion' + accordionItem.id"
            data-bs-parent="#questionsMenu"
          >
            <div class="accordion-body">
              {{ accordionItem.answer }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
