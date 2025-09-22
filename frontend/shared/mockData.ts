export type MockQuestionKey =
    | "processingRegistry"
    | "ethicalCommission"
    | "other";

export type LinkData = {
    text: string;
    url: string;
};
export type AnswerPart = string | LinkData;
type MockQuestions = Record<MockQuestionKey, Record<string, AnswerPart[]>>;
export const mockQuestions: MockQuestions = {
    processingRegistry: {
        "What is part of personal data?": [
            "Personal data is dat that tells something about a living person of whom you know the identity, from whom you can discern the identity or whom are otherwise recognizable. For example: contact information is personal data, but also a lot of research data is personal data. Measurement data, answers on a questionnaire, or interviews, observations, demographic data and much more. Data that can not be traced back to personal data are anonymous data, those are not personal data",
        ],
        "Why are bananas curved?": ["Because they are yellow."],
    },
    ethicalCommission: {
        "Where can i find the documents I have to deliver?": [
            "During the application it may be possible that you need submit certain documents. Use the most recent model documents.",
            {
                text: "Model Documents",
                url: "https://intranet.uu.nl/en/documents-ethics-assessment-committee-humanities",
            },
            "You can also find the links to the documents during the application itself.",
        ],
        "How long do responses take after submission?": ["No idea."],
        "What happens if my application gets rejected?": [
            "You will need to make a revision and resubmit the application.",
        ],
        "Help my draft application suddenly changed": [
            "It is possible for the supervisor to change your application.",
        ],
    },
    other: {
        "When will the Ethical Commission be added to to My Research?": [
            "After an estimated 2000 cups of coffee.",
        ],
        "Why am I looking at a picture of a cat?": ["https://cataas.com/cat"],
    },
};
