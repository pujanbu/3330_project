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

            checkAdmin: false,
            pageUpdate: '0',

            likeCount: 15,
            commentCount: 5
        }
    },

    mounted() {
        this.getMainProfile();
        this.getAllPosts();
    },

    methods: {
        runAll: function () {
            // this.getMainProfile();
            this.getMainPosts();
            this.getAllPosts();
        },

        clickedHome: function () {
            this.getAllPosts();
            this.display = 'home';
        },

        userProfileClicked: function (p) {
            if (p.profile_id) {
                this.selectedProfileId = p.profile_id;
                this.display = 'user';
                this.getProfile();
                this.getPosts();
            } else {
                this.pageClicked(p.page_id)
            }
        },

        pageClicked: function (id) {
            for (let admin of this.currentUser.adminof) {
                if (admin.id == id) {
                    this.checkAdmin = true;
                    console.log(this.checkAdmin);
                }
            }

            this.selectedPageId = id;
            this.selectedProfileId = id;
            this.getPages();
            this.getPostsP();
            this.pageUpdate = '0';
            this.display = 'page';
        },

        deleteUser: function () {
            fetch(`/api/profile`, {
                    method: 'DELETE'
                })
                .then(res => res.json())
                .then(data => {
                    console.log(data);
                    if (data.success) {
                        location.reload()
                    }
                })
                .catch(err => console.error(err));
        },

        updatePageC: function (id) {
            this.pageUpdate = '1';
            this.selectedPageId = id;
            this.getPages();
        },

        updatePage: function () {
            fetch(`/api/page`, {
                    method: 'UPDATE',
                    body: JSON.stringify({
                        page_id: this.selectedPageId,
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
                    this.updatePage = '0';
                    this.getMainProfile();
                })
                .catch(err => {
                    console.error(err);
                });
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

        getPostsP: function () {
            fetch(`/api/post?page_id=${this.selectedPageId}`)
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

        postItP: function () {
            fetch(`/api/post`, {
                    method: 'POST',
                    body: JSON.stringify({
                        type: 'text',
                        body: this.newPost,
                        page_id: this.selectedPageId,
                    }),
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    }
                })
                .then(res => res.json())
                .then(data => {
                    console.log(data);
                    this.getPostsP();
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
                    this.getMainProfile();
                })
                .catch(err => {
                    console.error(err);
                });

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