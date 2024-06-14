<script>
import axios from 'axios';
import axiosInstance from '@/axiosSetup';
import { mapActions } from 'vuex';

export default {
    name: 'GoogleView',

    methods: {
        ...mapActions(['login'])
    },
    
    async created() {
        try {
        const urlParams = new URLSearchParams(window.location.search);
        const accessToken = urlParams.get('access');
        const refreshToken = urlParams.get('refresh');

        if (accessToken && refreshToken) {
          localStorage.setItem('accessToken', accessToken);
          localStorage.setItem('refreshToken', refreshToken);

          axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;

          const profileResponse = await axiosInstance.get(`/api/v1/account/profile/`);
          const profiles = profileResponse.data;

          if (profiles && profiles.length > 0) {
            const userProfile = profiles[0]; 
            const userNickname = userProfile.username;
            const profileID = userProfile.id;

            await this.login({
                accessToken: accessToken,
                refreshToken: refreshToken,
                userNickname: userNickname,
                currentUserId: profileID,
            });

            this.$router.push('/').then(() => {
              window.location.reload();
            });
          } else {
            console.error('Error: User profile not found');
            this.$router.push('/login');
          }
        } else {
          console.error('Error: Tokens not found in URL parameters');
          this.$router.push('/login');
        }
      } catch (error) {
        console.error('Error processing login:', error);
        this.$router.push('/login');
      }
    },    


    mounted(){
        document.title = "Google authentication"
    }
}

</script>