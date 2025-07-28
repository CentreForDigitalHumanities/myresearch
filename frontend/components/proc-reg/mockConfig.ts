import type { FormConfig } from "./types";

export const mockVwr: FormConfig = {
  labelNl: "Verwerkingsregister",
  labelEn: "Processing Registry",
  steps: [
    {
      slug: "study-name",
      labelNl: "De naam van je studie",
      labelEn: "The name of your study",
      stepNameNL: "Studienaam",
      stepNameEN: "Study name",
      order: 1,
      questions: [
        {
          id: "study-name-question",
          labelNl: "Studienaam",
          labelEn: "Study name",
          type: "text",
          order: 1,
          required: true,
          placeholderNl: "Studienaam",
          placeholderEn: "Study name",
        },
      ],
      substeps: [
        {
          slug: "study-contributors",
          labelNl: "Betrokken onderzoekers",
          labelEn: "Involved researchers",
          stepNameNL: "Betrokken onderzoekers",
          stepNameEN: "Involved researchers",
          order: 1,
          questions: [
            {
              id: "responsible",
              labelNl:
                "Wie is er binnen de UU de eindverantwoordelijke voor de studie?",
              labelEn: "Who is ultimately responsible for the study at UU?",
              type: "text",
              order: 1,
              placeholderNl: "E-mailadres",
              placeholderEn: "Email address",
              required: true,
            },
            {
              id: "other-contributors",
              order: 2,
              labelNl: "Wie werkt er binnen de UU nog meer mee aan de studie?",
              labelEn: "Who else at UU is involved in the study?",
              type: "text",
              placeholderNl: "E-mailadres",
              placeholderEn: "Email address",
              required: false,
            },
          ],
        },
        {
          slug: "faculty",
          labelNl: "Faculteit",
          labelEn: "Faculty",
          stepNameNL: "Faculteit",
          stepNameEN: "Faculty",
          descriptionNl:
            "Selecteert de faculteit waarbinnen het onderzoek plaatsvindt, of de faculteit die optreedt als penvoerder.",
          descriptionEn:
            "Select the faculty where the research takes place, or the faculty that acts as the lead.",
          order: 2,
          questions: [
            {
              id: "faculty",
              labelNl: "Faculteit",
              labelEn: "Faculty",
              type: "select",
              order: 1,
              options: [
                {
                  value: "GW",
                  labelNl: "Faculteit Geesteswetenschappen",
                  labelEn: "Faculty of Humanities",
                },
                {
                  value: "REBO",
                  labelNl: "Faculteit Recht, Economie, Bestuur en Organisatie",
                  labelEn: "Faculty of Law, Economics and Governance",
                },
              ],
              required: true,
            },
          ],
          sideConfig: {
            titleNl: "Vragen?",
            titleEn: "Questions?",
            paragraphs: [
              {
                textNl:
                  "Kan ik een faculteit invullen waarbij de eindverantwoordelijke niet werkzaam is?",
                textEn:
                  "Can I fill in a faculty where the responsible person is not employed?",
                link: "dummy",
              },
              {
                textNl: "Wat moet ik hier invullen?",
                textEn: "What should I fill in here?",
                link: "dummy",
              },
              {
                textNl:
                  "Wat als een studie door meerdere departementen wordt uitgevoerd?",
                textEn: "What if a study is conducted by multiple departments?",
                link: "dummy",
              },
            ],
          },
        },
      ],
      sideConfig: {
        titleNl: "Vragen?",
        titleEn: "Questions?",
        paragraphs: [
          {
            textNl: "Wat wordt er bedoeld met een studie?",
            textEn: "What is meant by a study?",
            link: "dummy",
          },
          {
            textNl: "Wordt de naam die ik opgeef vaker gebruikt?",
            textEn: "Will the name I provide be used more often?",
            link: "dummy",
          },
          {
            textNl: "Wat gebeurt er met de informatie die ik invoer?",
            textEn: "What happens to the information I enter?",
            link: "dummy",
          },
          {
            textNl:
              "Ik heb deze naam al ergens anders opgegeven. Waarom moet ik dit nog een keer doen?",
            textEn:
              "I have already provided this name elsewhere. Why do I need to do this again?",
            link: "dummy",
          },
        ],
      },
    },
  ],
};
