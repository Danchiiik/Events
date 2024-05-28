<template>
  <section class="home">
    <div class="container">
      <div class="filter-main">

        <div class="filter-create">
          <div class="filters">
            <div class="buttons">
              <router-link to="/">
                <button class="all"><p class="reset">Сбросить</p></button>
              </router-link>
              <button class="date-ordering"><p class="date">Дата</p></button>
            </div>
            <div class ="three-filters">
              
              <div class="region-filter">
                <label for="regions" class="regions">Регион:</label> <br>
                <select name="region" id="region" class="regions-select">
                  <option value="default">-</option>
                  <option value="Bishkek">Бишкек</option>
                <option value="Chui">Чуй</option>
                <option value="Talas">Талас</option>
                <option value="Issyk-Kul">Иссык-Куль</option>
                <option value="Jalal-Abad">Жалал-Абад</option>
                <option value="Naryn">Нарын</option>
                <option value="Osh">Ош</option>
                <option value="Batken">Баткен</option>
              </select> <br>
            </div>
            
            <div class="types_event-filter">
              <label for="types_of_events" class="types-of-events">Вид мероприятия:</label> <br>
              <select name="types_of_event" id="types_of_event" class="types_event-select">
                <option value="default">-</option>
                <option value="1">Открытие</option>
                <option value="2">Выставка</option>
                <option value="3">Ярмарка</option>
                <option value="4">Презентация</option>
                <option value="5">Праздник</option>
                <option value="6">Пресс-мероприятие</option>
                <option value="7">Тренинг/семинар</option>
                <option value="8">Фестиваль/концерт</option>
              </select> <br>
            </div>

            <div class="type-filter">
              <label for="types" class="types">Тип мероприятия:</label> <br>
              <select name="types" id="types" class="types-select">
                <option value="default">-</option>
                <option value="1">Открытый</option>
                <option value="2">Закрытый</option>
              </select>            
            </div>
          </div>
        </div>
      </div>
    </div>
      
      <div class="events-main">
        <div class="event-cards">
          <div class="box"
          v-for="event in Events"
          v-bind.key = "event.id"
          @click="redirectToDetail(event.id)" 
          >
          <img v-bind:src="event.image" alt="" class="image-event">
          <div class="name-event-div">
            <span class="name-event">{{formatName(event.name)}}</span>
          </div>
          <p class="owner">Организатор:</p><span class="owner-event"> {{ event.owner }}</span>
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
        console.log("Events response: ", response.data);
      } catch (error) {
        console.error("An error occurred: ", error);
      }
    },
    formatName(name) {
      try {
        if (name.length > 25) {
          return `${name.substring(0, 25)}...`;
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


