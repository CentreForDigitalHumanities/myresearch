<script setup lang="ts">
import useEthicsLinks from "~/composables/useEthicsLinks";
</script>
<template>
  <div class="uu-content">
    <Title>{{ $t("MyResearch") }}</Title>
    <div class="uu-hero">
      <h1>{{ $t("Welcome to MyResearch!") }}</h1>
    </div>
    <div class="uu-sidebar-container uu-sidebar-right">
      <div class="uu-sidebar-content">
        <div class="uu-container">
          {{ $t("english_introduction") }}
        </div>
      </div>
      <aside class="uu-sidebar pe-3">
        <!-- TODO pe-3 does not exactly give 1.25 rem as pixels but it seems very close, low prio -->
        <RecentActivity />
      </aside>
    </div>
    <div class="uu-sidebar-container uu-sidebar-right uu-sidebar-sticky">
      <div class="uu-sidebar-content">
        <h2 class="uu-sidebar-header-linked">
          {{ $t("Processing register") }}
        </h2>
        <p>
          {{ $t("english_verwerkingsregister_uitleg") }}
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
        <h3>{{ $t("Before you begin") }}</h3>
        <p>{{ $t("Before submitting an application, please consult:") }}</p>
        <p>
          <a :href="useEthicsLinks('FEtC_H')" target="_blank">{{
            $t("link.UU-webpage of the FEtC-H")
          }}</a>
          for news and upcoming dates.
        </p>
        <p>
          <a :href="useEthicsLinks('model_documents')" target="_blank">{{
            $t("link.Model documents")
          }}</a>
          Tijdens de aanvraagprocedure kan er om een of meer bijlagen worden
          gevraagd. Gebruik daarvoor de juiste (meest recente)
          voorbeelddocumenten
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
        <!-- TODO low prio: sidebar header linked does not work on the aside side, does work on the uu example site. According to the description it needs to be pixel perfect -->
        <FrequentQuestions
          questionsGroup="ethicalCommission"
          title="Frequent questions"
        />
      </aside>
    </div>
    <div class="uu-sidebar-container uu-sidebar-right uu-sidebar-sticky">
      <div class="uu-sidebar-content">
        <FrequentQuestions title="Other questions" />
      </div>
      <aside class="uu-sidebar">
        <h2 class="uu-sidebar-header-linked">Contact</h2>
        <p>
          {{ $t("questions_privacy_officier")
          }}<a href="mailto:l.j.w.m.kessels@uu.nl">l.j.w.m.kessels@uu.nl</a>
        </p>
        <p>
          {{ $t("questions_technical")
          }}<a href="mailto:portaldev.gw@uu.nl">portaldev.gw@uu.nl</a>
        </p>
      </aside>
    </div>
  </div>
</template>
<style scoped></style>
<!--
calc(50% - var(--bs-uu-content-width) / 2)
--bs-uu-content-width: 40rem;


  --bs-uu-sidebar-width: 21.875rem;
  --bs-uu-sidebar-gap: 6.25rem;
  --bs-uu-sidebar-breakpoint: lg;
  --bs-uu-sidebar-padding-x: 1.25rem;
  --bs-uu-sidebar-padding-y: 1.25rem;
  --bs-uu-sidebar-mobile-padding-y: 0.625rem;
  --bs-uu-sidebar-header-padding-y: 0.625rem;
  --bs-uu-sidebar-header-font-weight: 0;
  --bs-uu-sidebar-nav-padding-y: 0rem;
  --bs-uu-sidebar-nav-padding-x: 0;
  --bs-uu-sidebar-nav-disabled-color: $gray-600;
  --bs-uu-sidebar-nav-active-font-weight: 600;
  -->
