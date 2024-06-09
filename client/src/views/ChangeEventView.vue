<template>
    <section class="change-event-section">
        <div class="container">
            <form @submit.prevent="updateEvent" class="change-event-form">
                <div class="change-event-info">
                    <div class="change-event-name-div">
                        <span>Название: </span>
                        <input type="text" class="change-event-name" v-model="editEvent.name">
                    </div>
                    <div class="change-event-img-div">
                        <span>Изображение-обложка:</span>
                        <input type="file" class="change-event-img" @change="onFileChange">
                    </div>
                    <div class="change-event-des-div">
                        <span>Описание:</span>
                        <input type="text" v-model="editEvent.description" maxlength="1500" minlength="50" class="change-event-des">
                    </div>

                    <div class="change-event-region-div">
                        <span>Регион:</span>
                        <select v-model="editEvent.region">
                            <!-- <option value="default">-</option> -->
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

                    <div class="change-event-address-div">
                        <span>Адрес:</span>
                        <input type="text" class="chnage-event-address" v-model="editEvent.address">
                    </div>
                    <div class="change-event-date-div">
                        <span>Дата:</span>
                        <input type="date" class="chnage-event-date" v-model="editEvent.date">
                    </div>
                    <div class="change-event-time-div">
                        <span>Время:</span>
                        <input type="time" class="change-event-time" v-model="editEvent.time">
                    </div>
                    <div class="change-event-types-div">
                        <span>Вид мероприятия:</span>
                        <select v-model="editEvent.type_of_event">
                            <!-- <option value="default">-</option> -->
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
                    <div class="change-event-type-div">
                        <span>Тип мероприятия:</span>
                        <select v-model="editEvent.type">
                            <!-- <option value="default">-</option> -->
                            <option value="Открытый">Открытый</option>
                            <option value="Закрытый">Закрытый</option>
                        </select>

                    </div>
                    <div class="change-event-price-div">
                        <span>Цена за вход: </span>
                        <input type="number" v-model="editEvent.price">
                    </div>
                </div>


                <div class="change-buttons">
                    <button class="change-button" type="submit">Сохранить</button>
                    <button class="change-cancel" @click="cancelChange">Отмена</button>
                </div>
            </form>

        </div>
    </section>
</template>

<script>
import axios from 'axios';
import axiosInstance from '@/axiosSetup';
import { useToast } from 'vue-toast-notification'

export default {
    name: 'ChangeEvent',

    data() {
        return {
            Event: {},
            editEvent: {
                name: '',
                description: '',
                region: '',
                address: '',
                date: '',
                time: '',
                type_of_event: '',
                type: '',
                price: '',
                image: null
            },
        }
    },

    mounted() { 
        this.getEvent();
        this.$toast = useToast()
        document.title = 'Change event'
    },

    methods: {
        async getEvent() {
            const eventId = this.$route.params.id;
            try {
                const response = await axiosInstance.get(`/api/v1/events/${eventId}/`);
                this.Event = response.data
                this.editEvent = response.data; 
                console.log("Detail data: ", response.data);
            } catch (error) {
                console.error("An error occurred: ", error);
            }
        },

        async updateEvent() {

            const eventId = this.$route.params.id;
            const token = localStorage.getItem('accessToken');
            if (!token) {
            console.error("No token found in localStorage.");
            }

            try {
            const formData = new FormData();
            formData.append('name', this.editEvent.name);
            formData.append('description', this.editEvent.description);
            formData.append('region', this.editEvent.region);
            formData.append('address', this.editEvent.address);
            if (this.editEvent.date){ 
                const today = new Date();
                const selectedDate = new Date(this.editEvent.date);
                today.setHours(0, 0, 0, 0); 
                if (selectedDate < today) {
                    this.$toast.warning("Дата не может быть в прошлом");
                } else {
                    formData.append('date', this.editEvent.date);
                }
            }
                
            formData.append('time', this.editEvent.time);
            formData.append('type_of_event', this.editEvent.type_of_event);
            formData.append('type', this.editEvent.type);
            formData.append('price', this.editEvent.price);
            

            
            if (this.editEvent.image) {
                console.log('AAAAAAAAAAAAAAAAAAAAAa', this.editEvent.image)

                if (typeof this.editEvent.image === 'string'){
                    fetch(this.editEvent.image)
                        .then(response => response.blob())
                        .then(blob => {
                            const file = new File([blob], 'image.jpg', { type: 'image/jpeg' });
                            console.log("File:", file);
                            formData.append('image', file);
                    })
                    .catch(error => console.error('Error fetching the image:', error));
                    }
                else {
                    formData.append('image', this.editEvent.image)
                }}
                

            const response = await axiosInstance.patch(`/api/v1/events/${eventId}/`, formData, {
                headers: {
                // "Authorization": `Bearer ${token}`,
                "Content-Type": "multipart/form-data"
                }
            });
            this.Event = response.data;
            console.log("Event updated: ", response.data);

            const profilesResponse = await axiosInstance.get(`api/v1/account/profile/`)
            const filteredProfile = profilesResponse.data.filter(profile => profile.user === this.Event.owner)
            
            this.$router.push(`/profile/${filteredProfile[0].id}`)


            } catch (error) {
            console.error("An error occurred while updating the profile: ", error);
            }
        },  

        async cancelChange() {
            const response = await axiosInstance.get(`api/v1/account/profile/`)
            const filteredResponse = response.data.filter(profile => profile.user === this.Event.owner)
            
            this.$router.push(`/profile/${filteredResponse[0].id}`)

        },

        onFileChange(event) {
            const file = event.target.files[0];
            if (file && file.type.startsWith('image/')) {
                this.editEvent.image = file;
            } else {
                this.$toast.error('Please select a valid image file.');
                this.editEvent.image = null;
            }
        },

        
    }

}

</script>


<style>
@import '../components/css/main.css';
</style>