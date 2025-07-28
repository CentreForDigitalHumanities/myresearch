<script lang="ts" setup>
export interface SideBarConfig {
  titleNl?: string;
  titleEn?: string;
  paragraphs: {
    textNl: string;
    textEn: string;
    link?: string;
  }[];
}

const props = defineProps<{
  config: SideBarConfig;
}>();
</script>
<template>
  <div class="uu-form-help">
    <div v-if="props.config.titleNl || props.config.titleEn">
      <strong>{{ useTranslateableAttribute(props.config, "title") }}</strong>
    </div>
    <template v-for="(paragraph, index) in config.paragraphs" :key="index">
      <a
        v-if="paragraph.link"
        :href="paragraph.link"
        target="_blank"
        rel="noopener noreferrer"
      >
        {{ useTranslateableAttribute(paragraph, "text") }}
      </a>
      <p v-else>{{ useTranslateableAttribute(paragraph, "text") }}</p>
      <br />
    </template>
  </div>
</template>
