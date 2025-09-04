const questionOneProcessingRegister = "What is part of personal data?";
const answerOneProcessingRegister =
  "Personal data is dat that tells something about a living person of whom you know the identity, from whom you can discern the identity or whom are otherwise recognizable. For example: contact information is personal data, but also a lot of research data is personal data. Measurement data, answers on a questionnaire, or interviews, observations, demographic data and much more. Data that can not be traced back to personal data are anonymous data, those are not personal data";
const questionTwoProcessingRegister = "Waarom zijn bananen krom?";
const answerTwoProcessingRegister = "Because they are yellow";
const questionOneEthnicalCommission =
  "Where can i find the documents I have to deliver";
const answerOneEthnicalCommission =
  "Tijdens de aanvraagprocedure kan er om een of meer bijlagen worden gevraagd. Gebruik daarvoor de juiste (meest recente) voorbeelddocumenten " +
  useEthicsLinks("model_documents");
const questionTwoEthnicalCommission = "How long do responses take";
const answerTwoEthnicalCommission = "Geen idee";
const questionThreeEthnicalCommission =
  "What happens if my application gets rejected";
const answerThreeEthnicalCommission = "you modify it until it gets accepted";
const questionFourEthnicalCommission =
  "Help my draft application suddenly changed";
const answerFourEthnicalCommission =
  "it is possible for the supervisor to change your application";

let processingQuestionAnswers = new Map<string, string>();
processingQuestionAnswers.set(
  questionOneProcessingRegister,
  answerOneProcessingRegister,
);
processingQuestionAnswers.set(
  questionTwoProcessingRegister,
  answerTwoProcessingRegister,
);

let ethicalCommissionQuestionAnswers = new Map<string, string>();
ethicalCommissionQuestionAnswers.set(
  questionOneEthnicalCommission,
  answerOneEthnicalCommission,
);
ethicalCommissionQuestionAnswers.set(
  questionTwoEthnicalCommission,
  answerTwoEthnicalCommission,
);
ethicalCommissionQuestionAnswers.set(
  questionThreeEthnicalCommission,
  answerThreeEthnicalCommission,
);
ethicalCommissionQuestionAnswers.set(
  questionFourEthnicalCommission,
  answerFourEthnicalCommission,
);

let questionAnswers = new Map<string, Map<string, string>>();
questionAnswers.set("processingRegister", processingQuestionAnswers);
questionAnswers.set("ethicalCommission", ethicalCommissionQuestionAnswers);

export class mockData {
  static getQuestionAnswers(
    questionsGroup: string,
  ): Map<string, string> | undefined {
    return questionAnswers.get(questionsGroup);
  }
}
