import {
    type FrequentAnswer,
    type FrequentQuestionKey,
} from "~/components/frontpage/FrequentQuestions.vue";

type MockQuestions = Record<
    FrequentQuestionKey,
    Record<string, FrequentAnswer>
>;

export const mockQuestions: MockQuestions = {
    processingRegistry: {
        "What is part of personal data?": {
            text: "Personal data are data that tells something about a living person whose identity you know or can be discovered, or who is otherwise recognisable. Contact details are personal data, but data obtained through research (measurements, questionnaires, interviews, observations etc.) may count as personal data as well. Data that cannot be traced back to an individual are anonymous data. These are not considered personal data",
            url: null,
            image: null,
        },
        "Why are bananas curved?": {
            text: "Because they are yellow.",
            url: null,
            image: null,
        },
    },
    ethicalCommission: {
        "Where can I find the documents that I have to submit?": {
            text: "During the application you may need to submit certain documents. Use the most recent model documents. You can also find the links to the documents during the application itself.",
            url: null,
            image: null,
        },
        "Model documents": {
            text: "Model documents",
            url: "https://intranet.uu.nl/en/documents-ethics-assessment-committee-humanities",
            image: null,
        },
        "How long does it take to receive a reply after submitting?": {
            text: "No idea.",
            url: null,
            image: null,
        },

        "What happens if my application gets rejected?": {
            text: "You will need to revise and resubmit the application.",
            url: null,
            image: null,
        },

        "Why did my draft application suddenly change?": {
            text: "It is possible for the supervisor to change your application.",
            url: null,
            image: null,
        },
    },
    other: {
        "When will the Ethical Commission be added to to MyResearch?": {
            text: "After an estimated 2000 cups of coffee.",
            url: null,
            image: null,
        },

        "Why am I looking at a picture of a cat?": {
            text: null,
            url: null,
            image: {
                src: "https://cataas.com/cat",
                altText: "My cat is gone",
            },
        },
    },
};
