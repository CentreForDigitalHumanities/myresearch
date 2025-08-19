<script setup lang="ts"></script>
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
      <aside class="uu-sidebar">
        <RecentActivity />
      </aside>
    </div>
    <div class="uu-sidebar-container uu-sidebar-right">
      <div class="uu-sidebar-content">
        <h2 class="uu-sidebar-header-linked">
          {{ $t("Processing register") }}
        </h2>
        <p>
          {{ $t("english_verwerkingsregister_uitleg") }}
        </p>
      </div>
      <aside class="uu-sidebar">
        <!-- TODO make sticky, see uu-bootstrap -->
        <h2 class="uu-sidebar-header-linked">{{ $t("Frequent questions") }}</h2>
        <FrequentQuestions QuestionsGroup="processingRegister" />
      </aside>
    </div>
    <div class="uu-sidebar-container uu-sidebar-right">
      <div class="uu-sidebar-content">
        <h2 class="uu-sidebar-header-linked">
          {{ $t("Ethical commission") }}
        </h2>
        <p>
          {{ $t("english_ethical_commission_uitleg") }}
        </p>
      </div>
      <aside class="uu-sidebar">
        <h2 class="uu-sidebar-header-linked">{{ $t("Frequent questions") }}</h2>
        <!-- TODO sidebar header linked does not work on the aside side, does work on the uu example site -->
        <FrequentQuestions QuestionsGroup="ethicalCommission" />
      </aside>
    </div>
    <div class="uu-sidebar-container uu-sidebar-right">
      <div class="uu-sidebar-content">
        <h2 class="uu-sidebar-header-linked">{{ $t("Other questions") }}</h2>
        <FrequentQuestions />
        <!--        <Bootstrapaccordian />-->
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
