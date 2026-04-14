export function useOverviewStepSlug(): string {
    const config = useRuntimeConfig();
    return config.public.overviewStepSlug;
}