    <template>
      <div class="home-event">
        <div class="container">
          <div class="content">
            <div class="img-event">

              <button class="switch-btn left" @click="toggleMedia"></button>

              <template v-if="showVideo && event.video">
                <video v-bind:src="event.video" class="main-video" controls autoplay loop></video>
              </template>
              <template v-else>
                <img v-bind:src="event.image" class="main-img">
              </template>

              <button class="switch-btn right" @click="toggleMedia"></button>
              
              <div class="like-fav">
                <div class="like-div">

                  <div class="like" @click="likeHandler">
                    <img src="../../static_files/hearts.png" class="like-sign" v-if="this.LikeUser">
                    <img src="../../static_files/love.png" class="like-sign" v-else>
                  </div>
              
                    <div class="like-count">
                      <span>{{ event.likes }}</span>
                    </div>
                </div>

                <div class="favourite" @click="FavouriteHandler">
                  <img src="../../static_files/free-icon-bookmark-3983855.png" v-if="this.favourite" class="fav-sign">
                  <img src="../../static_files/free-icon-bookmark-3983871.png" v-else class="fav-sign">
                </div>
              </div>
            </div>

            <div class="main-event-name-div">
              <span class="main-event-name">{{ event.name }}</span>
            </div>

            <div class="owner-card-div">
              <div class="owner-card">
                <div class="owner-card-avatar">
                  <img v-bind:src="this.ownerAvatar" class="owner-avatar">
                </div>

                <div class="some-text">
                  <span class="main-event-owner"> {{ ownerUsernames[event.owner] }}</span>
                  <p>организатор</p>
                </div>
                
                <button @click="redicrectToUser(event.owner)" class="to-profile-button">Посмотреть профиль</button>
              </div>

              <div class="price-card">
                <div class="price-card-text">
                  <span>Вход</span>
                  <span class="price">{{ formatPrice(event.price) }}</span>
                </div>
              </div>
            </div>

            <div class="event-info-div">
              <div class="main-info">
                <div class="main-info-header">
                  <img src="../../static_files/free-icon-data-analytics-8738041.png" alt="">
                  <span>Главная информация</span>
                </div>
                <div class="main-info-content">
                  <span>{{ event.type_of_event }}</span>
                  <span>{{ event.type }}</span>
                </div>
              </div>
              
              <div class="date-and-time">
                <div class="date-and-time-header">
                  <img src="../../static_files/free-icon-time-and-date-26-9188173.png" alt="">
                  <span>Дата и время</span>
                </div>
                <div class="date-and-time-content">
                  <span>{{ formatDate(event.date) }}</span>
                  <span>{{ event.time }}</span>
                </div>
              </div>
              
              <div class="location">
                <div class="location-header">
                  <img src="../../static_files/free-icon-location-pin-1201684.png" alt="">
                  <span>Локация</span>
                </div>
                <div class="location-content">
                  <span>{{ event.region }}</span>
                  <span>{{ event.address }}</span>
                </div>
              </div>

            </div>

            <div class="descr-div">
              <div class="descr-header">
                <img src="../../static_files/product-description.png" alt="">
                <span>Описание</span>
              </div>
              <div class="descr-content">
                <span class="descr"> {{ event.description }}</span>
              </div>
            </div>

          </div>


          <div class="comments">
            <div class="comments-header-div"><span class="comments-header">Комментарии:</span></div>

            <div class="comment-div">
              <div class="comment-avatar">
                <div class="avatar-img"> <img v-bind:src="myProfile.avatar" class="avatar-img"> </div>
              </div>
              <div class="write-comment">
                <input type="text" v-model="newComment" @keyup.enter="sendComment">
              </div>
              <button class="send-comment" @click="sendComment"><span>Отправить</span></button>
            </div>

            <div class="someone-comment-div"
            v-for="comment in Comments"
            v-bind:key="comment.id"
            >
              <div class="someone-comment-avatar" @click="redicrectToUser(comment.owner)">
                <div class="someone-avatar-img"><img v-bind:src="profile.avatar" class="someone-avatar-img-main"></div>
              </div>
              <div class="someone-comment-group">
                <div class="someone-comment-owner"><span>{{ profile.username }}</span></div>
                <div class="someone-comment"><span>{{ comment.comment }}</span></div>
              </div>
            </div>

          </div>
        </div>
      </div>

    </template>

<script>
import axios from 'axios';
import { useToast } from 'vue-toast-notification'
import axiosInstance from '@/axiosSetup';

export default {
  name: 'EventView',
  data() {
    return {
      showVideo: true,
      LikeUser: false,
      favourite: false,
      event: {
        likes: 0,
      },
      Comments: [],
      nameEvent: "",
      profile: "",
      ownerUsernames: {},
      currentUserId: localStorage.getItem('currentUserId'),
      myProfile: [],
      newComment: '',
      ownerAvatar: null,

      
    }
  },
  mounted() {
    this.getEvent();
    this.getComment();
    this.getMyProfile();
    document.title = 'Loading...';
    this.$toast = useToast()

    const eventId = this.$route.params.id;
    const userId = localStorage.getItem("currentUserId");
    const likeUserFromStorage = localStorage.getItem(`LikeUser_${userId}_${eventId}`);
    if (likeUserFromStorage !== null) {
      this.LikeUser = JSON.parse(likeUserFromStorage);
    }

    const FavFromStorage = localStorage.getItem(`favourite_${userId}_${eventId}`);
    if (FavFromStorage !== null) {
      this.favourite = JSON.parse(FavFromStorage);
    }

  },


  methods: {
    async getEvent() {
      const eventId = this.$route.params.id;
      
      try {
        const response = await axiosInstance.get(`/api/v1/events/${eventId}/`);
        this.event = response.data;
        this.nameEvent = response.data.name;
        document.title = this.nameEvent;
        console.log("Detail data: ", response.data);
        this.getOwnerUsername(this.event.owner);
      } catch (error) {
        console.error("An error occurred: ", error);
      }
    },

    async redicrectToUser(ownerEmail) {
      const response = await axiosInstance.get(`/api/v1/account/profile/`); 
      const profiles = response.data;
      const profile = profiles.filter(profile => profile.user === ownerEmail )
      this.$router.push(`/profile/${profile[0].id}/`)
    },

    async getOwnerUsername(ownerId) {
      if (!this.ownerUsernames[ownerId]) {
        try {
          const response = await axiosInstance.get(`/api/v1/account/profile/`);
          const profile = response.data.find(profile => profile.user === ownerId);
          console.log('!!!!!!!!!!!!!!!!!!!!!!!!!!1', profile)
          if (profile) {
            this.ownerUsernames[ownerId] = profile.username;
            this.ownerAvatar = profile.avatar;
          } else {
            this.ownerUsernames[ownerId] = 'Unknown';
            this.ownerAvatar = null;
          }
        } catch (error) {
          console.error("An error occurred: ", error);
          this.ownerUsernames[ownerId] = 'Error';
        }
      }
      return this.ownerUsernames[ownerId] || 'Loading...';
    },

    toggleMedia() {
      if (this.event.video) {
        this.showVideo = !this.showVideo; // Toggle between video and image
      }
    },


    async getComment() {
      const eventId = this.$route.params.id;
      try {
        const response = await axiosInstance.get(`/api/v1/events/${eventId}`);
        this.Comments = response.data.comments.reverse()
        console.log("Comments response: ", response.data.comments);
      } catch (error) {
        console.error("An error occurred: ", error);
      }

        if (this.Comments.length > 0) {
          const ownerEmail = this.Comments[0].owner;
          this.getProfileByEmail(ownerEmail); 
        }
    },

    async sendComment() {
      if (!this.newComment.trim()) {
        this.$toast.warning('Комментарий не может быть пустым');
        return;
      }

      const eventId = this.$route.params.id;
      const token = localStorage.getItem('accessToken');
      if (!token) {
        console.error("No token found in localStorage.");
        this.$toast.warning('Для начала авторизуйтесь');
        return;
      }

      try {
        const response = await axiosInstance.post(`/api/v1/events/${eventId}/comment/`, {
          comment: this.newComment
        }, {
          headers: {
            "Content-Type": "application/json"
          }
        });

        if (response.data) {
          console.log("Comment posted:", response.data);
          this.Comments.push(response.data); 
          this.newComment = ""; 
          this.getComment();
        } else {
          console.error("No data in the response.");
        }
      } catch (error) {
        console.error("An error occurred while posting the comment:", error);
        this.$toast.error('Не удалось отправить комментарий');
      }
    },

    async getMyProfile() {
      try {
        const response = await axiosInstance.get(`api/v1/account/profile/${this.currentUserId}/`)
        this.myProfile = response.data
      } catch {}
    },
    
    async getProfileByEmail(ownerEmail) {
      try {
        const response = await axiosInstance.get(`/api/v1/account/profile?email=${ownerEmail}`); 
        const profiles = response.data;
        console.log("Profile data: ", response.data);

        const profile = profiles.find(profile => profile.user === ownerEmail);
        if (profile) {
          this.profile = profile;
          console.log("Matched Profile: ", profile);
        } else {
          console.error("Profile not found for email: ", ownerEmail);
        }
      } catch (error) {
        console.error("An error occurred: ", error);
      }
    },

    formatDate(dateString) {
      try {
        const [year, month, day] = dateString.split('-');
        return `${day}/${month}/${year}`;
      } catch (error) {
      }
    },


    formatPrice(priceString) {
      try {

        if (priceString === null) {
          return "Бесплатно";
        } 
        else if (priceString == 0) {
          return "Бесплатно";
        } 
        else {
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

    async likeHandler() {
      const eventId = this.$route.params.id;
      const userId = localStorage.getItem("currentUserId");
      const token = localStorage.getItem("accessToken");
      if (!token) {
        console.error("No token found in localStorage.");
        this.$toast.warning('Для начало авторизуйтесь');
        return;
      }

      try {
        const response = await axiosInstance.post(`/api/v1/events/${eventId}/like/`, {}, {
          headers: {
            // "Authorization": `Bearer ${token}`,
          },
        });
        
        if (!response) {
          return
        } 
        
        if (response.data.includes('поставили лайк')) {
          this.event.likes += 1;
          this.LikeUser = true;
          // localStorage.setItem(`LikeUser_${eventId}`, JSON.stringify(this.LikeUser));

        } else if (response.data.includes('убрали лайк')) {
          this.event.likes -= 1;
          this.LikeUser = false;
          // localStorage.setItem(`LikeUser_${eventId}`, JSON.stringify(this.LikeUser));
        }    
        else {
          console.error("No data in the response.");
        }
        
        localStorage.setItem(`LikeUser_${userId}_${eventId}`, JSON.stringify(this.LikeUser));

      } catch (error) {
        console.log("token: ", token);
        console.error("An error occurred: ", error);
        this.$toast.warning('Для начало авторизуйтесь');
      }
    },

    async FavouriteHandler() {
      const eventId = this.$route.params.id;
      const userId = localStorage.getItem("currentUserId");
      const token = localStorage.getItem("accessToken");
      if (!token) {
        console.error("No token found in localStorage.");
        this.$toast.warning('Для начало авторизуйтесь');
        return;
      }

      try {
        const response = await axiosInstance.post(`/api/v1/events/${eventId}/favourite/`, {}, {
          headers: {
            // "Authorization": `Bearer ${token}`,
          },
        });

        console.log('FFFFFFFFFFFFFFFFFFF', response.data)
        
        if (!response) {
          return
        } 
        
        if (response.data.includes('Сохранены')) {
          this.favourite = true;
          // localStorage.setItem(`favourite_${eventId}`, JSON.stringify(this.favourite));

        } else if (response.data.includes('Удалены')) {
          this.favourite = false;
          // localStorage.setItem(`favourite_${eventId}`, JSON.stringify(this.favourite));
        }
        else {
          console.error("No data in the response.");
        }

        localStorage.setItem(`favourite_${userId}_${eventId}`, JSON.stringify(this.favourite));


      } catch (error) {
        console.log("token: ", token);
        console.error("An error occurred: ", error);
        this.$toast.warning('Для начало авторизуйтесь');
      }
    },


  },

  //   created() {
  //   const likeUser = localStorage.getItem('LikeUser');
  //   if (likeUser !== null) {
  //     this.LikeUser = JSON.parse(likeUser);
  //   }

  //   const favouriteUser = localStorage.getItem('FavouriteUser');
  //   if (favouriteUser !== null) {
  //     this.favourite = JSON.parse(favouriteUser);
  //   }
  // },


}

</script>



<style>
@import '../components/css/main.css';
</style>
