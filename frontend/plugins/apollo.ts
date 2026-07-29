import { DefaultApolloClient } from "@vue/apollo-composable";
import {
    ApolloClient,
    ApolloLink,
    HttpLink,
    InMemoryCache,
} from "@apollo/client/core";
import { removeTypenameFromVariables } from "@apollo/client/link/remove-typename";
import { loadDevMessages, loadErrorMessages } from "@apollo/client/dev";
import { defineNuxtPlugin } from "#app";
import { useRuntimeConfig } from "#imports";

export const apolloClient = new ApolloClient({
    cache: new InMemoryCache(),
});

function getCsrfToken(): string | null {
    const csrfCookie = useCookie("csrftoken");
    return csrfCookie.value ?? null;
}

export default defineNuxtPlugin((nuxtApp) => {
    // We can only access runtime config inside this function, so we setup the
    // link here
    const GRAPHQL_URL = useRuntimeConfig().public.API_URL + "/graphql";

    const removeTypenameLink = removeTypenameFromVariables();
    const httpLink = new HttpLink({
        uri: GRAPHQL_URL,
        credentials: "include", // This tells Apollo to send our auth cookies
        headers: {
            "X-CSRFToken": getCsrfToken() ?? "",
        },
    });
    const linkChain = ApolloLink.from([removeTypenameLink, httpLink]);

    apolloClient.setLink(linkChain);

    nuxtApp.vueApp.provide(DefaultApolloClient, apolloClient);

    if (import.meta.dev) {
        // Adds messages only in a dev environment
        loadDevMessages();
        loadErrorMessages();
    }
});
