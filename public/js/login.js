$(document).ready(function() {

  $("#loginbutton").click(function(event){

    //event.preventDefault();

    jQuery.post({
      url: "/login",
      data: $("#loginform").serialize(),
      statusCode: {
        403: function() {
          $("#failedlogin_message").hide();
          $("#failedlogin_message").show(500);
        }
      }
    });
  });

});
