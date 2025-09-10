<script setup lang="ts"></script>

<template>
  <h2 class="uu-sidebar-header-linked">{{ $t("Recent Activity") }}</h2>
  <div class="tiles uu-container mw-100">
    <a class="tile w-100 mw-100 justify-content-center">
      <NuxtLink to="/studies/" class="nav-link">
        <div class="row">
          <div class="col-9">
            <strong>refnumber + Titel met langere naam</strong>
          </div>
          <div class="col-3">25-08-23</div>
        </div>
        <p></p>
        <div class="row justify-content-around">
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
        <p></p>
        <div class="row justify-content-end">
          <button class="btn btn-primary btn-arrow-right col-12">
            Continue
          </button>
        </div>
      </NuxtLink>
    </a>
  </div>
</template>

<style lang="scss" scoped>
.tiles .tile {
  aspect-ratio: 2/1;

  &:hover {
    background: white;
  }
}
</style>
