$(document).ready(function() {

  $("#loginbutton").click(function(event){

    event.preventDefault();

    jQuery.post({
      url: "/login",
      data: $("#loginform").serialize(),
      statusCode: {
        200: function() {
          window.location.replace("/");
        },
        403: function() {
          $("#failedlogin_message").hide();
          $("#failedlogin_message").show(500);
        }
      }
    });
  });

});
