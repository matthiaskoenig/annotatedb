<template>
  <v-app>
    <v-toolbar app flat>
      <v-toolbar-title class="headline" >

        <span class="text-uppercase">AnnoteDB</span>
        <!--<span class="font-weight-light">&nbsp; annotations made easy</span>-->
      </v-toolbar-title>
      <v-spacer></v-spacer>

      <v-btn
        flat
        href="https://github.com/vuetifyjs/vuetify/releases/latest"
        target="_blank"
      >
        <span class="mr-2">Latest Release</span>

      </v-btn>

      <v-btn icon color="blue" :href="api_url" title="REST API"><v-icon>{{ icon('api') }}</v-icon></v-btn>
      <v-btn icon color="blue" :href="admin_url" title="Django admin interface">
        <v-icon>{{ icon('admin') }}</v-icon>
      </v-btn>

      <v-btn icon color="blue" href="https://www.github.com/matthiaskoenig/annotatedb" title="GitHub code repository">
        <v-icon>{{ icon('github')}}</v-icon>
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
      return this.$store.state.django_domain + '/admin/';
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
