import { i18n } from "~/plugins/i18n";
const { t } = i18n.global;

const questionOne_verwerkingsregister = "What is part of personal data?";
const questionTwo_verwerkingsregister = "Waarom zijn bananen krom?";
const answerOne_verwerkingsregister =
  "Persoonsgegevens zijn gegevens die iets zeggen over een levende persoon van wie je de identiteit weet, van wie " +
  "je de identiteit te weten kunt komen of die je op een andere manier kunt herkennen. Bijvoorbeeld: contactgegevens " +
  "zijn persoonsgegevens, maar ook veel onderzoeksgegevens zijn persoonsgegevens. Denk aan meetgegevens, antwoorden " +
  "op vragen in een vragenlijst of interview, observaties, demografische gegevens etc. Let op: Gegevens die op geen " +
  "enkele manier meer zijn te koppelen aan een bepaalde persoon, zijn anonieme gegevens. Dit zijn géén persoonsgegevens.";
const answerTwo_verwerkingsregister =
  "Omdat ze anders niet in hun schil passen";

export class mockData {
  static questionsVerwerkingsregister: string[] = [
    t(questionOne_verwerkingsregister),
    t(questionTwo_verwerkingsregister),
  ];
  static answersVerwerkingsregister = [
    t(answerOne_verwerkingsregister),
    t(answerTwo_verwerkingsregister),
  ];
  static questionsEthicalCommission = [t(questionTwo_verwerkingsregister)];
  static answersEthicalCommission = [t(answerTwo_verwerkingsregister)];
}
