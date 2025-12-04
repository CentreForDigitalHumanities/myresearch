<script setup lang="ts">
import springURL from "assets/images/covers/coverimage-spring.jpg";
import summerURL from "assets/images/covers/coverimage-summer.jpg";
import autumnURL from "assets/images/covers/coverimage-autumn.jpg";
import winterURL from "assets/images/covers/coverimage-winter.jpg";

const seasons = {
    spring: {
        image: springURL,
        author: "Dick Boetekees",
    },
    summer: {
        image: summerURL,
        author: "Bert Spiertz",
    },
    autumn: {
        image: autumnURL,
        author: "Ivar Pel",
    },
    winter: {
        image: winterURL,
        author: "Simona Evstatieva",
    },
};
function getSeasonalCoverImage() {
    const month = new Date().getMonth() + 1; //months go from 1 to 12.
    if ([3, 4, 5].includes(month)) {
        return seasons["spring"];
    } else if ([6, 7, 8].includes(month)) {
        return seasons["summer"];
    } else if ([9, 10, 11].includes(month)) {
        return seasons["autumn"];
    } else {
        return seasons["winter"];
    }
}
const seasonCover = getSeasonalCoverImage();
</script>

<template>
    <div class="uu-cover h-400">
        <img
            :src="seasonCover.image"
            class="uu-cover-image w-100"
            alt="cover"
        />
        <div class="uu-cover-copyright uu-cover-copyright-right">
            {{ $t("Cover by") }} {{ seasonCover.author }}
        </div>
    </div>
</template>
