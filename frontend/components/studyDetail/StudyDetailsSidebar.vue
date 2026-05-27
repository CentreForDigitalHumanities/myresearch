<script setup lang="ts">
import type { GetStudyQuery } from "~/generated/gql/graphql";

defineProps<{
    study: NonNullable<GetStudyQuery["study"]>;
}>();

function formatDate(date: string) {
    const split = date.split(/[T.]/);
    return split[0] + ", " + split[1]
}
</script>

<template>
    <aside class="uu-sidebar">
        <button
            class="uu-sidebar-toggle"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#exampleSidebar"
            aria-expanded="false"
        >
            {{ $t("Show sidebar") }}
        </button>
        <div id="exampleSidebar" class="uu-sidebar-collapse collapse">
            <h3>{{ $t("Creator details") }}</h3>
            <ul>
                <li class="mt-2">
                    {{ $t("Created by") }}:
                    {{ study.createdBy.fullName }}
                </li>
                <li class="mt-2">
                    {{ $t("Creator email") }}:
                    {{ study.createdBy.email }}
                </li>
            </ul>
            <h3>{{ $t("Study details") }}</h3>
            <ul>
                <li class="mt-2">
                    {{ $t("Created on") }}:
                    {{ formatDate(study.createdAt) }}
                </li>
                <li class="mt-2">
                    {{ $t("Submitted on") }}:
                    {{ formatDate(study.updatedAt) }}
                </li>
            </ul>
        </div>
    </aside>
</template>
