import type { ComputedRef } from 'vue';

function useStudyId(): ComputedRef<string | undefined> {
    const route = useRoute();
    return computed(() => coerceArrayToString(route.params.study_id));
}

function useSubmissionId(): ComputedRef<string | undefined> {
    const route = useRoute();
    return computed(() => coerceArrayToString(route.params.submission_id));
}

function useStepSlug(): ComputedRef<string | undefined> {
    const route = useRoute();
    return computed(() => coerceArrayToString(route.params.slug));
}

/**
 * Helper function to make sure we always get a string from the route params if
 * the param is defined, even if it is an array.
 * 
 * For some reason the type checker does not think undefined is a possible
 * value for the param, so we explicitly add it here.
 */
function coerceArrayToString(
    param: string | string[] | undefined,
): string | undefined {
    if (Array.isArray(param)) {
        return param[0];
    }
    return param;
}

export { useStudyId, useSubmissionId, useStepSlug };
