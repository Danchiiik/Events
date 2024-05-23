<!-- <template>
    <section class="login-section">
        <div class="container">
            <div class="login-form">
                    <div class="preview-text">
                        <h1 class="login-header">Login</h1>
                    </div>
        
                <form @submit.prevent="submitForm">
                    <div class="form">
                        <ul class="login-fields">
                            <span>Электронная почта</span>
                            <li class="li-button"><input type="text" v-model="email"></li>
                            <span>Пароль</span>
                            <li class="li-button"><input type="password" v-model="password"></li>
                        </ul>
                        
                        <button type="submit" class="signup-button">Login</button>
                    </div>
                </form>

                <div class="register-div">
                    <span>Еще не регистрировались?</span>
                    <router-link to="/register">
                        <button class="register-button">Sign up</button>
                    </router-link>
                    
                </div>

            </div>
        </div>
    </section>
</template>


<script>
import axios from 'axios'

export default {
    name: "LoginView",
    data() {
        return {
            email: "",
            password: "",
            errors: [],
            accessToken: "",
            refreshToken: ""
        }
    },
    mounted() {
        document.title = "Events.kg"
    },
    methods: {
        submitForm() {
            this.errors = []

            if (this.email === "") {
                this.errors.push("The email is missing")
            }

            if (this.password === "") {
                this.errors.push("The password is missing")
            }

            if (!this.errors.length) {
                const formData = {
                    email: this.email,
                    password: this.password,
                }

                axios
                .post("/api/v1/account/login/", formData)
                .then(response => {
                    console.log("Response received:", response);
                    if (response.data && response.data.access && response.data.refresh) {
                        this.access = response.data.access;
                        this.refresh = response.data.refresh;
                        console.log("Access Token:", this.access);
                        console.log("Refresh Token:", this.refresh);

                        localStorage.setItem('access', this.access);
                        localStorage.setItem('refresh', this.refresh);
                        
                        // Redirect to the base page
                        this.$router.push('/');


                    } else {
                        this.errors.push("Invalid response format");
                    }
                })
                .catch(errors => {
                    if (errors.response) {
                        for (const property in errors.response.data) {
                            this.errors.push(`${property}: ${errors.response.data[property]}`);
                        }

                        console.log("Error response data:", JSON.stringify(errors.response.data));
                    } else if (errors.message) {
                        this.errors.push("Something went wrong, please try again");
                        console.log("Error message:", JSON.stringify(errors));
                    }
                });
            }
        }
    }
}
</script>

<style>
@import '../components/css/main.css';
</style> -->


<template>
    <section class="login-section">
        <div class="container">
            <div class="login-form">
                <div class="preview-text">
                    <h1 class="login-header">Login</h1>
                </div>
        
                <form @submit.prevent="submitForm">
                    <div class="form">
                        <ul class="login-fields">
                            <span>Электронная почта</span>
                            <li class="li-button"><input type="text" v-model="email"></li>
                            <span>Пароль</span>
                            <li class="li-button"><input type="password" v-model="password"></li>
                        </ul>
                        
                        <button type="submit" class="signup-button">Login</button>
                    </div>
                </form>

                <div v-if="errors.length">
                    <ul>
                        <li v-for="error in errors" :key="error">{{ error }}</li>
                    </ul>
                </div>

                <div class="register-div">
                    <span>Еще не регистрировались?</span>
                    <router-link to="/register">
                        <button class="register-button">Sign up</button>
                    </router-link>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
import axios from 'axios';
import { mapActions } from 'vuex';

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
    },
    methods: {
        ...mapActions(['login']),
        submitForm() {
            this.errors = [];

            if (this.email === "") {
                this.errors.push("The email is missing");
            }

            if (this.password === "") {
                this.errors.push("The password is missing");
            }

            if (!this.errors.length) {
                const formData = {
                    email: this.email,
                    password: this.password,
                };

                axios
                .post("/api/v1/account/login/", formData)
                .then(response => {
                    console.log("Response received:", response);
                    if (response.data && response.data.access && response.data.refresh) {
                        const { access, refresh, user } = response.data;
                        console.log("Access Token:", access);
                        console.log("Refresh Token:", refresh);

                        this.login({
                            accessToken: access,
                            refreshToken: refresh,
                            userNickname: this.email
                        });
                        
                        // Redirect to the base page
                        this.$router.push('/');
                    } else {
                        this.errors.push("Invalid response format");
                    }
                })
                .catch(errors => {
                    if (errors.response) {
                        for (const property in errors.response.data) {
                            this.errors.push(`${property}: ${errors.response.data[property]}`);
                        }

                        console.log("Error response data:", JSON.stringify(errors.response.data));
                    } else if (errors.message) {
                        this.errors.push("Something went wrong, please try again");
                        console.log("Error message:", JSON.stringify(errors));
                    }
                });
            }
        }
    }
}
</script>

<style>
@import '../components/css/main.css';
</style>

