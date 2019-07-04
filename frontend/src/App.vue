<template>
  <v-app>
    <v-toolbar app flat>
      <v-toolbar-title class="headline" >

        <!--<span class="text-uppercase">AnnoteDB</span>-->
        <!--<span class="font-weight-light">&nbsp; annotations made easy</span>-->
      </v-toolbar-title>


      <v-btn icon color="black" :href="api_url" title="REST API">
        <v-icon color="white">{{ icon('api') }}</v-icon>
      </v-btn>
      <v-spacer></v-spacer>


      <v-btn icon color="black" href="https://www.github.com/matthiaskoenig/annotatedb" title="Documentation and additional information">
        <v-icon color="white">{{ icon('about')}}</v-icon>
      </v-btn>
      <v-btn icon color="black" href="https://www.github.com/matthiaskoenig/annotatedb" title="GitHub code repository">
        <v-icon color="white">{{ icon('github')}}</v-icon>
      </v-btn>
      <v-btn icon color="black" :href="admin_url" title="Admin interface">
        <v-icon color="white">{{ icon('admin') }}</v-icon>
      </v-btn>
    </v-toolbar>

    <v-content>
      <Main/>
    </v-content>

  </v-app>
</template>

<script>
import {lookup_icon} from "@/icons"
import Main from './components/Main'

export default {
  name: 'App',
  components: {
    Main,
  },
  data () {
    return {
      //
    }
  },
  computed: {
    // vuex store
    admin_url() {
      return this.$store.state.endpoints.django + '/admin/';
    },
    api_url() {
      return this.$store.state.endpoints.api;
    }
  },
  methods: {
    icon: function (key) {
      return lookup_icon(key)
    },
  }
}
</script>
