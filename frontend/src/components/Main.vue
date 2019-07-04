<template>
    <v-container>
        <v-layout
                text-xs-center
                wrap
        >
            <v-flex xs12>
                <v-flex mb-4>
                    <v-img
                            :src="require('../assets/annotatedb.png')"
                            class="my-3"
                            contain
                            height="130"
                    ></v-img>
                </v-flex>

                <v-flex mb-4>
                    <h1 class="display-2 font-weight-bold mb-3">
                        Welcome to AnnotateDB<br/>
                        <span class="font-weight-light">&nbsp; annotation mappings made easy</span>
                    </h1>
                </v-flex>
            </v-flex>

            <v-flex xs12>
                <mappings-table></mappings-table>
            </v-flex>

            <v-flex xs12>
            <p class="subheading font-weight-regular">
                For help and questions, please open a
                <a href="https://github.com/matthiaskoenig/annotatedb/issues" target="_blank">Github Issue</a>
            </p>
            </v-flex>

        </v-layout>
    </v-container>
</template>

<script>
    import {lookup_icon} from "@/icons"
    import MappingsTable from "./MappingsTable";

    export default {
        components: {MappingsTable},
        data: () => ({}),
        methods: {
            icon: function (key) {
                return lookup_icon(key)
            },
        }

    }
</script>

<style>

</style>
