<script setup lang="ts">
import type { GetStudyQuery } from "~/generated/gql/graphql";

defineProps<{
    study: GetStudyQuery["study"] | null;
    randomDatePastYear: string;
}>();
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
                    {{ study?.createdBy.fullName }}
                </li>
                <li class="mt-2">
                    {{ $t("Creator email") }}:
                    {{ study?.createdBy.email }}
                </li>
            </ul>
            <h3>{{ $t("Study details") }}</h3>
            <ul>
                <li class="mt-2">
                    {{ $t("Created on") }}: {{ randomDatePastYear }}
                </li>
                <li class="mt-2">
                    {{ $t("Submitted on") }}: {{ randomDatePastYear }}
                </li>
            </ul>
        </div>
    </aside>
</template>
