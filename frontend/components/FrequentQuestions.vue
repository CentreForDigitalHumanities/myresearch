<script setup lang="ts">
import { mockData } from "~/shared/mockData";

const props = defineProps({
  QuestionsGroup: String,
});

let groupName = "";

let questionOne = "aaa";
let answerOne = "aaa";
let questionsList = <string[]>[""];
let answersList = [""];
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
const workingsAccordionItemsWithDuplicate = ref([
  { id: groupName + id++, question: questionOne, answer: answerOne },
]);
const accordionItems = workingsAccordionItemsWithDuplicate; //= ref([]);
for (let i = 0; i < questionsList.length; i++) {
  accordionItems.value.push({
    id: groupName + id++,
    question: questionsList[i],
    answer: answersList[i],
  });
}
//TODO this list is not yet dynamic
</script>

<template>
  <div class="col-12">
    <!-- without col-12 the accordion can shrink if the accordion-body has little content-->
    <div class="accordion" id="questionsMenu">
      <div v-for="accordionItem in accordionItems" :key="accordionItem.id">
        <div class="accordion-item">
          <!-- TODO: id's are dynamic but the other accordions also collapse when an item is openend-->
          <h2 class="accordion-header" v-bind:id="'header' + accordionItem.id">
            <button
              class="accordion-button collapsed"
              type="button"
              data-bs-toggle="collapse"
              v-bind:data-bs-target="'#' + accordionItem.id"
              aria-expanded="true"
              v-bind:aria-controls="accordionItem.id"
            >
              {{ accordionItem.question }}
            </button>
          </h2>
          <div
            v-bind:id="'' + accordionItem.id"
            class="accordion-collapse collapse"
            v-bind:aria-labelledby="'header' + accordionItem.id"
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
