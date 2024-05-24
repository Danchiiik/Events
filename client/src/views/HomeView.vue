<template>
  <section class="home">
    <div class="container">
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

      <div class="events-main">
        <div class="event-cards">
          <div class="box"
          v-for="event in Events"
          v-bind.key = "event.id"
          @click="redirectToDetail(event.id)"
          >
            <p class="name">Название:</p><span class="name-event">{{ event.name }}</span>
            <p class="owner">Организатор:</p>
            <img v-bind:src="event.image" alt="" class="image">
            <p class="description">Описание:</p><span class="desc-event">{{ event.description }}</span>
            <p class="address">Адресс:</p><span class="address-event">{{ event.address }}</span>
            <p class="date">Дата:</p><span class="date-event">{{ event.date }}</span>
            <p class="time">Время:</p><span class="time-event">{{ event.time }}</span>
            <p class="type_of_event">Вид:</p><span class="types-event-event">{{ event.type_of_event }}</span>
            <p class="type">Тип:</p><span class="type-event">{{ event.type }}</span>
            <p class="price">Цена:</p><span class="price-event">{{ event.price }}</span>
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
    this.getEvent() 
    document.title = "Events.kg"

  },
  methods: {
    getEvent() {

      axios
      .get("api/v1/events/")
      .then(response =>{
        this.Events = response.data.results
        console.log("Events response: ", response.data)
      })
      .catch(errors =>{
        console.log("Errors: ", errors)
      })
    },

    redirectToDetail(eventId){
      this.$router.push(`/events/${eventId}`)
    } 
  }
}
</script>


<style>
@import '../components/css/main.css';
</style>
