<template>
    <section class="login-section">
        <div class="container">
            <div class="login-form">
                <div class="preview-text">
                    <h1 class="login-header">Login</h1>
                </div>
        
                <form @submit.prevent="submitForm" class="main-form">
                    <div class="form">
                        <ul class="login-fields">
                            <span>Электронная почта</span>
                            <li class="li-button"><input type="text" v-model="email"></li>
                            <span>Пароль</span>
                            <li class="li-button"><input type="password" v-model="password"></li>
                        </ul>
                        
                        <div class="login-buttons">
                            <button type="submit" class="login-button">Login</button>
                            <router-link to="/google">
                                <button type="submit" class="google-button">Google</button>
                            </router-link>
                        </div>
                    </div>

                    <div class="add-form">
                        <div class="register-div">
                            <span class="register-text">Не зарегистрированы?</span>
                            <router-link to="/register">
                                <button class="register-button">Sign up</button>
                            </router-link>
                        </div>
                            
                        <router-link to="/forgot_password">
                        <div class="forgot-password-div">
                                <span class="forgot-password">Забыли пароль?</span>
                            </div>
                        </router-link>
                    </div>

                </form>


            </div>
        </div>
    </section>
</template>

<script>
import axios from 'axios';
import axiosInstance from '@/axiosSetup';
import { mapActions } from 'vuex';
import { useToast } from 'vue-toast-notification'

export default {
    name: "LoginView",
    data() {
        return {
            email: "",
            password: "",
            errors: [],
        }
    },
    mounted() {
        document.title = "Events.kg"
        this.$toast = useToast()  
    },
    methods: {
        ...mapActions(['login']),
        async submitForm() { 
            this.errors = [];

            if (this.email === "") {
                this.errors.push("The email is missing");
                this.$toast.warning("The 'email' field is empty")
            }

            if (!this.email.includes("@")) {
                this.errors.push("Please write email correctly")
                this.$toast.warning("Please write email correctly")
            }

            if (this.password === "") {
                this.errors.push("The password is missing");
                this.$toast.warning("The 'password' fields is empty")
            }

            if (!this.errors.length) {
                const formData = {
                    email: this.email,
                    password: this.password,
                };

                try {
                    const response = await axiosInstance.post("/api/v1/account/login/", formData); 
                    console.log("Response received:", response.data);


                    if (response.data && response.data.access && response.data.refresh) {
                        const { access, refresh} = response.data;
                        console.log("Access Token:", access);
                        console.log("Refresh Token:", refresh);
                    
                        await this.getProfileByEmail(this.email); 
                        const userNickname = this.profile.username;

                    const profileResponse = await axiosInstance.get(`/api/v1/account/profile/`);
                    const profiles = profileResponse.data;
                    const filteredResponse = profiles.filter(profile => profile.user === this.email)
                    const profileID = filteredResponse[0].id

                        this.login({
                            accessToken: access,
                            refreshToken: refresh,
                            userNickname: userNickname,
                            currentUserId: profileID,
                        });

                        this.$router.push('/');
                    } else {
                        this.errors.push("Invalid response format");
                    }
                } catch (error) {
                    if (error.response) {
                        for (const property in error.response.data) {
                            this.errors.push(`${property}: ${error.response.data[property]}`);
                        }
                        this.$toast.warning("Нет такого зарегестрированного пользователя")
                        console.log("Error response data:", JSON.stringify(error.response.data));
                    } else if (error.message) {
                        this.errors.push("Something went wrong, please try again");
                        console.log("Error message:", JSON.stringify(error));
                    }
                }
            }
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
        }
    }
}
</script>

<style>
@import '../components/css/main.css';
</style>
