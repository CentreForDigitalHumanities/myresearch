// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2025-05-15",
  devtools: { enabled: true },
  modules: ["@nuxt/eslint", "@nuxt/test-utils"],
  ssr: false,

  vite: {
    server: {
      watch: {
        // Necessary for HMR to pick up changes in the volume.
        usePolling: true,
      },
    },
    css: {
      devSourcemap: true,
    },
  },
  
  css: ["@/shared/main.scss"],

  app: {
    head: {
      charset: "utf-8",
      viewport: "width=device-width, initial-scale=1",
      meta: [],
      link: [
        {
          rel: "icon",
          type: "image/x-icon",
          href: "/static/favicon.ico",
        },
      ],
      style: [],
      script: [],
    },
  },
});
