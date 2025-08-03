# Nuxt Minimal Starter

Look at the [Nuxt documentation](https://nuxt.com/docs/getting-started/introduction) to learn more.

## Setup

Make sure to install dependencies:

```bash
# npm
npm install

# pnpm
pnpm install

# yarn
yarn install

# bun
bun install
```

## Development Server

Start the development server on `http://localhost:3000`:

```bash
# npm
npm run dev

# pnpm
pnpm dev

# yarn
yarn dev

# bun
bun run dev
```

## Production

Build the application for production:

```bash
# npm
npm run build

# pnpm
pnpm build

# yarn
yarn build

# bun
bun run build
```

Locally preview production build:

```bash
# npm
npm run preview

# pnpm
pnpm preview

# yarn
yarn preview

# bun
bun run preview
```

Check out the [deployment documentation](https://nuxt.com/docs/getting-started/deployment) for more information.

## Internationalization

Internationalization is implemented using the `vue-i18n` package. The message files are in the `locales` subdirectory.

To extract new messages from the source code, run the `vue-i18n-extract` tool:

```bash
npm run i18n-extract
```

This tool adds missing keys with an initial empty string as values. (A newer version of `vue-i18n-extract` includes
an option to use `null` as initial value instead, but there is no release for this yet as of July 2025.)

To check whether there are no missing keys **and** all messages have been translated, run:

```bash
npm run i18n-check
```
