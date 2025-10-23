import { defineStore } from "pinia";
import { useApolloClient } from "@vue/apollo-composable";
import { graphql } from "~/generated/gql";

interface State {
    currentUser?: any;
}

export const useCurrentUserStore = defineStore("currentUser", {
    state: (): State => {
        return {
            currentUser: undefined,
        };
    },
    actions: {
        async loadData() {
            const { client } = useApolloClient();

            const GET_CURRENT_USER = graphql(`
                query getCurrentUser {
                    currentUser {
                        id
                        username
                        email
                        fullName
                    }
                }
            `);

            const result = await client.query({
                query: GET_CURRENT_USER,
            });

            this.currentUser = result.data.currentUser ?? undefined;
        },
    },
});
