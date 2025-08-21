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
            {
              id: "department",
              labelNl: "Departement",
              labelEn: "Department",
              type: "select",
              order: 2,
              options: [
                {
                  value: "gkg",
                  labelNl: "Geschiedenis en Kunstgeschiedenis",
                  labelEn: "History and Art History",
                },
                {
                  value: "tlc",
                  labelNl: "Talen, Literatuur en Communicatie",
                  labelEn: "Languages, Literature and Communication",
                },
                {
                  value: "mcw",
                  labelNl: "Media en Cultuurwetenschappen",
                  labelEn: "Media and Culture Studies",
                },
                {
                  value: "fnr",
                  labelNl: "Filosofie en Religiewetenschappen",
                  labelEn: "Philosophy and Religious Studies",
                },
              ],
            },
          ],
          sideConfig: {
            questions: [
              {
                textNl:
                  "Kan ik een faculteit invullen waarbij de eindverantwoordelijke niet werkzaam is?",
                textEn:
                  "Can I fill in a faculty where the responsible person is not employed?",
                link: "dummy",
              },
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
        questions: [
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
    {
      slug: "study-period",
      labelNl: "Studieperiode",
      labelEn: "Study period",
      stepNameNL: "Studieperiode",
      stepNameEN: "Study period",
      order: 2,
      descriptionNl:
        "Wanneer begin je met het verzamelen van persoonsgegevens en wanneer verwacht je de resultaten te publiceren?",
      descriptionEn:
        "When do you start collecting personal data and when do you expect to publish the results?",
      questions: [
        {
          id: "begin-date",
          labelNl: "Startdatum",
          labelEn: "Start date",
          descriptionNl:
            "Dit is de datum waarop begint met het verzamelen van persoonsgegevens.",
          descriptionEn: "This is the date you start collecting personal data.",
          type: "date",
          order: 1,
          required: true,
        },
        {
          id: "end-date",
          labelNl: "Einddatum",
          labelEn: "End date",
          descriptionNl:
            "Dit is de verwachte publicatiedatum van de onderzoeksresultaten. Op deze datum gaat de archiveringstermijn van de onderzoeksdata in.",
          descriptionEn:
            "This is the expected publication date of the research results. The archiving period for the research data starts on this date.",
          type: "date",
          order: 2,
          required: true,
        },
      ],
      sideConfig: {
        questions: [
          {
            textNl:
              "Wat gebeurt er als de hier opgegeven periode is verstreken?",
            textEn: "What happens when the specified period has expired?",
            link: "dummy",
          },
          {
            textNl: "Moet ik de archiveringsperiode meetellen?",
            textEn: "Do I need to include the archiving period?",
            link: "dummy",
          },
        ],
      },
    },
    {
      slug: "research-goal",
      labelNl: "Onderzoeksdoel",
      labelEn: "Research goal",
      stepNameNL: "Onderzoeksdoel",
      stepNameEN: "Research goal",
      order: 3,
      sideConfig: {
        questions: [
          {
            textNl: "Wat wordt bedoeld met onderzoeksdoel?",
            textEn: "What is meant by research goal?",
            link: "dummy",
          },
          {
            textNl: "Kan ik ook meerdere doelen opgeven?",
            textEn: "Can I also specify multiple goals?",
            link: "dummy",
          },
        ],
        extraInfo: [
          {
            textNl:
              "Persoonsgegevens mogen alleen worden verwerkt als daarmee minimaal één specifiek, welomschreven doel wordt gediend. Met deze vraag gaan we na wat het onderzoeksdoel is. Mocht je onderzoek meerdere doelen hebben, voeg dan velden toe met behulp van de knop onder het invoerveld.  Bij wetenschappelijk onderzoek is het niet altijd mogelijk om vooraf precies met zekerheid aan te geven dat de persoonsgegevens niet voor een enigszins ander doel gebruikt gaan worden. Het doel kan in de loop van je onderzoek namelijk verschuiven, bijvoorbeeld op basis van de voorlopige resultaten. Is hiervan sprake, kom dan in de toekomst terug naar deze tool en pas het antwoord op deze vraag aan.",
            textEn:
              "Personal data may only be processed if at least one specific, well-defined purpose is served. With this question, we will examine what the research goal is. If your research has multiple goals, please add fields using the button below the input field. In scientific research, it is not always possible to indicate in advance with certainty that the personal data will not be used for a somewhat different purpose. The purpose may shift during the course of your research, for example based on preliminary results. If this is the case, please return to this tool in the future and adjust your answer to this question.",
          },
        ],
      },
      questions: [
        {
          type: "text",
          id: "research-goal",
          labelNl: "Wat is het doel van je onderzoek?",
          labelEn: "What is the goal of your research?",
          placeholderNl: "Onderzoeksdoel",
          placeholderEn: "Research goal",
          order: 1,
          lines: 5,
          required: true,
        },
      ],
    },
  ],
};
