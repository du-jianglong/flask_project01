$(function () {

    $(".error_toast .close").click(function () {
        $(this).parents(".error_toast").hide();
    });

    $(".error_toast .ok_btn").click(function () {
        $(this).parents(".error_toast").hide();
    });

});