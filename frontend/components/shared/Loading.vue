<script lang="ts" setup>
interface Props {
  inline?: boolean;
}
const props = withDefaults(defineProps<Props>(), {
  inline: false,
});
</script>

<template>
  <span class="text-center" :class="inline ? '' : 'mt-5 mb-5'">
    <div class="spinner-border spinner-border-sm" role="status" />
    {{ $t("Loading") }} ...
  </span>
</template>
