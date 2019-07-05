<template>
    <span>
        
        <span v-for="mapping in entries">
            <mapping :mapping="mapping"></mapping>
        </span>
    </span>
</template>

<script>
    import axios from 'axios'
    import Mapping from "./Mapping"


    export default {
        name: "MappingsTable",
        components: {
            Mapping
        },
        data () {
            return {
                search: '',
                headers: [
                    {text: 'data', value: 'data'},
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
                return this.$store.state.endpoints.django  + '/search/mapping/?format=json'
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
                let headers = {};
                console.log(this.url)
                axios.get(this.url, {headers: headers})
                    .then(res => {
                        this.entries = res.data.results;
                        this.count = res.data.count;
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


