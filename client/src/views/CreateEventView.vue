<template>
    <section class="create-event-section">
        <div class="container">
            <form @submit.prevent="createForm" class="create-event-form">
                <div class="create-event-info">
                    <div class="create-event-name-div">
                        <span>Название: </span>
                        <input type="text" class="create-event-name" v-model="name" maxlength="150">
                    </div>
                    <div class="create-event-img-div">
                        <span>Изображение-обложка:</span>
                        <input type="file" class="create-event-img" @change="onFileChange">
                    </div>
                    <div class="create-event-des-div">
                        <span>Описание:</span>
                        <input type="text" v-model="des" maxlength="2500" minlength="50" class="create-event-des">
                    </div>

                    <div class="create-event-region-div">
                        <span>Регион:</span>
                        <select v-model="region">
                            <option value="default">-</option>
                            <option value="Бишкек">Бишкек</option>
                            <option value="Чуй">Чуй</option>
                            <option value="Талас">Талас</option>
                            <option value="Иссык-Куль">Иссык-Куль</option>
                            <option value="Жалал-Абад">Жалал-Абад</option>
                            <option value="Нарын">Нарын</option>
                            <option value="Ош">Ош</option>
                            <option value="Баткен">Баткен</option>
                        </select>
                    </div>

                    <div class="create-event-address-div">
                        <span>Адрес:</span>
                        <input type="text" class="create-event-address" v-model="address">
                    </div>
                    <div class="create-event-date-div">
                        <span>Дата:</span>
                        <input type="date" class="create-event-date" v-model="date">
                    </div>
                    <div class="create-event-time-div">
                        <span>Время:</span>
                        <input type="time" class="create-event-time" v-model="time">
                    </div>
                    <div class="create-event-types-div">
                        <span>Вид мероприятия:</span>
                        <select v-model="type_of_event">
                            <option value="default">-</option>
                            <option value="Открытие">Открытие</option>
                            <option value="Выставка">Выставка</option>
                            <option value="Ярмарка">Ярмарка</option>
                            <option value="Презентация">Презентация</option>
                            <option value="Праздник">Праздник</option>
                            <option value="Пресс-мероприятие">Пресс-мероприятие</option>
                            <option value="Тренинг/семинар">Тренинг/семинар</option>
                            <option value="Фестиваль/концерт">Фестиваль/концерт</option>
                        </select>
                    </div>
                    <div class="create-event-type-div">
                        <span>Тип мероприятия:</span>
                        <select v-model="type">
                            <option value="default">-</option>
                            <option value="Вход свободный">Вход свободный</option>
                            <option value="Вход закрытый">Вход закрытый</option>
                        </select>

                    </div>
                    <div class="create-event-price-div">
                        <span>Цена за вход: </span>
                        <input type="number" v-model="price">
                    </div>

                </div>

                <div class="create-buttons">
                    <button class="create-button" type="submit">Создать</button>
                    <button class="cancel-button" @click="cancelCreate">Отмена</button>
                </div>

            </form>

        </div>
    </section>
</template>


<script>
import axios from 'axios';
import { useToast } from 'vue-toast-notification'
import axiosInstance from '../axiosSetup';


export default {
    name: 'CreateEvent',

    data() {
        return {
            name: '',
            image: null,
            des: '',
            region: 'default',
            address: '',
            date: '',
            time: '',
            type_of_event: 'default',
            type: 'default',
            price: '0',
            errors: []
        }
    },

    mounted() {
        document.title = 'Create event'
        this.$toast = useToast()
    },

    methods: {
        onFileChange(event) {
            const file = event.target.files[0];
            if (file && file.type.startsWith('image/')) {
                this.image = file;
            } else {
                this.$toast.error('Please select a valid image file.');
                this.image = null;
            }
        },


        async createForm() { 
            this.errors = [];

            if (this.name === "") {
                this.errors.push("Please write the title of the event");
                this.$toast.warning("Напишите название мероприятия")
            }

            if (!this.image) {
                this.errors.push("Please provide image")
                this.$toast.warning("Загрузите картинку")
            }

            if (this.region === 'default') {
                this.errors.push("Please select region");
                this.$toast.warning("Выберите регион")
            }

            if (!this.address) {
                this.errors.push("Please provide the address");
                this.$toast.warning("Напишите адрес")
            }

            if (!this.date) {
                this.errors.push("Please provide the date");
                this.$toast.warning("Напишите дату")
            } else {
                const today = new Date();
                const selectedDate = new Date(this.date);
                today.setHours(0, 0, 0, 0); 
                if (selectedDate < today) {
                    this.errors.push("The date cannot be in the past");
                    this.$toast.warning("Дата не может быть в прошлом");
                }
            }

            if (!this.time) {
                this.errors.push("Please provide the time");
                this.$toast.warning("Напишите время")
            }

            if (this.type_of_event === 'default') {
                this.errors.push("Please select the kind of the event");
                this.$toast.warning("Выберите вид мероприятия")
            }

            if (this.type === 'default') {
                this.errors.push("Please select the type of the event");
                this.$toast.warning("Выберите тип мероприятия")
            }

            if (!this.errors.length) {
                const formData = new FormData();
                formData.append('name', this.name);
                formData.append('image', this.image);
                formData.append('description', this.des);
                formData.append('region', this.region);
                formData.append('address', this.address);
                formData.append('date', this.date);
                formData.append('time', this.time);
                formData.append('type_of_event', this.type_of_event);
                formData.append('type', this.type);
                formData.append('price', this.price);

                try {
                    const token = localStorage.getItem('accessToken');
                    if (!token) {
                    console.error("No token found in localStorage.");
                    }

                    const response = await axiosInstance.post('/api/v1/events/', formData, {
                        headers: {
                        // "Authorization": `Bearer ${token}`,
                        "Content-Type": "multipart/form-data",
                        }
                    });
                    console.log('Response received:', response.data);
                    this.$toast.success('Event created successfully.');
                    this.$router.push('/')
                } catch (error) {
                    console.error('An error occurred:', error);
                    this.$toast.error('An error occurred while creating the event.');
                }
            }    

        },

        cancelCreate() {
            this.$router.push('/')
        }, 

    },

    components: {

    }


}




</script>



<style>
@import '../components/css/main.css';
</style>
