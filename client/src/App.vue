<template>
  <div id="app">
    <div class="container nav-bar-container">
      <ul class="nav justify-content-center">
        <li><a class="nav-link active" href="/"> HOME </a></li>
        <li><a class="nav-link active" href="/dashboard"> DASHBOARD </a></li>
        <li><a class="nav-link active" href="/add"> ADD </a></li>
      </ul>
    </div>
      <router-view/>
    </div>
</template>

<script>

export default {
  data() {
    return {

    };
  },
};

</script>

<style scoped>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  background-color: #fff;
  box-shadow: none;
}

a {
  color: #37474f;
}

.nav-bar-container {
  background-color: #37474f;
  margin-bottom: 45px;
}

.nav-bar-container a {
  color: #fff;
}

</style>
