<script setup lang="ts">
import { useQuery } from "@vue/apollo-composable";
import { graphql } from "~/generated/gql";
import type { GetNoteQuery } from "~/generated/gql/graphql";
import { useStepSlug } from "~/composables/useRouteParams";
definePageMeta({
    public: true,
});

const GET_NOTE = graphql(`
    query getNote($slug: ID!) {
        note(slug: $slug) {
            titleNl
            titleEn
            contentEn
            contentNl
        }
    }
`);

const slug = useStepSlug();

const { result: noteResult } = useQuery<GetNoteQuery>(GET_NOTE, () => ({
    slug: slug.value,
}));
const note = computed(() => noteResult.value?.note ?? null);
</script>

<template>
    <div v-if="note" class="uu-content">
        <div class="uu-hero">
            <h1>{{ useTranslateableAttribute(note, "title") }}</h1>
        </div>
        <div class="uu-container">
            <div
                class="col-9"
                v-html="useTranslateableAttribute(note, 'content')"
            ></div>
        </div>
    </div>
</template>
