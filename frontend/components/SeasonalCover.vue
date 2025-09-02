<script setup lang="ts">
import springURL from "@/assets/images/covers/coverimage-spring.jpg";
import summerURL from "@/assets/images/covers/coverimage-summer.jpg";
import autumnURL from "@/assets/images/covers/coverimage-autumn.jpg";
import winterURL from "@/assets/images/covers/coverimage-winter.jpg";
const seasons = {
  spring: {
    image: springURL,
    author: "Dick Boetekees",
    // seasons.classes controls how the image is fitted inside the container; every image has its own 'best' fit
    classes: "align-items-end",
  },
  summer: {
    image: summerURL,
    author: "Bert Spiertz",
    classes: "align-items-middle",
  },
  autumn: {
    image: autumnURL,
    author: "Ivar Pel",
    classes: "align-items-middle",
  },
  winter: {
    image: winterURL,
    author: "Simona Evstatieva",
    classes: "align-items-middle",
  },
};
//only considers Dutch seasons, not Australian
function getSeasonalCoverImage() {
  let month = new Date().getMonth() + 1; //const month goes from 1 to 12
  if ([3, 4, 5].includes(month)) {
    return seasons["spring"];
  } else if ([6, 7, 8].indexOf(month) >= 0) {
    return seasons["summer"];
  } else if ([9, 10, 11].indexOf(month) >= 0) {
    return seasons["autumn"];
  } else {
    return seasons["winter"];
  }
}
const seasonCover = getSeasonalCoverImage();
</script>

<template>
  <div :class="'uu-cover h-400 ' + seasonCover.classes">
    <img
      v-bind:src="seasonCover.image"
      class="uu-cover-image w-100"
      alt="cover"
    />
    <div class="uu-cover-copyright uu-cover-copyright-right">
      Cover by {{ seasonCover.author }}
    </div>
  </div>
</template>
<style scoped></style>
