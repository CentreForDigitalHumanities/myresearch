<script lang="ts" setup>
import { graphql } from "~/generated/gql";

const GET_FORM = graphql(`
    query GetForm {
        form {
            id
            nameEn
            nameNl
            descriptionEn
            descriptionNl
            steps {
                ...StepFragment
                formOrder
                substeps {
                    ...StepFragment
                    parentOrder
                }
            }
        }
    }
`);

const { result: formResult } = usePerformQuery({
    queryDocument: GET_FORM,
});

const form = computed(() => formResult.value?.form ?? null);
</script>

<template>
    <div class="uu-content">
        <Title>{{ $t("Processing Registry") }}</Title>
        <div class="uu-hero">
            <h1>{{ $t("Processing Registry") }}</h1>
        </div>
        <div class="uu-container">
            <SharedMRForm v-if="form" :form="form" />
        </div>
    </div>
</template>
