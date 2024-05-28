    <template>
      <div class="home-event">
        <div class="container">
          <div class="content">
            <div class="img-event">
              <img v-bind:src="event.image" class="main-img">
              <div class="like-fav">
                <div class="like-div">
                  <div class="like"><img src="../../static_files/free-icon-heart-8181213.png" class="like-sign"></div>
                  <div class="like-count">
                    <span>{{ event.likes }}</span>
                  </div>
                </div>

                <div class="favourite"><img src="../../static_files/free-icon-bookmark-2710704.png" class="fav-sign"></div>
              </div>
            </div>
            <div class="infoo-event">
              <div class="info-event-div">
                <span class="main-event-name">{{ event.name }}</span>
                <p class="main-event-owner-p">Организатор:</p><span class="main-event-owner"> {{ event.owner }}</span>
                <p class="main-event-types-p">Вид:</p><span class="main-event-types">{{ event.type_of_event }}</span>
                <p class="main-event-region-p">Регион:</p><span class="main-event-region">{{ event.region }}</span>
                <p class="main-event-address-p">Адрес:</p><span class="main-event-address">{{ event.address }}</span>
                <p class="main-event-date-p">Дата:</p><span class="main-event-date">{{formatDate(event.date) }}</span>
                <p class="main-event-time-p">Время:</p><span class="main-event-time">{{ event.time }}</span>
                <p class="main-event-type-p">Тип:</p><span class="main-event-type">{{ event.type }}</span>
                <p class="main-event-price-p">Цена:</p><span class="main-event-price">{{formatPrice(event.price) }}</span>
              </div>

            </div>
          </div>
            <div class="descr-div">
              <p class="descr-p">Описание:</p>
              <span class="descr"> {{ event.description }}</span>
            </div>
          <div class="comments">
            <div class="comments-header-div"><span class="comments-header">Комментарии:</span></div>

            <div class="comment-div">
              <div class="comment-avatar">
                <div class="avatar-img"></div>
              </div>
              <div class="write-comment">
                <input type="text">
              </div>
              <div class="send-comment"><span>Отправить</span></div>
            </div>

            <div class="someone-comment-div"
            v-for="comment in Comments"
            v-bind:key="comment.id"
            >
              <div class="someone-comment-avatar">
                <div class="someone-avatar-img"></div>
              </div>
              <div class="someone-comment"><span>{{ comment.comment }}</span></div>
            </div>
            
          </div>
        </div>
      </div>

    </template>

<script>
import axios from 'axios';

export default {
  name: 'EventView',
  data() {
    return {
      event: {},
      Comments: {},
      nameEvent: "",

    }
  },
  mounted() {
    this.getEvent();
    this.getComment();
    document.title = 'Loading...';
  },
  methods: {
    async getEvent() {
      const eventId = this.$route.params.id;
      try {
        const response = await axios.get(`/api/v1/events/${eventId}/`);
        this.event = response.data;
        this.nameEvent = response.data.name;
        document.title = this.nameEvent;
        console.log("Detail data: ", response.data);
      } catch (error) {
        console.error("An error occurred: ", error);
      }
    },

    async getComment() {
      const eventId = this.$route.params.id;
      try {
        const response = await axios.get(`/api/v1/events/${eventId}`);
        this.Comments = response.data.comments
        console.log("Comments response: ", response.data.comments);
      } catch (error) {
        console.error("An error occurred: ", error);
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
        window.location.href = eventId;
      } catch {
        console.error("An error occurred: ", error); 
      }
    },
    // previous() {
    //   try {
    //     this.$router.go(-1);
    //   } catch {
    //     console.error("An error occurred: ", error); 
    //   }
    // }
  }
}
</script>



<style>
@import '../components/css/main.css';
</style>
