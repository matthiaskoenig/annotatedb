<template>
    <v-card>{{mapping}}</v-card>
</template>

<script>
    export default {
        name: "Mapping",
        props: {
            mapping: {
                type: Object,
                required: true
            },
        }
    }
</script>

<style scoped>

</style>