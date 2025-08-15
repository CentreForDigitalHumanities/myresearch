<script setup lang="ts"></script>

<template>
  <div class="col-12">
    <!-- without col-12 accordion will collapse if the body has little content-->
    <div class="accordion" id="questionsMenu">
      <div class="accordion-item">
        <h2 class="accordion-header" id="QuestionOneHeading">
          <button
            class="accordion-button collapsed show"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#questionOne"
            aria-expanded="true"
            aria-controls="questionOne"
          >
            {{ $t("Wat valt er onder persoonsgegevens?") }}
          </button>
        </h2>
        <div
          id="questionOne"
          class="accordion-collapse collapse show"
          aria-labelledby="QuestionOneHeading"
          data-bs-parent="#questionsMenu"
        >
          <div class="accordion-body">
            {{
              $t(
                "Persoonsgegevens zijn gegevens die iets zeggen over een levende persoon van wie je de identiteit weet, van wie je de identiteit te weten kunt komen of die je op een andere manier kunt herkennen. Bijvoorbeeld: contactgegevens zijn persoonsgegevens, maar ook veel onderzoeksgegevens zijn persoonsgegevens. Denk aan meetgegevens, antwoorden op vragen in een vragenlijst of interview, observaties, demografische gegevens etc. Let op: Gegevens die op geen enkele manier meer zijn te koppelen aan een bepaalde persoon, zijn anonieme gegevens. Dit zijn géén persoonsgegevens.",
              )
            }}
          </div>
        </div>
      </div>
      <div class="accordion-item">
        <h2 class="accordion-header" id="QuestionTwoHeading">
          <button
            class="accordion-button collapsed"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#questionTwo"
            aria-expanded="false"
            aria-controls="questionTwo"
          >
            Waarom zijn bananen krom?
          </button>
        </h2>
        <div
          id="questionTwo"
          class="accordion-collapse collapse"
          aria-labelledby="QuestionTwoHeading"
          data-bs-parent="#questionsMenu"
        >
          <div class="accordion-body">
            Omdat ze anders niet in hun schil passen
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
