const questionOneProcessingRegister = "What is part of personal data?";
const answerOneProcessingRegister =
  "Personal data is dat that tells something about a living person of whom you know the identity, from whom you can discern the identity or whom are otherwise recognizable. For example: contact information is personal data, but also a lot of research data is personal data. Measurement data, answers on a questionnaire, or interviews, observations, demographic data and much more. Data that can not be traced back to personal data are anonymous data, those are not personal data";
const questionTwoProcessingRegister = "Why are bananas curved?";
const answerTwoProcessingRegister = "Because they are yellow";
const questionOneEthnicalCommission =
  "Where can i find the documents I have to deliver";
const answerOneEthnicalCommission =
  "During the application it may be possible that you need submit certain documents. Use the most recent model documents. " +
  useEthicsLinks("model_documents");
const questionTwoEthnicalCommission =
  "How long do responses take after submission?";
const answerTwoEthnicalCommission = "No idea";
const questionThreeEthnicalCommission =
  "What happens if my application gets rejected? ";
const answerThreeEthnicalCommission =
  "You will need to make a revision and resubmit the application. ";
const questionFourEthnicalCommission =
  "Help my draft application suddenly changed";
const answerFourEthnicalCommission =
  "It is possible for the supervisor to change your application. ";

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

let otherQuestionAnswers = new Map<string, string>();
otherQuestionAnswers.set(
  "When will the Ethical Commission be added to to My Research?",
  "After an estimated 2000 cups of coffee.",
);
otherQuestionAnswers.set(
  "Why am I looking at a picture of a cat?",
  "https://cataas.com/cat", //unable to display cat links in accordion, a disappointment.
);

let questionAnswers = new Map<string, Map<string, string>>();
questionAnswers.set("processingRegister", processingQuestionAnswers);
questionAnswers.set("ethicalCommission", ethicalCommissionQuestionAnswers);
questionAnswers.set("other", otherQuestionAnswers);

export class mockData {
  static getQuestionAnswers(
    questionsGroup: string,
  ): Map<string, string> | undefined {
    return questionAnswers.get(questionsGroup);
  }
}
