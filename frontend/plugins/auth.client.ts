export default defineNuxtPlugin(() => {
    addRouteMiddleware(
        'global-auth',
        async (to, from) => {
            
            // Check if page is marked as public
            if (to.meta.public) {
                return;
            }

            const config = useRuntimeConfig();

            const getLoginUrl = () => {
                const redirect = encodeURIComponent(window.location.href);
                return `${config.public.SAML_URL}/login/?next=${redirect}`;
            };

            const currentUserStore = useCurrentUserStore();
            
            // If currentUser is not loaded, try to load it
            if (!currentUserStore.currentUser) {
                try {
                    await currentUserStore.loadData();
                } catch (error) {
                    // If loading fails, redirect to login
                    if (process.client) {
                        const loginUrl = getLoginUrl();
                        window.location.href = loginUrl;
                    }
                    return;
                }
            }
            
            // Additional check: verify user has an ID (is authenticated)
            if (!currentUserStore.currentUser?.id) {
                if (process.client) {
                    const loginUrl = getLoginUrl();
                    window.location.href = loginUrl;
                    // Prevent page render while redirecting
                    return false;
                }
            }
            
        },
        { global: true }
    );
});
