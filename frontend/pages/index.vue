<script setup lang="ts">
import SeasonalCover from "~/components/frontpage/SeasonalCover.vue";
import RecentActivity from "~/components/frontpage/RecentActivity.vue";
definePageMeta({
    public: true,
});
</script>
<template>
    <div class="uu-content">
        <Title>{{ $t("MyResearch") }}</Title>
        <SeasonalCover />
        <div class="uu-hero">
            <h1>{{ $t("Home") }}</h1>
        </div>
        <div class="uu-sidebar-container uu-sidebar-right">
            <div class="uu-sidebar-content">
                <h2 class="uu-sidebar-header-linked">
                    {{ $t("What is MyResearch?") }}
                </h2>
                <div class="uu-container">
                    <p>
                        {{
                            $t(
                                "MyResearch is a portal that supports researchers from the faculties of Humanities and Law, Economics, and Governance of Utrecht University in preparing their research projects. Some preparatory activities are legally required, others arise from university or faculty policy.",
                            )
                        }}
                    </p>
                    <i18n-t keypath="MyResearch currently offers a {processingRegister} to comply with legal obligations under the General Data Protection Regulation (GDPR). In the future, more and more preparatory tasks will be accommodated in MyResearch, so that you as a researcher can meet a multitude of requirements in one request. Consider drawing up a data management plan and submitting an application for ethical review." tag="p">
                        <template #processingRegister>
                            <b>{{
                                $t( "processing register for research data" )
                            }}
                            </b>
                        </template>
                    </i18n-t>
                </div>
            </div>
            <aside class="uu-sidebar pe-3">
                <RecentActivity />
            </aside>
        </div>
        <div class="uu-sidebar-container uu-sidebar-right uu-sidebar-sticky">
            <div class="uu-sidebar-content">
                <h2 class="uu-sidebar-header-linked">
                    {{ $t("Processing Register") }}
                </h2>
                <i18n-t keypath="If you process {personalData} relating to one or more identifiable persons (usually participants) in your research, you are obliged to complete the processing register." tag="p">
                    <template #personalData>
                        <a href="https://intranet.uu.nl/en/knowledgebase/what-is-personal-data" target="_blank">{{
                            $t( "personal data" )
                        }}
                        </a>
                    </template>
                </i18n-t>
                <p>
                    {{
                        $t(
                            "Via MyResearch, the participating faculties offer a processing register that is carefully tailored to the needs of researchers and to the processing operations that most commonly occur in scientific research. You do not need to have knowledge of the GDPR to register the processing in your study: your registration is completed on the basis of a helpful questionnaire.",
                        )
                    }}
                </p>
            </div>
            <aside class="uu-sidebar pe-3"></aside>
        </div>
        <div class="uu-sidebar-container uu-sidebar-right uu-sidebar-sticky">
            <div class="uu-sidebar-content">
                <h2 class="uu-sidebar-header-linked">
                    {{ $t("Where can I start?") }}
                </h2>
                <p>
                    {{
                        $t(
                            "The conducting researcher registers the research activities per study. The definition of a “study” may differ per research project. If in doubt, we advise you to take this definition narrowly. That is, the activities required to answer one research question. You can always make additional registrations.",
                        )
                    }}
                </p>
                <p>
                    {{
                        $t(
                            'After logging in with your Solis ID, you can start right away by navigating to "New registration".',
                        )
                    }}
                </p>
            </div>
            <aside class="uu-sidebar">
                <h2 class="uu-sidebar-header-linked">Contact</h2>
                <p>
                    {{
                        $t(
                            "For questions about the processing register contact the privacy officer:",
                        ) + " "
                    }}<a href="mailto:privacy.gw@uu.nl">privacy.gw@uu.nl</a>/<a href="mailto:privacy.rebo@uu.nl">privacy.rebo@uu.nl</a>
                </p>
                <p>
                    {{ $t("For technical issues relating to MyResearch:") + " "
                    }}<a href="mailto:portalsupport.gw@uu.nl"
                        >portalsupport.gw@uu.nl</a
                    >
                </p>
            </aside>
        </div>
        <div class="uu-sidebar-container uu-sidebar-right uu-sidebar-sticky">
            <div class="uu-sidebar-content"></div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.card {
    width: 60%;
}

.card-image-left {
    display: flex;

    & img {
        width: 30%;
    }
}
</style>
