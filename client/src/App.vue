<template>
  <div id="app">
    <div class="navbar container">
      <div class="navbar-fixed">
      <nav>
        <div class="nav-wrapper">
          <ul class="hide-on-med-and-down">
            <li><a href="/"> HOME </a></li>
            <li><a href="/dashboard"> DASHBOARD </a></li>
            <li><a href="/add"> ADD </a></li>
          </ul>
        </div>
      </nav>
      </div>
    </div>
      <router-view/>
    </div>
</template>

<script>

export default {
  data() {
    return {

    }
  }
}

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

.nav-wrapper {
  box-shadow: none;
  width: 50%;
}

</style>
