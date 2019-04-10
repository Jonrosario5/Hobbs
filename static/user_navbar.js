$(document).ready(function () {
    console.log('hi')
    $('#user_hobbies_button').click(function(){
        console.log('hi')
        $(".user_events_list").hide()
        $(".user_followers").hide()
        $(".user_followings").hide()
        $(".user_hobbies_list").show()
    })

    $("#user_events_button").click(function(){
        console.log('hi')
        $(".user_hobbies_list").hide()
        $(".user_followers").hide()
        $(".user_followings").hide()
        $(".user_events_list").show()
    })

    $("#user_followers_display_button").click(function(){
        console.log('hi')
        $(".user_hobbies_list").hide()
        $(".user_events_list").hide()
        $(".user_followings").hide()
        $(".user_followers").show()
    })
    $("#user_followings_display_button").click(function(){
        console.log('hi')
        $(".user_hobbies_list").hide()
        $(".user_events_list").hide()
        $(".user_followers").hide()
        $(".user_followings").show()
    })

})
