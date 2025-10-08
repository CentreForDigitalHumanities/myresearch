import {
    type Answer,
    type FrequentQuestionKey,
} from "~/components/frontpage/FrequentQuestions.vue";

type MockQuestions = Record<FrequentQuestionKey, Record<string, Answer>>;
export const mockQuestions: MockQuestions = {
    processingRegistry: {
        "What is part of personal data?": [
            "Personal data are data that tells something about a living person whose identity you know or can be discovered, or who is otherwise recognisable. Contact details are personal data, but data obtained through research (measurements, questionnaires, interviews, observations etc.) may count as personal data as well. Data that cannot be traced back to an individual are anonymous data. These are not considered personal data",
        ],
        "Why are bananas curved?": ["Because they are yellow."],
    },
    ethicalCommission: {
        "Where can I find the documents that I have to submit?": [
            "During the application you may need to submit certain documents. Use the most recent model documents.",
            {
                text: "Model documents",
                url: "https://intranet.uu.nl/en/documents-ethics-assessment-committee-humanities",
            },
            "You can also find the links to the documents during the application itself.",
        ],
        "How long does it take to receive a reply after submitting?": ["No idea."],
        "What happens if my application gets rejected?": [
            "You will need to revise and resubmit the application.",
        ],
        "Why did my draft application suddenly change?": [
            "It is possible for the supervisor to change your application.",
        ],
    },
    other: {
        "When will the Ethical Commission be added to to My Research?": [
            "After an estimated 2000 cups of coffee.",
        ],
        "Why am I looking at a picture of a cat?": [
            {
                imageUrl: "https://cataas.com/cat",
                altText: "My cat is gone",
            },
        ],
    },
};
