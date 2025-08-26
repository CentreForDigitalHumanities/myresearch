import { i18n } from "~/plugins/i18n";
const { t } = i18n.global;

const questionOneProcessingRegister = t("What is part of personal data?");
const answerOneProcessingRegister = t(
  "Personal data is dat that tells something about a living person of whom you know the identity, from whom you can discern the identity or whom are otherwise recognizable. For example: contact information is personal data, but also a lot of research data is personal data. Measurement data, answers on a questionnaire, or interviews, observations, demographic data and much more. Data that can not be traced back to personal data are anonymous data, those are not personal data",
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
