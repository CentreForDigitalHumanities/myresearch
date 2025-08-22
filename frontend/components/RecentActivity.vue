<script setup lang="ts"></script>

<template>
  <div class="tiles uu-container mw-100">
    <!-- mw-100 only goes for this div and not those below them, seems to give the tiles the same size as well -->
    <a class="tile w-100">
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
    </a>
    <a class="tile w-100">
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
hello div {
  max-width: 100% !important;
}
</style>
