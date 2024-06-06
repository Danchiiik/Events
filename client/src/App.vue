
 <template>
  <div class="app">
    <nav class="nav">
      <div class="container">
        <div class="nav-menu">
          <div class="home-link-div">
            <router-link class="home-link" to="/"><i>Events.kg</i></router-link>
            <router-link to="" v-if="isAuthenticated" class="router-create"><p class="create">Создать</p></router-link>
          </div>
          <ul class="nav__list" v-if="showNav && !isAuthenticated">
            <li class="nav__list-item">
              <router-link to="/register">
                <button class="sign">sign up</button>
              </router-link>
            </li>
            <li class="nav__list-item">
              <router-link to="/login">
                <button class="sign">login</button>
              </router-link>
            </li>
          </ul>
          <ul class="nav__list" v-if="isAuthenticated">
              <li class="nav__list-item-auth" @click="redirectToProfile">
                <span class="nickname">{{ UserName }}</span>
              </li>
  
            <li class="nav__list-item">
              <button class="sign" @click="handleLogout">logout</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <section class="events">
      <router-view/>
      
    </section>

    <div class="footer-wrapper">
      <footer class="footer">
          <div class="container">
            <div class="footer-content">
              <div class="footer-section">
              <h3>About Us</h3>
              <p><b><i>Events.kg</i></b> - это ведущая платформа для организации и посещения мероприятий в Кыргызстане. Мы стремимся создать пространство, где каждый может найти интересные и актуальные события в своем регионе.</p>
            </div>
            <div class="footer-section">
              <h3>Quick Links</h3>
              <ul>
                <li><router-link to="/">Home</router-link></li>
                <li><router-link to="/about">About</router-link></li>
              </ul>
            </div>
            <div class="footer-section">
              <h3>Contact Us</h3>
              <p class="contact">Email: dcabatar@gmail.com</p> 
              <p class="contact">Phone: +996 995 75 07 07</p>
              <a href="https://www.instagram.com/danc_iiik/" class="media" target="_blank"><img src="../static_files/free-icon-social-12940260.png" alt="" class="logo-contact"></a>
              <a href=" https://t.me/danchiiiiik/" class="media" target="_blank"><img src="../static_files/free-icon-telegram-logo-87413.png" alt="" class="logo-contact"></a>
            </div>
          </div>
          <div class="footer-bottom">
            <p>&copy; 2024 Events.kg | All Rights Reserved</p>
          </div>
        </div>
      </footer>
    </div>

  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import axios from 'axios';

export default {

  data() {
    return {
      Profile: null,
      error: null,
      UserName: '',
      currentUserId: localStorage.getItem('currentUserId')
    }
  },
  
  computed: {
    ...mapGetters(['isAuthenticated', 'userNickname']),
    showNav() {
      return this.$route.path !== '/register' && this.$route.path !== '/login';
    },
  },


  methods: {
    ...mapActions(['logout']),

    handleLogout() {
      this.logout();
      this.$router.push('/');
    },

    async getProfile() {
      this.loading = true;
      try {
        const response = await axios.get(`/api/v1/account/profile/`);
        const filteredResponse = response.data.filter(profile => profile.id == this.currentUserId);

        if (filteredResponse.length > 0) {
          this.Profile = filteredResponse[0];

        const response = await axios.get(`/api/v1/account/profile/${this.Profile.id}/`)
        this.UserName = response.data.username

        } else {
          this.Profile = null;
        }
        console.log("Filtered Profiles response: ", filteredResponse);
      } catch (error) {
        this.error = error;
        console.error("An error occurred: ", error);
      } finally {
        this.loading = false;
      }
    },


    redirectToProfile() {
      if (this.Profile && this.Profile.id) {
        this.$router.push(`/profile/${this.Profile.id}/`);
      } else {
        console.error("Profile not found");
      }
    },

  },
  components: {

  },

  mounted() {
    this.getProfile()
  },

}
</script>

<style>
@import './components/css/main.css';
</style>




