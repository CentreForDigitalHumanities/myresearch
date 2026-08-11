<script lang="ts" setup>
import type { GetStudyTitleQuery } from "~/generated/gql/graphql";

type QueriedStudy = NonNullable<GetStudyTitleQuery["study"]>;

defineProps<{
    study: QueriedStudy | null;
}>();
</script>

<template>
    <Title v-if="study">{{ study.reference }} - {{ study.title }}</Title>
    <Title v-else>{{ $t("Registration Overview") }}</Title>

    <div class="uu-hero">
        <h1 v-if="study" class="text-wrap text-break">
            {{ study.reference }} -
            {{ study.title }}
        </h1>
        <h1 v-else>{{ $t("Registration overview") }}</h1>
    </div>
</template>
