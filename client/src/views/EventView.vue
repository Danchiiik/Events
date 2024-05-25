    <template>


    </template>

<script>
import axios from 'axios'

export default {
    name: 'EventView',

    data() {
        return {
            event: {},
            nameEvent: "",
        }
    },
    mounted() {
        this.getEvent()
        document.title = 'Loading...'
    },
    methods: {
    getEvent() {
        const eventId = this.$route.params.id

        axios
        .get(`/api/v1/events/${eventId}/`)
        .then(response => {
            this.event = response.data
            this.nameEvent = response.data.name
            document.title = this.nameEvent 
            
            console.log("Detail data: ", response.data)
            console.log("***************8: ", response.data.name)
        })
        .catch(errors => {
            console.log("An error occured: ", errors)
        })
    },
    redirectToDetail(eventId) {
        window.location.href = eventId
    },
    previous() {
        this.$router.go(-1)
    },
    }
}


</script>


<style>
@import '../components/css/main.css';
</style>
