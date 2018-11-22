new Vue({
    el: '#app',
    data() {
        return {
            profile: true,

            currentUser: "Safal Lamsal", //logged in user

            selectedUser: "Safal Lamsal", //selected user for display
            selectedBio: "Hey my name is Safal Lamsal and this is my profile.",

            newPost: "",

            likeCount: 15,
            commentCount: 5,

            likes: [1, 2, 3, 4, 5]
        }
    }

});