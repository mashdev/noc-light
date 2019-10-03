<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/noc-seal.jpg">
    <HomeDash class="home-dash" msg="NOC Light Dashboard"/>
  </div>
</template>

<script>
// @ is an alias to /src
import HomeDash from '@/components/HomeDash.vue';

export default {
  name: 'home',
  components: {
    HomeDash,
  },
};
</script>


<style scoped>

img {
  height: 180px;
  width: 180px;
  margin: 25px 0px 0px 0px;
}

.home-dash {
  margin-top: 25px;
}

</style>
