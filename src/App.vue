<template>
  <div id="app">
    <!-- <img class="logo" src="./assets/logo.png">
    <img class="logo" src="./assets/dj.png"> -->
    <router-view/>
    <p>
      Welcome to your Django - Vue.js app!
    </p>
  </div>
</template>

<script>
export default {
  name: 'app'
}
</script>

<style>
.html {
  height: 100%;
}

.body {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

#app {
  color: #2c3e50;
  text-align: center;
}

#app a {
  color: #42b983;
  text-decoration: none;
}

.logo {
  width: 100px;
  height: 100px
}
</style>
