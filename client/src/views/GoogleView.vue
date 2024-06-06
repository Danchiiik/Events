<template>
</template>


<script>
import axios from 'axios';

export default {
    name: 'GoogleView',
    data() {
        return {
        email: "",
        }
    },

    mounted(){
        document.title = "Google authentication"
    }
}

</script>