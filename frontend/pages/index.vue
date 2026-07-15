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
                    {{ $t("About MyResearch") }}
                </h2>
                <div class="uu-container">
                    <p>
                        {{
                            $t(
                                "MyResearch is a tool with which researchers of Utrecht University can register their research activities. This is a legal requirement for the processing of personal data, for example data relating to research participants.",
                            )
                        }}
                    </p>
                    <p>
                        {{
                            $t(
                                "At this time MyResearch provides a data processing register that facilitates compliance with the AVG, or the Dutch implementation of the EU-wide General Data Protection Regulation (GDPR). Future development will allow for multiple registration activities, including Ethical approval, to be completed at once within MyResearch.",
                            )
                        }}
                    </p>
                </div>
            </div>
            <aside class="uu-sidebar pe-3">
                <RecentActivity />
            </aside>
        </div>
        <div class="uu-sidebar-container uu-sidebar-right uu-sidebar-sticky">
            <div class="uu-sidebar-content">
                <h2 class="uu-sidebar-header-linked">
                    {{ $t("The processing register") }}
                </h2>
                <p>
                    {{
                        $t(
                            "When you process personal data in your research, you are mandated to treat them with care and protect them accordingly. A necessary part of that is to register which data you collect and how you process them.",
                        )
                    }}
                </p>

                <p>
                    {{
                        $t(
                            "The participating faculties of Humanities and Law, Economics, and Governance aim to provide a data processing register that is attuned to the needs of researchers and the kind of data processing that scientific research entails. You don't need any previous knowledge to register the data you process in MyResearch: a guided questionnaire will make things easy.",
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
                            "The registration of data processing activities is done at the study level by the lead researcher. The definition of a study may very from one research project to the next. If in doubt, we recommend taking a narrow scope: consider a study to be the set of data and processing activities attributed to one research question. Making additional registrations is always an option.",
                        )
                    }}
                </p>
                <p>
                    {{
                        $t(
                            'After logging in with your Solis-ID you can start immediately by navigating to "New registration".',
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
                    }}<a href="mailto:privacy.gw@uu.nl">privacy.gw@uu.nl</a>
                </p>
                <p>
                    {{ $t("For technical issues relating to myresearch:") + " "
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
