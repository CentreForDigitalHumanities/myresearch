<script lang="ts" setup>
export interface SideBarConfig {
    questions?: {
        textNl: string;
        textEn: string;
        link: string;
    }[];
    extraInfo?: {
        textNl: string;
        textEn: string;
    }[];
}

const props = defineProps<{
    config: SideBarConfig;
}>();
</script>
<template>
    <div class="uu-form-help">
        <div class="help-item">
            <div v-if="props.config.questions?.length">
                <strong>{{ $t("Questions?") }}</strong>
            </div>
            <template
                v-for="(question, index) in config.questions"
                :key="index"
            >
                <a
                    :href="question.link"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="d-block my-1"
                >
                    {{ useTranslateableAttribute(question, "text") }}
                </a>
            </template>
        </div>
        <div class="help-item">
            <div v-if="props.config.extraInfo?.length">
                <strong>{{ $t("Additional Information") }}</strong>
                <ul>
                    <li
                        v-for="(info, index) in props.config.extraInfo"
                        :key="index"
                    >
                        {{ useTranslateableAttribute(info, "text") }}
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.help-item:not(:last-child) {
    margin-bottom: 2rem;
}
</style>
