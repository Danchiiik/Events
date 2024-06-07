<template>
  <section class="home">
    <div class="container">
      <div class="filter-main">

        <div class="filter-create">
          <div class="filters">

            <div class="buttons">
              <router-link to="/">
                <button class="all" @click="resetFilters"><p class="reset">Сбросить</p></button>
              </router-link>
              <button class="date-ordering" @click="toggleDateOrdering"><p class="date">По дате</p></button>
            </div>

            <div class ="three-filters">  
              <div class="region-filter">
                <label for="regions" class="regions">Регион:</label> <br>
                <select name="region" id="region" class="regions-select" v-model="filters.region" @change="applyFilters">
                  <option value="default">-</option>
                  <option value="Бишкек">Бишкек</option>
                <option value="Чуй">Чуй</option>
                <option value="Талас">Талас</option>
                <option value="Иссык-Куль">Иссык-Куль</option>
                <option value="Жалал-Абад">Жалал-Абад</option>
                <option value="Нарын">Нарын</option>
                <option value="Ош">Ош</option>
                <option value="Баткен">Баткен</option>
              </select> <br>
            </div>
            
            <div class="types_event-filter">
              <label for="types_of_events" class="types-of-events">Вид мероприятия:</label> <br>
              <select name="types_of_event" id="types_of_event" class="types_event-select" v-model="filters.typeOfEvent" @change="applyFilters">
                <option value="default">-</option>
                <option value="Открытие">Открытие</option>
                <option value="Выставка">Выставка</option>
                <option value="Ярмарка">Ярмарка</option>
                <option value="Презентация">Презентация</option>
                <option value="Праздник">Праздник</option>
                <option value="Пресс-мероприятие">Пресс-мероприятие</option>
                <option value="Тренинг/семинар">Тренинг/семинар</option>
                <option value="Фестиваль/концерт  ">Фестиваль/концерт</option>
              </select> <br>
            </div>

            <div class="type-filter">
              <label for="types" class="types">Тип мероприятия:</label> <br>
              <select name="types" id="types" class="types-select" v-model="filters.type" @change="applyFilters">
                <option value="default">-</option>
                <option value="Открытый">Открытый</option>
                <option value="Закрытый">Закрытый</option>
              </select>            
            </div>
          </div>
        </div>
      </div>
    </div>
      
      <div class="events-main">

        <div class="search-div">
          <input type="text" class="search-input" v-model="searchQuery" placeholder="Поиск...">
          <button class="search-button" @click="applySearch"><span>Поиск</span></button>
        </div>


        <div class="event-cards">
          <div class="box"
          v-for="event in filteredEvents"
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
import axios from 'axios';

export default {
  name: 'HomeView',
  data() {
    return {
      Events: [],
      usernames: {},
      filteredEvents: [],
      filters: {
        region: 'default',
        typeOfEvent: 'default',
        type: 'default',
        dateOrdering: null,
      },
      searchQuery: '',

    }
  },
  mounted() {
    this.getEvent();
    document.title = "Events.kg";
  },
  methods: {
    async getEvent() {
      try {
        const response = await axios.get("/api/v1/events/");
        this.Events = response.data.results;
        this.filteredEvents = this.Events;
        console.log("Events response: ", response.data);

        this.Events.forEach(event => {
          this.ownerUsername(event.owner);
        });

      } catch (error) {
        console.error("An error occurred: ", error);
      }
    },

    applyFilters() {
      this.applySearch(); 
    },

    applyFiltersToSearchResults() {
      this.filteredEvents = this.filteredEvents.filter(event => {
        const regionMatch = this.filters.region === 'default' || event.region === this.filters.region;
        const typeOfEventMatch = this.filters.typeOfEvent === 'default' || event.type_of_event === this.filters.typeOfEvent;
        const typeMatch = this.filters.type === 'default' || event.type === this.filters.type;

        return regionMatch && typeOfEventMatch && typeMatch;
      });

      if (this.filters.dateOrdering) {
        if (this.filters.dateOrdering === 'asc') {
          this.filteredEvents.sort((a, b) => new Date(a.date) - new Date(b.date));
        } else if (this.filters.dateOrdering === 'desc') {
          this.filteredEvents.sort((a, b) => new Date(b.date) - new Date(a.date));
        }
      }
    },

    applySearch() {
      const query = this.searchQuery.toLowerCase();
      this.filteredEvents = this.Events.filter(event => {
        return (
          event.name.toLowerCase().includes(query) ||
          this.getUsername(event.owner).toLowerCase().includes(query)
        );
      });

      this.applyFiltersToSearchResults();
    },

    resetFilters() {
      this.filters.region = 'default';
      this.filters.typeOfEvent = 'default';
      this.filters.type = 'default';
      this.filters.dateOrdering = null;
      this.searchQuery = '';
      this.applyFilters();
    },

    toggleDateOrdering() {
      if (this.filters.dateOrdering === 'asc') { 
        this.filters.dateOrdering = 'desc'; 
      } else {
        this.filters.dateOrdering = 'asc'; 
      }
      this.applyFilters();
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

    async ownerUsername(eventOwner) {
      try {
        const response = await axios.get(`api/v1/account/profile/`);
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

        if (priceString === null) {
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
    }
  }
}
</script>



<style>
@import '../components/css/main.css';
</style>


