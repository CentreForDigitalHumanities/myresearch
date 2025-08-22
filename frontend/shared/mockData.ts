import { i18n } from "~/plugins/i18n";
const { t } = i18n.global;

const questionOneProcessingRegister = t("What is part of personal data?");
const answerOneProcessingRegister = t(
  "Persoonsgegevens zijn gegevens die iets zeggen over een levende persoon van wie je de identiteit weet, van wie " +
    "je de identiteit te weten kunt komen of die je op een andere manier kunt herkennen. Bijvoorbeeld: contactgegevens " +
    "zijn persoonsgegevens, maar ook veel onderzoeksgegevens zijn persoonsgegevens. Denk aan meetgegevens, antwoorden " +
    "op vragen in een vragenlijst of interview, observaties, demografische gegevens etc. Let op: Gegevens die op geen " +
    "enkele manier meer zijn te koppelen aan een bepaalde persoon, zijn anonieme gegevens. Dit zijn géén persoonsgegevens.",
);
const questionTwoProcessingRegister = t("Waarom zijn bananen krom?");
const answerTwoProcessingRegister = t(
  "Omdat ze anders niet in hun schil passen",
);
const questionOneEthnicalCommission = t(
  "Where can i find the documents I have to deliver",
);
const answerOneEthnicalCommission = t(
  "Tijdens de aanvraagprocedure kan er om een of meer bijlagen worden gevraagd. Gebruik daarvoor de juiste (meest recente) voorbeelddocumenten " +
    useEthicsLinks("model_documents"),
  //TODO creating a href here is ugly and hard to do, but i still need a link here, give the logic to ethicsLinks?
  // still very ugly but it only has to happen one time, also vue refus    questionOneEthnicalCommission,
  // questionTwoEthnicalCommission,es <a /> tags?
);
const questionTwoEthnicalCommission = t("How long do responses take");
const answerTwoEthnicalCommission = t("Geen idee");
const questionThreeEthnicalCommission = t(
  "What happens if my application gets rejected",
);
const answerThreeEthnicalCommission = t("you modify it until it gets accepted");
const questionFourEthnicalCommission = t(
  "Help my draft application suddenly changed",
);
const answerFourEthnicalCommission = t(
  "it is possible for the supervisor to change your application",
);

export class mockData {
  //if this becomes the permanent location than we can make this more dynamic
  //with same setup as in useEthicsLinks.ts, saves extending the if statement.

  static questionsProcessingRegister: string[] = [
    questionOneProcessingRegister,
    questionTwoProcessingRegister,
  ];
  static answersProcessingRegister = [
    answerOneProcessingRegister,
    answerTwoProcessingRegister,
  ];
  static questionsEthicalCommission = [
    questionTwoProcessingRegister,
    questionOneEthnicalCommission,
    questionTwoEthnicalCommission,
    questionThreeEthnicalCommission,
    questionFourEthnicalCommission,
  ];
  static answersEthicalCommission = [
    answerTwoProcessingRegister,
    answerOneEthnicalCommission,
    answerTwoEthnicalCommission,
    answerThreeEthnicalCommission,
    answerFourEthnicalCommission,
  ];
}
