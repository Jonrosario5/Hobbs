$(document).ready(function () {
    console.log('hi')
    $('#user_hobbies_button').click(function(){
        console.log('hi')
        $(".user_events_list").hide()
        $(".user_hobbies_list").show()
    })

    $("#user_events_button").click(function(){
        console.log('hi')
        $(".user_hobbies_list").hide()
        $(".user_events_list").show()
    })
})