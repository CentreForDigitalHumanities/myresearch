<script lang="ts" setup>
import type { GetStudyTitleQuery } from "~/generated/gql/graphql";

type QueriedStudy = NonNullable<GetStudyTitleQuery["study"]>;

defineProps<{
    study: QueriedStudy;
}>();
</script>

<template>
    <Title>{{ study.reference }} - {{ study.title }}</Title>
    <div class="uu-hero">
        <h1 class="text-wrap text-break">
            {{ study.reference }} -
            {{ study.title }}
        </h1>
    </div>
</template>
