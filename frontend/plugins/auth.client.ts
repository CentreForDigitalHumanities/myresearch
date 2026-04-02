export default defineNuxtPlugin(() => {
    addRouteMiddleware(
        "global-auth",
        async (to, from) => {
            // Check if page is marked as public
            if (to.meta.public) {
                return;
            }

            const config = useRuntimeConfig();

            async function rerouteToLogin(): Promise<void> {
                // Using the Dev-IDP the redirect seems to get overriden
                // Maybe this can be fixed on PROD
                const redirect = encodeURIComponent(window.location.href);
                const loginUrl = `${config.public.SAML_URL}/login/?next=${redirect}`;
                await navigateTo(loginUrl, { external: true });
            }

            const currentUserStore = useCurrentUserStore();

            // If currentUser is not loaded, try to load it
            if (!currentUserStore.currentUser) {
                try {
                    await currentUserStore.loadData();
                } catch (error) {
                    await rerouteToLogin();
                    return false;
                }
            }

            // Additional check: verify user has an ID (is authenticated)
            if (!currentUserStore.currentUser?.id) {
                await rerouteToLogin();
                return false;
            }
        },
        { global: true },
    );
});
