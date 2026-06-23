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
                    {{
                        $t(
                            "MyResearch is a website that helps researchers manage their research administration/MyResearch is a website that helps researchers with submitting a request to register a research. On this website you can register your research at the processing registry which than can be seen by the privacy officer.",
                        )
                    }}
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
            <aside class="uu-sidebar pe-3"></aside>
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
                    {{ $t("Registration for the FEtC-H can be done at the") }}
                    <a
                        :href="$t('https://fetc-gw.wp.hum.uu.nl/en/')"
                        target="_blank"
                        >{{ $t("UU-webpage of the FEtC-H") }}</a
                    >
                </p>
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
