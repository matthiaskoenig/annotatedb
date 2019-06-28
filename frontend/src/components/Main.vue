<template>
  <v-container>
    <v-layout
      text-xs-center
      wrap
    >
      <v-flex xs12>
        <v-img
          :src="require('../assets/annotatedb.png')"
          class="my-3"
          contain
          height="150"
        ></v-img>
      </v-flex>

      <v-flex mb-4>
        <h1 class="display-2 font-weight-bold mb-3">
          Welcome to AnnotateDB
          <span class="font-weight-light">&nbsp; annotation mappings made easy</span>
        </h1>
        <p class="subheading font-weight-regular">
          For help and questions, please open a
          <a href="https://github.com/matthiaskoenig/annotatedb/issues" target="_blank">Github Issue</a>
        </p>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  export default {
    data: () => ({
    })
  }
</script>

<style>

</style>
