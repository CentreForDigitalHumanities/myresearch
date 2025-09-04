<script setup lang="ts">
import useEthicsLinks from "~/composables/useEthicsLinks";
</script>
<template>
  <div class="uu-content">
    <Title>{{ $t("MyResearch") }}</Title>
    <div class="uu-hero">
      <h1>{{ $t("Home") }}</h1>
    </div>
    <div class="uu-sidebar-container uu-sidebar-right">
      <div class="uu-sidebar-content">
        <h2 class="uu-sidebar-header-linked">
          {{ $t("What is MyResearch?") }}
        </h2>
        <div class="uu-container">
          {{
            $t(
              "My Research is a website that helps researchers with submitting a request to start a research. On this website you can register your research at the processing register. But first you should fill in the roadmap",
            )
          }}
        </div>
        <h2 class="uu-sidebar-header-linked">
          {{ $t("Roadmap") }}
        </h2>
        <div>
          {{
            $t(
              "The roadmap is a questionnaire that helps researchers to find out what needs to happen to submit a request to start a research. Do I need to register my research at processing register at all. Perhaps that isn't needed? Questions that the roadmap helps answering",
            )
          }}
          <div class="uu-container">
            <button class="btn btn-primary width: 40%">
              Mooie afbeelding of niet
            </button>
            <div class="card" style="width: 60%">
              <div class="card-body">
                <h5 class="card-title">{{ $t("Start a new roadmap") }}</h5>
                <p class="card-text">
                  {{ $t("Also possible as orientation") }}
                </p>
                <a href="#" class="btn btn-primary">{{
                  $t("Start Roadmap")
                }}</a>
              </div>
            </div>
          </div>
        </div>
      </div>
      <aside class="uu-sidebar pe-3">
        <RecentActivity />
      </aside>
    </div>
    <div class="uu-sidebar-container uu-sidebar-right uu-sidebar-sticky">
      <div class="uu-sidebar-content">
        <h2 class="uu-sidebar-header-linked">
          {{ $t("Processing register") }}
        </h2>
        <p>
          {{
            $t(
              "At the processing register you register your studies that contain personal data. The processing register is a central place for all studies with personal data. The Dutch government under the Algemene Verordening Gegevensbescherming (AVG) demands that studies are registered where personal data plays a role. Registering such studies also has an advantage for that researcher that registers the study: registration gives a user-friendly overview about aspects in data processing such as the type of personal data, the persons to whom those data apply, retention periods, used software, necessary security measures and the different parties that play a role",
            )
          }}
        </p>
      </div>
      <aside class="uu-sidebar pe-3">
        <FrequentQuestions
          questionsGroup="processingRegister"
          title="Frequent questions"
        />
      </aside>
    </div>
    <div class="uu-sidebar-container uu-sidebar-right uu-sidebar-sticky">
      <div class="uu-sidebar-content">
        <h2 class="uu-sidebar-header-linked">
          {{ $t("Ethical commission") }}
        </h2>
        <p>
          {{
            $t(
              "Formal approval by a chamber for the FEtC-H (by means of an official approval letter) is required for research involving human participants within the UU Faculty of Humanities. You must acquire this approval prior even to recruiting participants. Therefore, always wait for the letter of approval before starting research activities.",
            )
          }}
        </p>
        <p>
          <a :href="useEthicsLinks('FEtC_H')" target="_blank">{{
            $t("link.UU-webpage of the FEtC-H")
          }}</a>
          for news and upcoming dates.
        </p>
        <p>
          <a :href="useEthicsLinks('FEtC_H_regulations')" target="_blank">{{
            $t("link.Regulations of the FEtC-H")
          }}</a>
        </p>
        <p>
          {{
            $t(
              "Het reglement van de FETC-GW. Tijdens de aanvraagprocedure kan er om een of meer bijlagen worden gevraagd. Gebruik daarvoor de juiste (meest recente) voorbeelddocumenten/templates.",
            )
          }}
        </p>
      </div>
      <aside class="uu-sidebar pe-3">
        <FrequentQuestions
          questionsGroup="ethicalCommission"
          title="Frequent questions"
        />
      </aside>
    </div>
    <div class="uu-sidebar-container uu-sidebar-right uu-sidebar-sticky">
      <div class="uu-sidebar-content">
        <FrequentQuestions title="Other questions" questionsGroup="" />
      </div>
      <aside class="uu-sidebar">
        <h2 class="uu-sidebar-header-linked">Contact</h2>
        <p>
          {{
            $t(
              "For questions about the processing register contact the privacy officer: ",
            )
          }}<a href="mailto:l.j.w.m.kessels@uu.nl">l.j.w.m.kessels@uu.nl</a>
        </p>
        <p>
          {{ $t("For compliments contact: ")
          }}<a href="mailto:portaldev.gw@uu.nl">portaldev.gw@uu.nl</a>
        </p>
      </aside>
    </div>
  </div>
</template>
<style scoped></style>
