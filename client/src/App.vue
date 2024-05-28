
 <template>
  <div class="app">
    <nav class="nav">
      <div class="container">
        <div class="nav-menu">
          <router-link class="home-link" to="/"><i>Events.kg</i></router-link>
          <router-link to="" v-if="isAuthenticated" class="router-create"><p class="create">Создать</p></router-link>
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
            <li class="nav__list-item-auth">
              <span class="nickname">{{ userNickname }}</span>
            </li>
            <li class="nav__list-item">
              <button class="sign" @click="logout">logout</button>
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
              <p>wertyuiolkjhgf sdfghjkgf ffsdf dfsfsdf gdfgdfgdfg dsfdfdsfs gsgdsf</p>
            </div>
            <div class="footer-section">
              <h3>Quick Links</h3>
              <ul>
                <li><router-link to="/">Home</router-link></li>
                <li><router-link to="/about">About</router-link></li>
                <!-- <li><router-link to="/contact">Contact</router-link></li> -->
              </ul>
            </div>
            <div class="footer-section">
              <h3>Contact Us</h3>
              <p class="contact">Email: dcabatar@gmail.com</p> 
              <p class="contact">Phone: +996 995 75 07 07</p>
              <a href="https://www.instagram.com/danc_iiik/" class="media"><img src="../static_files/free-icon-social-12940260.png" alt="" class="logo-contact"></a>
              <a href=" https://t.me/danchiiiiik/" class="media"><img src="../static_files/free-icon-telegram-logo-87413.png" alt="" class="logo-contact"></a>
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

export default {
  
  computed: {
    ...mapGetters(['isAuthenticated', 'userNickname']),
    showNav() {
      return this.$route.path !== '/register' && this.$route.path !== '/login';
    },

  },
  methods: {
    ...mapActions(['logout'])

  },
  components: {
   
  }

}
</script>

<style>
@import './components/css/main.css';
</style>




