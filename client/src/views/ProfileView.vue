<template>
    <section class="profile-section">
        <div class="container">
            <div class="profile-div">
                <div class="avatar-div" v-if="LookingProfile">
                    <img v-bind:src="profile.avatar" class="profile-avatar">  
                </div>
                <div class="profile-info-div" v-if="LookingProfile">
                    <div class="profile-main-info-div">
                        <div class="profile-email">
                            <span class="profile-email-h">Почта:</span> 
                            <span class="profile-email-t">{{ profile.user }}</span>
                        </div>
                        <div class="profile-username">
                            <span class="profile-username-h">Никнейм:</span>
                            <span class="profile-username-t"> {{ profile.username }}</span>
                        </div>
                        <div class="profile-url">
                            <span class="profile-url-h">Ссылка:</span>
                            <span class="profile-url-t">
                              <a v-if="profile.url" :href="profile.url" target="_blank">{{ urlCheck(profile.url) }}</a>
                              <span v-else>{{ urlCheck(profile.url) }}</span>
                            </span>
                        </div>
                        <div class="profile-des">
                            <span class="profile-des-h">Описание:</span>
                            <span class="profile-des-t">{{ profile.description}}</span>
                        </div>
                    </div>

                    <div class="profile-button-div" v-if="IsProfileOwner">
                        <button class="change-profile" @click="editMode = true">Изменить профиль</button>
                    </div>
                </div>

                <div v-if="editMode" class="edit-profile-form">
                    <form @submit.prevent="updateProfile">
                    <div class="change-avatar">
                        <label for="avatar">Avatar image:</label>
                        <input type="file" accept="image/" @change="handleAvatar" id="avatar">
                    </div>
                    <div class="change-username">
                        <label for="username">Username:</label>
                        <input type="text" maxlength="100" v-model="editProfile.username" id="username">
                    </div>
                    <div class="change-url">
                        <label for="url">URL:</label>
                        <input type="text" v-model="editProfile.url" id="url">
                    </div>
                    <div class="change-des">
                        <label for="description">Description:</label>
                        <input type="text" v-model="editProfile.description" id="description">
                    </div>
                    <div class="change-buttons">
                        <button class="change-buttons-save" type="submit">Save</button>
                        <button class="change-buttons-cancel" type="button" @click="editMode = false">Cancel</button>
                    </div>
                    </form>
                </div>

            </div>

            <div class="profile-event-div">
                <div class="profile-event-h">
                    <p>Мероприятии пользователя</p>
                </div>                
                <div class="profile-event-main">
                    <div class="profile-event-card" 
                        v-for="event in Events"
                        v-bind.key="event.id">
                    
                        <img v-bind:src="event.image" class="profile-event-img">
                        <div class="profile-event-name">
                            <span>{{ formatName(event.name) }}</span>
                        </div>
                        <div class="profile-event-type">
                            <span>{{ event.type_of_event }}</span>
                        </div>

                        <div class="profile-event-card-buttons" v-if="IsProfileOwner">
                                <button class="profile-event-del">Удалить</button>
                                <button class="profile-event-ch">Изменить</button>
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
    name: 'ProfileView',
    data() {
        return {
            profile: {},
            nameProfile: "",
            Events: [],
            currentUserId: parseInt(localStorage.getItem('currentUserId')),
            editProfile: {
                avatar: null,
                username: '',
                url: '',
                description: ''
            },
            editMode: false,
        }
    },

    mounted() {
        document.title = "Profile",
        this.getProfile(),
        this.getEvent()
    },

    computed: {
        IsProfileOwner() {
            return this.profile.id === this.currentUserId;
        },

        LookingProfile() {
            if (this.editMode === false) {
                return true
            }
        }

    },

    methods: {

    async getEvent() {
        const profileId = this.$route.params.id;
      try {
        const response = await axios.get("/api/v1/events/");
        const user = await axios.get(`api/v1/account/profile/${profileId}/`);
        const filtered = response.data.results.filter(event => event.owner == user.data.user);

        this.Events = filtered;
        console.log("Events response: ", filtered);
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


    async getProfile() {
      const profileId = this.$route.params.id;
      
      try {
        const response = await axios.get(`/api/v1/account/profile/${profileId}/`)
        this.profile = response.data;
        this.nameProfile = response.data.username;
        this.editProfile = { ...response.data };
        document.title = this.nameProfile;
        console.log("Profile data: ", response.data);
      } catch (error) {
        console.error("An error occurred: ", error);
      }
    },

    async updateProfile() {
    const token = localStorage.getItem('accessToken');
    if (!token) {
      console.error("No token found in localStorage.");
    }

    try {
      const formData = new FormData();
      formData.append('username', this.editProfile.username);
      formData.append('description', this.editProfile.description);
      if (this.editProfile.url) {
        formData.append('url', this.editProfile.url);
      } else {
        formData.append('url', '')
      }
      if (this.editProfile.avatar) {
        console.log('AAAAAAAAAAAAAAAAAAAAAa', this.editProfile.avatar)

        if (typeof this.editProfile.avatar === 'string'){
            fetch(this.editProfile.avatar)
                .then(response => response.blob())
                .then(blob => {
                    const file = new File([blob], 'avatar.jpg', { type: 'image/jpeg' });
                    console.log("File:", file);
                    formData.append('avatar', file);
              })
              .catch(error => console.error('Error fetching the avatar:', error));
            }
          else {
            console.log("ELSEEEEEEEEEEEEE", this.editProfile.avatar)
            formData.append('avatar', this.editProfile.avatar)
          }}
          

      const response = await axios.patch(`/api/v1/account/profile/${this.profile.id}/`, formData, {
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "multipart/form-data"
        }
      });
      this.profile = response.data;
      this.editMode = false;
      console.log("Profile updated: ", response.data);
    } catch (error) {
      console.error("An error occurred while updating the profile: ", error);
    }
    },

    handleAvatar(avatar) {
      const file = avatar.target.files[0];
      console.log("FILEEEEEEEEEEEEEE", file)
      if (file) {
        this.editProfile.avatar = file;
      } 
    },

    urlCheck(url){
        if (url === ''){
            return "--------------"
        } else {
          return url
        }
        
    },

    },

    components() {

    },
}

</script>



<style>
@import '../components/css/main.css';
</style>
