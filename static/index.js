new Vue({
    el: '#app',
    data() {
        return {
            display: "profile",

            currentUser: {}, //logged in user

            currentUserPosts: {},

            selectedUser: {}, //selected user for display
            selectedUserPosts: {},

            allUserPosts: {},

            selectedProfileId: 1,

            selectedPage: "Hamro Page",
            selectedBio: "Hey my name is Safal Lamsal and this is my profile.",

            newPost: "",

            likeCount: 15,
            commentCount: 5
        }
    },

    mounted() {
        this.getMainProfile();
        this.selectedProfileId = currentUser.id;
        this.getMainPosts();
        // this.getPost();
    },

    methods: {
        getMainProfile: function () {
            fetch(`/api/profile`)
                .then(res => res.json())
                .then(data => {
                    console.log(data);
                    if (data.success) {
                        this.currentUser = data.profile;
                    }
                })
                .catch(err => console.error(err));
        },

        getMainPosts: function () {
            fetch(`/api/post?profile_id=${this.selectedProfileId}`)
                .then(res => res.json())
                .then(data => {
                    console.log(data);
                    if (data.success) {
                        this.currentUserPosts = data.profile;
                    }
                })
                .catch(err => console.error(err));
        },

        getAllPosts: function () {
            fetch(`/api/post`)
                .then(res => res.json())
                .then(data => {
                    console.log(data);
                    if (data.success) {
                        this.allUserPosts = data.profile;
                    }
                })
                .catch(err => console.error(err));
        },

        getProfile: function () {
            fetch(`/api/profile?profile_id=${this.selectedProfileId}`)
                .then(res => res.json())
                .then(data => {
                    console.log(data);
                    if (data.success) {
                        this.selectedUser = data.profile;
                    }
                })
                .catch(err => console.error(err));
        },

        getPost: function () {
            fetch(`/api/post?profile_id=${this.selectedProfileId}`)
                .then(res => res.json())
                .then(data => {
                    console.log(data);
                    if (data.success) {
                        this.profilePosts = data.posts;
                    }
                })
                .catch(err => console.error(err));
        },

        postIt: function () {

        }

    }

});