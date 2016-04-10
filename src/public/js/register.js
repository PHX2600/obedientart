$(document).ready(function() {

  $("#registerbutton").click(function(event){

    event.preventDefault();
    var pwd1 = $("#register_password1").val();
    var pwd2 = $("#register_password2").val();

    if(pwd1 != pwd2)
    {
      $("#failedregister_message").hide();
      $("#failedregister_message").hide();
      $("#failedregister_message_2").show(500);
      return;
    }

    jQuery.post({
      url: "/register",
      data: $("#registerform").serialize(),
      statusCode: {
        200: function() {
          window.location.replace("/login");
        },
        403: function() {
          $("#failedregister_message").hide();
          $("#failedregister_message_2").hide();
          $("#failedregister_message").show(500);
        }
      }
    });
  });

});
