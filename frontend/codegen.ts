import type { CodegenConfig } from "@graphql-codegen/cli";
import * as dotenv from "dotenv";

dotenv.config();

let schema = `${process.env.NUXT_PUBLIC_API_URL}/graphql`;
if ("CODEGEN_SCHEMA" in process.env && process.env.CODEGEN_SCHEMA) {
    schema = process.env.CODEGEN_SCHEMA;
}

const config: CodegenConfig = {
    schema,
    documents: [
        "**/*.vue",
        "composables/*.ts",
        "stores/*.ts",
        "middleware/*.ts",
        "shared/validators/*.ts",
    ],
    ignoreNoDocuments: true, // for better experience with the watcher,
    generates: {
        "./generated/gql/": {
            preset: "client",
            config: {
                useTypeImports: true,
                nonOptionalTypename: true,
            },
        },
    },
};

export default config;
