<template>
    <section class="register-section">
        <div class="container">
            <div class="register-form">
                    <div class="preview-text">
                        <h1 class="register-header">Sign up</h1>
                        <!-- <p class="register-description">Register to our paltform</p>    -->
                    </div>
        
                <form @submit.prevent="submitForm">
                    <div class="form">
                        <ul class="register-fields">
                            <span>Электронная почта</span>
                            <li class="li-button"><input type="text" v-model="email"></li>
                            <span>Пароль</span>
                            <li class="li-button"><input type="password" v-model="password"></li>
                            <span>Подтвердите пароль</span>
                            <li class="li-button"><input type="password" v-model="password2"></li >
                        </ul>
                        
                        <button type="submit" class="signup-button">Sign up</button>
                    </div>
                </form>

                <div class="login-div">
                    <span>У вас уже есть аккаунт?</span>
                    <router-link to="/login">
                        <button class="login-button">Login</button>
                    </router-link>
                    
                </div>

            </div>
        </div>
    </section>
</template>

<script>
import axios from 'axios'

export default {
    name: "SignUpView",
    data() {
        return {
            email: "",
            password: "",
            password_confirm: "",
            errors: []
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

            if (this.password2 !== this.password) {
                this.errors.push("The password does not match")
            }

            if (!this.errors.length) {
                const formData = {
                    email: this.email,
                    password: this.password,
                    password2: this.password2
                }

                axios
                .post("api/v1/account/register/", formData)
                .then(response => {console.log(response.data)})
                .catch(errors => {
                    if (errors.response) {
                        for (const property in errors.response.data) {
                            this.errors.push(`${property}: ${errors.response.data[property]}`)
                        }

                        console.log(JSON.stringify(errors.response.data))
                    } else if (errors.message) {
                        this.errors.push("Something went wrong, please try again")
                        console.log(JSON.stringify(errors))
                    }
                })
            }
        }
    }
}
</script>


<style>
@import '../components/css/main.css';
</style>
