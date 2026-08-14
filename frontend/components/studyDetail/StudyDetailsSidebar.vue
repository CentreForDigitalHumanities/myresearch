<script setup lang="ts">
import type { GetStudyQuery } from "~/generated/gql/graphql";

interface Props {
    study: NonNullable<GetStudyQuery["study"]>;
}
const props = defineProps<Props>();

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
        </div>
    </aside>
</template>
