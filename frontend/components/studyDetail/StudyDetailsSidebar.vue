<script setup lang="ts">
import type { GetStudyQuery } from "~/generated/gql/graphql";
import { i18n } from "~/plugins/i18n";

interface Props {
    study: NonNullable<GetStudyQuery["study"]>;
}
const props = defineProps<Props>();

const timeFormat: Intl.DateTimeFormatOptions = { month: 'long', day: 'numeric', year: 'numeric', hour: 'numeric', minute: 'numeric'}
function toLocalDate(isoString: string) {
    return new Date(isoString).toLocaleTimeString(i18n.global.locale.value, timeFormat)
}
const createdAt = computed(() => toLocalDate(props.study.createdAt));
const updatedAt = computed(() => toLocalDate(props.study.updatedAt));
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
                    {{ createdAt }}
                </li>
                <li class="mt-2">
                    {{ $t("Submitted on") }}:
                    {{ updatedAt }}
                </li>
            </ul>
        </div>
    </aside>
</template>
