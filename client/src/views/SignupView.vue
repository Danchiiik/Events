<template>
    <section class="register-section">
        <div class="container">
            <div class="register-form" v-if="!IsRegistered">
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

            <div class="register-form" v-else>
                <p class="registered-text">
                    Вы успешно зарегестрировались! Пожалуйста проверьте свою почту для дальнейших действий
                </p> 
            </div>
        </div>
    </section>
</template>

<script>
import axios from 'axios'
import { useToast } from 'vue-toast-notification'

// Vue.use(Toast, {
//   transition: "Vue-Toastification__bounce",
//   maxToasts: 20,
//   newestOnTop: true
// });

export default {
    name: "SignUpView",
    data() {
        return {
            email: "",
            password: "",
            password2: "",
            IsRegistered: false,
            errors: []
        }
    },
    mounted() {
        document.title = "Events.kg"
        this.$toast = useToast()
    },
    methods: {
        submitForm() {
            this.errors = []

            if (this.email === "") {
                this.errors.push("The email is missing")
                this.$toast.warning("The 'email' field is empty")
            }

            if (!this.email.includes("@")) {
                this.errors.push("Please write email correctly")
                this.$toast.warning("Please write email correctly")
            }

            if (this.password === "") {
                this.errors.push("The password is missing")
                this.$toast.warning("The 'password' fields is empty")

            }

            if (this.password2 !== this.password) {
                this.errors.push("The password does not match")
                this.$toast.warning("Passwords didn't match")
            }

            if (this.password.length < 8) {
                this.errors.push("The password is too small")
                this.$toast.warning("Password cannot be less then 6 characters")
            }

            if (!this.errors.length) {
                const formData = {
                    email: this.email,
                    password: this.password,
                    password2: this.password2
                }

                axios
                .post("api/v1/account/register/", formData)
                .then(response => {
                    this.IsRegistered =true
                    this.$toast.success("Account registered successfully!")
                    console.log(response.data)
                })
                .catch(errors => {
                    if (errors.response) {
                        for (const property in errors.response.data) {
                            this.errors.push(`${property}: ${errors.response.data[property]}`)
                        }

                        console.log(JSON.stringify(errors.response.data))
                    } else if (errors.message) {
                        this.errors.push("Something went wrong, please try again")
                        this.$toast.warning("Something went wrong, please try again")
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
