<script setup lang="ts"></script>
<template>
  <div class="uu-content">
    <Title>{{ $t("MyResearch") }}</Title>
    <div class="uu-hero">
      <h1>{{ $t("Welcome to MyResearch!") }}</h1>
    </div>
    <div class="uu-sidebar-container uu-sidebar-right">
      <aside class="uu-sidebar">
        <RecentActivity />
      </aside>
      <div class="uu-sidebar-content">
        <div class="uu-container">
          {{
            $t(
              "My research is een tool dat onderzoekers helpt met het aanvragen van een onderzoek. " +
                "Op deze website kan uw onderzoek worden geregistreerd bij het verwerkingsregister en " +
                "een aanvraag kan worden gedaan bij de ethische commissie of uw onderzoek wel door de beugal kan. " +
                "Maar eerst is het de bedoeling dat een wegwijzer wordt ingevuld. Het kan namelijk zo zijn " +
                "dat uw onderzoek bepaalde aanvragen helemaal niet hoeft te doen. " +
                "Iets wat de wegwijzer samen met u uitzoekt.",
            )
          }}
        </div>
        <div class="uu-container">
          <h2>{{ $t("Verwerkingsregister") }}</h2>
          <p>
            {{
              $t(
                "Bij het verwerkingsregister start je de registratie van studies (onderzoeksprojecten) " +
                  "waarin er persoonsgegevens worden verwerkt. Het verwerkingsregister is een centraal " +
                  "overzicht van alle studies waarin persoonsgegevens een rol spelen. De Algemene Verordening " +
                  "Gegevensbescherming (AVG) eist dat dergelijke studies worden geregistreerd. Voor de onderzoeker z" +
                  "elf biedt het verwerkingsregister ook voordelen: het geeft op een gebruiksvriendelijke manier inzicht " +
                  "in allerlei aspecten van de gegevensverwerking, zoals de typen persoonsgegevens, de personen op wie die " +
                  "gegevens van toepassing zijn, de bewaartermijnen, de gebruikte software, de beveiligingsmaatregelen en " +
                  "de verschillende partijen die een rol spelen.",
              )
            }}
          </p>
        </div>
      </div>
    </div>
    <div class="uu-sidebar-container uu-sidebar-right">
      <div class="uu-sidebar-content">
        <h2 class="uu-sidebar-header-linked">Veelgestelde vragen</h2>
        <AccordionQuestions />
      </div>
      <aside class="uu-sidebar">
        <h2 class="uu-sidebar-header-linked">Contact</h2>
        <p>
          {{ $t("Voor vragen neem contact op met de privacy officier: ")
          }}<a href="mailto:l.j.w.m.kessels@uu.nl">l.j.w.m.kessels@uu.nl</a>
        </p>
        <p>
          {{ $t("Voor complimentjes neem contact op met: ")
          }}<a href="mailto:portaldev.gw@uu.nl">portaldev.gw@uu.nl</a>
        </p>
      </aside>
    </div>
  </div>
</template>
<style scoped></style>
