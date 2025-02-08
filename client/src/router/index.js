import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignupView from '../views/SignupView.vue'
import EventView from '../views/EventView.vue'
import LoginView from '../views/LoginView.vue'
import AboutView from '../views/AboutView.vue'
import ProfileView from '../views/ProfileView.vue'
import CreateEvent from '../views/CreateEventView.vue'
import ChangeEvent from '../views/ChangeEventView.vue'
import ForgotPassword from '../views/ForgotPasswordView.vue'
import Favourites from '../views/FavouriteView.vue'
import GoogleView from '@/views/GoogleView.vue'

import axios from 'axios'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView
  },
  {
    path: '/register',
    name: 'register',
    component: SignupView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
  },
  {
    path: '/events/:id',
    name: 'event',
    component: EventView,
  },
  {
    path: '/profile/:id',
    name: 'profile',
    component: ProfileView,
  },
  {
    path: '/create',
    name: 'create',
    component: CreateEvent,
  },
  {
    path: '/change/:id',
    name: 'change',
    component: ChangeEvent,
  },
  {
    path: '/forgot_password',
    name: 'forgotPassword',
    component: ForgotPassword,
  },
  {
    path: '/myfavourites',
    name: 'myfavourites',
    component: Favourites,
  },
  {
    path: '/google',
    name: 'GoogleLogin',
    component: {
      created() {
        window.location.href = `${axios.defaults.baseURL}/accounts/google/login/?next=${window.location.origin}/google-callback`;
      }
    }
  },
  {
    path: '/google-callback',
    name: 'GoogleCallback',
    component: GoogleView,
  },

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition; // Restores position when using browser back/forward
    } else {
      return { top: 0 }; // Always scrolls to top on new pages
    }
  },
});

export default router
