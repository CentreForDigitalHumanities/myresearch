import {
    ApolloError,
    type OperationVariables,
    type TypedDocumentNode,
} from "@apollo/client/core";
import { useQuery } from "@vue/apollo-composable";
import type { Ref } from "vue";
import type {
    OptionsParameter,
    VariablesParameter,
    // @ts-expect-error - types not explicitly exported by the package
} from "@vue/apollo-composable/dist/useQuery";

interface PerformQueryInputWithVariables<
    Query,
    Variables extends OperationVariables
> {
    queryDocument: TypedDocumentNode<Query, Variables>;
    errorMessage?: string;
    variables: VariablesParameter<Variables>;
    options?: OptionsParameter<Query, Variables>;
}

interface PerformQueryInputWithoutVariables<Query> {
    queryDocument: TypedDocumentNode<Query, Record<string, never>>;
    errorMessage?: string;
    options?: OptionsParameter<Query, Record<string, never>>;
}

type PerformQueryInput<Query, Variables extends OperationVariables> =
    | PerformQueryInputWithVariables<Query, Variables>
    | PerformQueryInputWithoutVariables<Query>;

interface PerformQueryReturn<Query, Variables extends OperationVariables> {
    result: Ref<Query | undefined>;
    loading: Ref<boolean>;
    variables: Ref<Variables | undefined>;
}

/**
 * A wrapper around Apollo's `useQuery` hook that takes care of error handling.
 * @template Query - The expected shape of the query result.
 * @template Variables - The expected shape of the query variables.
 * @param {PerformQueryInput<Query, Variables>} input - An object containing the query document, error message, and variables.
 * @returns {PerformQueryReturn<Query>} An object containing the query result and loading state.
 */
function usePerformQuery<Query, Variables extends OperationVariables>(
    input: PerformQueryInput<Query, Variables>,
    onError: (e: ApolloError) => void | undefined
): PerformQueryReturn<Query, Variables> {
    const { queryDocument, errorMessage } = input;

    let queryResult: Ref<Query | undefined> | null = null;
    let queryError: Ref<ApolloError | null> | null = null;
    let queryLoading: Ref<boolean> | null = null;
    let queryVariables: Ref<Variables | undefined> = ref(undefined);

    if ("variables" in input) {
        const { result, error, loading, variables } = useQuery<
            Query,
            Variables
        >(queryDocument, input.variables, input.options ?? {});
        queryResult = result;
        queryError = error;
        queryLoading = loading;
        queryVariables = variables;
    } else {
        const { result, error, loading } = useQuery<Query>(
            queryDocument,
            null,
            input.options ?? {}
        );
        queryResult = result;
        queryError = error;
        queryLoading = loading;
    }

    watch(queryError, () => {
        if (queryError?.value) {
            onError(queryError.value)
        }
    });
    return {
        result: queryResult,
        loading: queryLoading,
        variables: queryVariables,
    };
}

export { usePerformQuery };
