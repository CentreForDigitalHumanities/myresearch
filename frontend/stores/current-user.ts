import { defineStore } from "pinia";
import { useApolloClient } from "@vue/apollo-composable";
import { graphql } from "~/generated/gql";
import type { GetCurrentUserQuery } from "~/generated/gql/graphql";

export const useCurrentUserStore = defineStore("currentUser", () => {
  const currentUser = ref<GetCurrentUserQuery["currentUser"]>();

  async function loadData() {
    const { client } = useApolloClient();

    const GET_CURRENT_USER = graphql(`
      query getCurrentUser {
        currentUser {
          id
          username
          email
          fullName
          isStaff
        }
      }
    `);

    const result = await client.query({
      query: GET_CURRENT_USER,
    });

    currentUser.value = result.data.currentUser ?? undefined;
  }

  return { currentUser, loadData };
});
