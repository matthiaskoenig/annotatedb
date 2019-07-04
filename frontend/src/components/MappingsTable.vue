<template>
    <v-card flat>
        <v-toolbar id="heading-toolbar" dark>
            <v-text-field
                    v-model="search"
                    append-icon="fa-search"
                    label="Search"
                    single-line
                    hide-details
                    :autofocus=true
            />
        </v-toolbar>
            <v-data-table dark
                    :headers="headers"
                    :items="entries"
                    :pagination.sync="pagination"
                    :total-items="count"
                    :loading="loading"
                    :class="table_class"

            >
            <template slot="items" slot-scope="table">
                <td>{{table.item.pk}}</td>
                <td>{{table.item.qualifier}}</td>
            </template>
        </v-data-table>
    </v-card>
</template>

<script>
    import axios from 'axios'

    export default {
        name: "MappingsTable",
        components: {},
        data () {
            return {
                search: '',
                headers: [
                    {text: 'pk', value: 'pk'},
                    {text: 'qualifier', value: 'qualifier'},
                ],
                count: 0,
                entries: [],
                search:"",
                loading: true,
                pagination: {},
                rowsPerPageItems: [5, 10, 20, 50, 100],
                table_class: "elevation-1",
            }
        },
        computed: {
            resource_url() {
                return this.$store.state.endpoints.django  + '/search/mappings/?format=json'
            },
            /**
             * Create query url.
             * @returns {string}
             */
            url() {
                var url = this.resource_url
                    // + '&page='+ this.pagination.page
                    // + '&page_size='+ this.pagination.rowsPerPage
                // + '&ordering='+ this.descending+ this.pagination.sortBy;
                // if (this.search){
                //     url += '&search_multi_match='+ this.search
                // }

                return url
            },
            descending() {
                return (this.pagination.descending ? "-" : "");
            }
        },
        methods: {
            icon(key) {
                return lookup_icon(key)
            },
            searchUpdate (newValue) {
                this.search = newValue
            },
            get_ids(array_of_obj) {
                return array_of_obj.map(i => i.pk)
            },

            getData() {
                var headers = {};
                console.log(this.url)
                if (localStorage.getItem('token')) {
                    var headers = {
                        Authorization :  'Token ' + localStorage.getItem('token')
                    }
                }
                axios.get(this.url, {headers: headers})
                    .then(res => {
                        this.entries = res.results;
                        this.count = res.count;
                    })
                    .catch(err => {
                        console.log(err);
                    })
                    .finally(() => this.loading = false);
            },
        },
        watch: {
            pagination: {
                handler () {
                    this.getData()
                },
                deep: true
            },
            search: {
                handler () {
                    this.getData();
                },
                deep: true
            },
            url: {
                handler () {
                    this.getData();
                },
                deep: true
            }
        },
        mounted () {
            this.getData()
        }
    }
</script>

<style scoped></style>


