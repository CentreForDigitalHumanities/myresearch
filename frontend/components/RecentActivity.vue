<script setup lang="ts"></script>

<template>
  <!-- TODO the first tile is not clickable everywhere, second one changes icon but is also not clickable -->
  <div class="tiles uu-container mw-100">
    <div class="tile w-100 mw-100">
      <NuxtLink to="/studies/" class="nav-link">
        <div class="row justify-content-between">
          <div class="col-8">
            <strong>refnumber + Titelmet langere naam</strong>
          </div>
          <div class="col-4">25-08-23</div>
        </div>
        <p></p>
        <div class="row justify-content-between">
          <div class="col-6">TYPE</div>
          <div class="col-6">Wegwijzer</div>
        </div>
        <div class="row justify-content-center">
          <div class="col-6">Status</div>
          <div class="col-6">DRAFT</div>
        </div>
        <div class="row justify-content-center">
          <div class="col-6">fav color</div>
          <div class="col-6">geel</div>
        </div>
        <div class="row justify-content-start">
          <div class="col-6">fav color</div>
          <div class="col-6">Geel</div>
        </div>
        <div class="row justify-content-end">
          <button class="btn btn-arrow-right col-6">Continue</button>
        </div>
      </NuxtLink>
    </div>
    <a class="tile w-100 mw-100">
      <NuxtLink to="/studies/" class="nav-link">
        <div class="row">
          <div class="col-8">
            <strong>refnumber + Titelmet langere naam</strong>
          </div>
          <div class="col-4">25-08-23</div>
        </div>
        <p></p>
        <div class="row">
          <div class="col-6">TYPE</div>
          <div class="col-6">Wegwijzer</div>
        </div>
        <div class="row">
          <div class="col-6">Status</div>
          <div class="col-6">DRAFT</div>
        </div>
        <div class="row">
          <div class="col-6">fav color</div>
          <div class="col-6">
            geel met een hele lange tekst erachter geplakt
          </div>
        </div>
        <div class="row justify-content-end">
          <button class="btn btn-arrow-right col-6">Continue</button>
        </div>
      </NuxtLink>
    </a>
  </div>
</template>

<style scoped>
.tiles .tile {
  aspect-ratio: 2/1;
}
</style>
