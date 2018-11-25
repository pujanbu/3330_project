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

            selectedProfileId: 0,

            selectedPage: {},
            selectedPageId: 0,

            selectedPage: "Hamro Page",
            selectedBio: "Hey my name is Safal Lamsal and this is my profile.",

            newPost: "",

            //PAGE
            newPageName: "",
            newPageDes: "",
            newPageCat: "",

            likeCount: 15,
            commentCount: 5
        }
    },

    mounted() {
        this.getMainProfile();
    },

    methods: {
        runAll: function () {
            // this.getMainProfile();
            this.getMainPosts();
            this.getAllPosts();
        },

        userProfileClicked: function (id) {
            this.selectedProfileId = id;
            this.display = 'user';
            this.getProfile();
            this.getPosts();
        },

        getMainProfile: function () {
            fetch(`/api/profile`)
                .then(res => res.json())
                .then(data => {
                    console.log(data);
                    if (data.success) {
                        this.currentUser = data.profile;
                        this.selectedProfileId = data.profile.id;
                        this.runAll();
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
                        this.currentUserPosts = data.posts;
                    }
                })
                .catch(err => console.error(err));
        },

        getPosts: function () {
            fetch(`/api/post?profile_id=${this.selectedProfileId}`)
                .then(res => res.json())
                .then(data => {
                    console.log(data);
                    if (data.success) {
                        this.selectedUserPosts = data.posts;
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
                        this.allUserPosts = data.posts;
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

        postIt: function () {
            fetch(`/api/post`, {
                    method: 'POST',
                    body: JSON.stringify({
                        type: 'text',
                        body: this.newPost,
                    }),
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    }
                })
                .then(res => res.json())
                .then(data => {
                    console.log(data);
                    this.getMainPosts();
                })
                .catch(err => console.error(err));
        },

        createPage: function () {
            fetch(`/api/page`, {
                    method: 'POST',
                    body: JSON.stringify({
                        name: this.newPageName,
                        desc: this.newPageDes,
                        category: this.newPageCat,
                    }),
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    }
                })
                .then(res => res.json())
                .then(data => {
                    console.log(data);
                })
                .catch(err => console.error(err));

        },

        getPages: function () {
            fetch(`/api/page?page_id=${this.selectedPageId}`)
                .then(res => res.json())
                .then(data => {
                    console.log(data);
                    if (data.success) {
                        this.selectedPage = data.page;
                    }
                })
                .catch(err => console.error(err));
        }

    }

});