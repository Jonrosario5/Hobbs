$(document).ready(function () {
    console.log('hi')
    $('#edit_user_details').click(function(){
        $(".add_hobbies").hide()
        $(".edit_form").show()
    })
    $('#add_hobbies_button').click(function(){
        $(".edit_form").hide()
        $(".add_hobbies").show()
    })
})