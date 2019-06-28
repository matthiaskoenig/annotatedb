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
          height="130"
        ></v-img>
      </v-flex>

      <v-flex mb-4>
        <h1 class="display-2 font-weight-bold mb-3">
          Welcome to AnnotateDB<br />
          <span class="font-weight-light">&nbsp; annotation mappings made easy</span>
        </h1>
        <p class="subheading font-weight-regular">
          For help and questions, please open a
          <a href="https://github.com/matthiaskoenig/annotatedb/issues" target="_blank">Github Issue</a>
        </p>
      </v-flex>

      <v-flex>
        Icon added
        <v-icon>{{ icon('admin') }}</v-icon>
        <font-awesome-icon icon="admin" />
        {{ icon('admin') }}

        <v-alert
                :value="true"
                type="success"
        >
          This is a success alert.
        </v-alert>
        <v-icon>event</v-icon>
        <v-icon>info</v-icon>
      </v-flex>

    </v-layout>
  </v-container>
</template>

<script>
  import {lookup_icon} from "@/icons"

  export default {
    data: () => ({
    }),
    methods: {
      icon: function (key) {
        return lookup_icon(key)
      },
    }

  }
</script>

<style>

</style>
