<template>
    <section class="fav-section">
        <div class="container">
            <div class="fav-main-div">

                <div class="fav-header">
                    <span>Мои сохраненные</span>
                </div>

                <div class="fav-event-cards">
                    <div class="box"
                    v-for="event in Events"
                    v-bind.key = "event.id"
                    @click="redirectToDetail(event.id)" 
                    >
                    <img v-bind:src="event.image" alt="" class="image-event">
                    <div class="name-event-div">
                        <span class="name-event">{{formatName(event.name)}}</span>
                    </div>
                    <p class="owner">Организатор:</p><span class="owner-event"> {{ getUsername(event.owner) }}</span>
                    <p class="type_of_event">Вид:</p><span class="types-event-event">{{ event.type_of_event }}</span>
                    <div class="info-event">
                        <span class="region-event">{{ event.region }}</span>
                        <span class="address-event">{{ event.address }}</span>
                        <span class="date-event">{{ formatDate(event.date) }}</span>
                        <span class="time-event">{{ event.time }}</span>
                        <span class="type-event">{{ event.type }}</span>
                        <span class="price-event">{{ formatPrice(event.price) }}</span>
                    </div>
                    </div>
                </div>

            </div>      
        </div>


    </section>
</template>


<script>
import axiosInstance from '@/axiosSetup';

export default {
    name: 'Favourites',
    data() {
        return {
            Fav: [],
            Events: [],
            usernames: {},
        }
    },

    mounted() {
        this.getFav();
        document.title = 'My favourites'
    },

    methods: {
        async getFav() {
            try {
                const response = await axiosInstance.get("/api/v1/events/favourites/");
                this.Fav = response.data;
                console.log("Fav events response: ", response.data);

                const eventDetailsPromises = this.Fav.map(async (fav) => {
                const eventResponse = await axiosInstance.get(`/api/v1/events/${fav.event}/`);
                return eventResponse.data;
               });

                this.Events = await Promise.all(eventDetailsPromises);
                console.log("Event details: ", this.Events);

                this.Events.forEach(event => {
                this.ownerUsername(event.owner);
                });
                
            } catch (error) {
                console.error("An error occurred: ", error);
            }
        },

        formatName(name) {
            try {
                if (name.length > 22) {
                return `${name.substring(0, 22)}...`;
                }
                return name;
            } catch (error) {
                console.error("An error occurred: ", error);
                return name; 
            }
        },

        formatDate(dateString) {
            try {
                const [year, month, day] = dateString.split('-');
                return `${day}/${month}/${year}`;
            } catch (error) {
                console.error("An error occurred: ", error); 
            }
        },

        formatPrice(priceString) {
            try {

                if (priceString === null || priceString == 0) {
                return "Бесплатно";
                } else {
                return `${parseInt(priceString, 10)} сом`;
                }
            } catch {
                console.error("An error occurred: ", error); 
            }
        },

        redirectToDetail(eventId) {
            try {
                this.$router.push(`/events/${eventId}`);
            } catch {
                console.error("An error occurred: ", error); 
            }
        },  
        
        async ownerUsername(eventOwner) {
            try {
                const response = await axiosInstance.get(`api/v1/account/profile/`);
                const filteredResponse = response.data.filter(profile => profile.user === eventOwner);
                if (filteredResponse.length > 0) {
                this.usernames[eventOwner] = filteredResponse[0].username;
                } else {
                console.log("No user found for the given event owner");
                this.usernames[eventOwner] = 'Unknown';
                }
            } catch (error) {
                console.log('An error occurred: ', error);
                this.usernames[eventOwner] = 'Error';
            }
        },

        getUsername(eventOwner) {
            return this.usernames[eventOwner] || 'Loading...';
        },


    }
    
    

}
</script>


<style>
@import '../components/css/main.css';
</style>