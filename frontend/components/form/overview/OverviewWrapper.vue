<script lang="ts" setup>
import { computed } from "vue";
import type { QueriedForm } from "../FormWrapper";
import { useFormState } from "~/composables/useFormState";
import useVuelidate from "@vuelidate/core";
import SubmissionOverview from "~/components/form/overview/OverviewForm.vue";
import { useAnnotateErrors } from "~/composables/useAnnotateErrors";

interface Props {
    queriedForm: QueriedForm;
}
const props = defineProps<Props>();

const queried = computed(() => props.queriedForm);
const { formObject, validationRules } = useFormState(queried);

const v$ = useVuelidate(
    validationRules,
    computed(() => formObject.value ?? { steps: [] }),
    {
        $autoDirty: true,
    },
);

void v$.value.$validate();

watchEffect(() => {
    if (formObject.value) {
        useAnnotateErrors(v$.value, formObject.value);
    }
});
</script>

<template>
    <SubmissionOverview v-if="formObject" :form="formObject" />
</template>
