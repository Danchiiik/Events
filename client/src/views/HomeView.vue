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
                <option value="Вход свободный">Вход свободный</option>
                <option value="Вход закрытый">Вход закрытый</option>
              </select>            
            </div>
          </div>
        </div>
      </div>
    </div>
      
      <div class="events-main">

        <div class="search-div">
          <div class="search-in-div">
            <input type="text" class="search-input" v-model="searchQuery" placeholder="Поиск..." @keyup.enter="applySearch">
            <!-- <ul v-if="showRecommendations && searchQuery" class="recommend-bar">
              <li v-for="event in filteredEvents" :key="event.id" class="every-recommend" @click="selectRecommendation(event.name)">{{ event.name }}</li>
            </ul> -->
          </div>
          <button class="search-button" @click="applySearch"><span>Поиск</span></button>
        </div>


        <div class="event-cards">
          <div class="box"
          v-for="event in filteredEvents"
          v-bind.key = "event.id"
          @click="redirectToDetail(event.id)" 
          >

          <div class="for-image">
            <img v-bind:src="event.image" alt="" class="image-event">
          </div>
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

        <div class="pagination">
          <button @click="changePage(currentPage - 1)" :disabled="currentPage === 1" class="prev-button">Предыдущая</button>
          <button v-if="currentPage > 2" @click="changePage(1)" class="current-page">1</button>
          <span v-if="currentPage > 3">...</span>
          <button v-if="currentPage > 1" @click="changePage(currentPage - 1)" class="current-page">{{ currentPage - 1 }}</button>
          <button @click="changePage(currentPage)" :class="{ active: true }" class="current-page">{{ currentPage }}</button>
          <button v-if="currentPage < totalPages" @click="changePage(currentPage + 1)" class="current-page">{{ currentPage + 1 }}</button>
          <span v-if="currentPage < totalPages - 2">...</span>
          <button v-if="currentPage < totalPages - 1" @click="changePage(totalPages)" class="current-page">{{ totalPages }}</button>
          <button @click="changePage(currentPage + 1)" :disabled="currentPage === totalPages" class="next-button">Следующая</button>
        </div>


      </div>
    </div>
  </section>
</template>

<script>
import axios from 'axios';
import axiosInstance from '@/axiosSetup';

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
      currentPage: 1,
      totalPages: 0,
      itemsPerPage: 18,
      // showRecommendations: true,

    }
  },
  mounted() {
    this.getEvent();
    document.title = "Events.kg";
  },


  methods: {
    async getEvent(page = 1) {
      try {
        const response = await axiosInstance.get(`/api/v1/events/?page=${page}&limit=${this.itemsPerPage}`);
        this.Events = response.data.results;
        this.filteredEvents = this.Events;


        this.totalPages = Math.ceil(response.data.count / this.itemsPerPage) 
        console.log('Total pages', this.totalPages)
        console.log("Events response: ", response.data);

        this.Events.forEach(event => {
          this.ownerUsername(event.owner);
        });

      } catch (error) {
        console.error("An error occurred: ", error);
      }
    },

    async applyFilters() {
      this.applySearch(); 
    },

    async changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
        this.resetFilters();
        await this.getEvent(page);
      }
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

    async applySearch() {

      const query = this.searchQuery.toLowerCase();
      this.filteredEvents = this.Events.filter(event => {
        return (
          event.name.toLowerCase().includes(query) ||
          this.getUsername(event.owner).toLowerCase().includes(query)
        );
      });

      // this.showRecommendations = false;
      this.applyFiltersToSearchResults();
    },

    // onInput() {
    //   this.showRecommendations = true;
    //   this.applySearch(this.searchQuery);
    // },

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

    // selectRecommendation(event) {
    //   this.searchQuery = event;
    //   this.applySearch(event);

    //   this.showRecommendations = false
    // },


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
    }
  }
}
</script>



<style>
@import '../components/css/main.css';
</style>


