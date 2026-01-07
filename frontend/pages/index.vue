<script setup lang="ts">
import SeasonalCover from "~/components/frontpage/SeasonalCover.vue";
import RecentActivity from "~/components/frontpage/RecentActivity.vue";
import FrequentQuestions from "~/components/frontpage/FrequentQuestions.vue";
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
                    {{
                        $t(
                            "My Research is a website that helps researchers with submitting a request to register a research. On this website you can register your research at the processing registry. First, however, you should fill in the roadmap",
                        )
                    }}
                </div>
                <h2 class="uu-sidebar-header-linked">
                    {{ $t("Roadmap") }}
                </h2>
                <div>
                    {{
                        $t(
                            "The Roadmap is a questionnaire that helps researchers to find out what needs to happen before starting a research project. Do I need to register my research at processing registry at all or not? The Roadmap helps you answer this question.",
                        )
                    }}
                    <div class="uu-container">
                        <div class="card-image-left">
                            <img
                                src="https://cataas.com/cat?height=200"
                                alt="Mooie afbeelding of niet"
                            />
                            <div class="card">
                                <div class="card-body">
                                    <h5 class="card-title">
                                        {{ $t("Start a new roadmap") }}
                                    </h5>
                                    <p class="card-text">
                                        {{ $t("Also possible as orientation") }}
                                    </p>
                                    <a href="#" class="btn btn-primary">{{
                                        $t("Start Roadmap")
                                    }}</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <aside class="uu-sidebar pe-3">
                <RecentActivity />
            </aside>
        </div>
        <div class="uu-sidebar-container uu-sidebar-right uu-sidebar-sticky">
            <div class="uu-sidebar-content">
                <h2 class="uu-sidebar-header-linked">
                    {{ $t("Processing registry") }}
                </h2>
                <p>
                    {{
                        $t(
                            "At the processing registry you register your studies that contain personal data. The processing registry is a central place for all studies with personal data. The Dutch government under the Algemene Verordening Gegevensbescherming (AVG) demands that studies are registered where personal data plays a role. Registering such studies also has an advantage for that researcher that registers the study: registration gives a user-friendly overview about aspects in data processing such as the type of personal data, the persons to whom those data apply, retention periods, used software, necessary security measures and the different parties that play a role",
                        )
                    }}
                </p>
            </div>
            <aside class="uu-sidebar pe-3">
                <FrequentQuestions
                    questions-group="processingRegistry"
                    title="Frequent questions"
                />
            </aside>
        </div>
        <div class="uu-sidebar-container uu-sidebar-right uu-sidebar-sticky">
            <div class="uu-sidebar-content">
                <h2 class="uu-sidebar-header-linked">
                    {{ $t("Ethical commission") }}
                </h2>
                <p>
                    {{
                        $t(
                            "Formal approval by a chamber for the FEtC-H (by means of an official approval letter) is required for research involving human participants within the UU Faculty of Humanities. You must acquire this approval prior even to recruiting participants. Therefore, always wait for the letter of approval before starting research activities.",
                        )
                    }}
                </p>
                <p>
                    {{
                        $t(
                            "Please Note: Accepted applications go to the archive. See above menu. The archive is available for everyone at the same facility with with a Solid-ID. ",
                        )
                    }}
                </p>
                <p>
                    <a
                        :href="$t('https://fetc-gw.wp.hum.uu.nl/en/')"
                        target="_blank"
                        >{{ $t("UU-webpage of the FEtC-H") }}</a
                    >
                </p>
                <p>
                    <a
                        :href="
                            $t(
                                'https://fetc-gw.wp.hum.uu.nl/en/regulations-fetc-h/',
                            )
                        "
                        target="_blank"
                        >{{ $t("Regulations of the FEtC-H") }}</a
                    >
                </p>
            </div>
            <aside class="uu-sidebar pe-3">
                <FrequentQuestions
                    questions-group="ethicalCommission"
                    title="Frequent questions"
                />
            </aside>
        </div>
        <div class="uu-sidebar-container uu-sidebar-right uu-sidebar-sticky">
            <div class="uu-sidebar-content">
                <FrequentQuestions
                    title="Other questions"
                    questions-group="other"
                />
            </div>
            <aside class="uu-sidebar">
                <h2 class="uu-sidebar-header-linked">Contact</h2>
                <p>
                    {{
                        $t(
                            "For questions about the processing registry contact the privacy officer:",
                        ) + " "
                    }}<a href="mailto:l.j.w.m.kessels@uu.nl"
                        >l.j.w.m.kessels@uu.nl</a
                    >
                </p>
                <p>
                    {{ $t("For compliments contact:") + " "
                    }}<a href="mailto:portaldev.gw@uu.nl">portaldev.gw@uu.nl</a>
                </p>
            </aside>
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
