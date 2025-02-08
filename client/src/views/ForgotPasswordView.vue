<template>
    <section class="forgot-password-section">
        <div class="container">
            <div class="main-form">
                <div class="forgot-password-header">
                    <h1>Password reset</h1>
                </div>

                <form class="forgot-password-form" @submit.prevent="forgotPassword" v-if="first">
                    <div class="first-form">
                        <!-- <span>Напишите почту</span> -->
                        <input type="email" v-model="email" placeholder="Email">
                    </div>

                    <div class="first-form-button">
                        <button class="sent-button" type="submit" @click="">Отправить</button>
                    </div>
                </form>

                <form class="forgot-password-finish-form" v-if="second" @submit.prevent="forgotPasswordFinish">
                    <div class="second-form">
                        <div class="second-form-email">
                            <span>Почта:</span>
                            <span class="email-span"> {{ this.email }}</span>
                        </div>
                        <div class="second-form-code">
                            <span>Вставьте код:</span>
                            <input type="text" v-model="code">
                        </div>
                        <div class="second-form-password">
                            <span>Напишите новый пароль</span>
                            <input type="password" v-model="password">
                        </div>
                        <div class="second-form-password2">
                            <span>Подтвердите новый пароль</span>
                            <input type="password" v-model="password2">
                        </div>
                    </div>

                    <div class="second-form-button">
                        <button type="submit" class="second-sent-button">Сохранить</button>
                    </div>
                </form>
            </div>
        </div>
    </section>
</template>


<script>
import axiosInstance from '@/axiosSetup';
import { useToast } from 'vue-toast-notification';

export default {
    name: 'ForgotPassword',

    data() {
        return {
            first: true,
            second: false,
            email: '',
            password: '',
            password2: '',
            code: ''
        }
    },

    mounted() {
        document.title = 'Forgot Password'
        this.$toast = useToast()
    },

    methods: {
        async forgotPassword() {
            try{   
                if (!this.email) {
                    this.$toast.warning('Напишите почту')
                }

                if (!this.email.includes('@')) {
                    this.$toast.warning('Напишите почту правильно')
                } 
                else {

                    const formData = new FormData();
                    formData.append('email', this.email)
        
                    const response = await axiosInstance.post('api/v1/account/forgot_password/', formData, {
                        headers: {
                                // "Authorization": `Bearer ${token}`,
                                "Content-Type": "multipart/form-data",
                                }
                    })
        
                    console.log('AAAAAAAAAAA', response.data)

                    this.$toast.success('На вашу почту пришло сообщение')
                    this.first = false
                    this.second = true
                }
            } catch (error) {
                console.log('An error occured: ', error)
                if (error.response && error.response.data && error.response.data.email) {
                    this.$toast.error(error.response.data.email[0]);
                } else {
                    this.$toast.error('An error occurred while processing your request.');
                        }
                }

        },

        async forgotPasswordFinish() {
            try{   
                if (!this.code) {
                    this.$toast.warning('Вставьте код')
                }
   
                if (!this.password && !this.password2) {
                    this.$toast.warning('Напишите пароли')
                }
                
                if (this.password.length < 8) {
                    this.$toast.warning('Пароль должен быть не меньше 8 символов')
                }

                if (this.password !== this.password2) {
                    this.$toast.warning('Пароли не совпадают')   
                }

                else {

                    const formData = new FormData();
                    formData.append('email', this.email)
                    formData.append('code', this.code)
                    formData.append('password', this.password)
                    formData.append('password2', this.password2)
        
                    const response = await axiosInstance.post('api/v1/account/forgot_password_finish/', formData, {
                        headers: {
                                // "Authorization": `Bearer ${token}`,
                                "Content-Type": "multipart/form-data",
                                }
                    })
        
                    console.log('AAAAAAAAAAA', response.data)

                    this.$toast.success('Ваш пароль успешно обновлен')
                    this.$router.push('/login')
                }
                } catch (error){
                    console.log('An error occured: ', error)
                if (error.response && error.response.data) {
                } else {
                    this.$toast.error('An error occurred while processing your request.');
                        }
                }

        },
    },
}


</script>

<style>
@import '../components/css/main.css';
</style>