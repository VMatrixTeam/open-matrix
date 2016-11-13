$( document ).ready(function() {
  $('#inputEmail').keyup(function() {
    var username_email = $('#inputEmail').val();
    load_avatar(username_email);
  });
  $('#sigin-button').click(function() {
    var username_email = $("#inputEmail").val();
    var password = $("#inputPassword").val();

    if(username_email == "" || password == "") {
      $("#text-danger").text('用户名和密码不能为空！');
      $("#login-info-modal").modal('show');
      return false;
    }

    $('#sigin-button').attr('disabled', 'disabled');

    $.post(
      '/login',
      {
        'username_email' : username_email,
        'password' : password
      },
      function(data) {
        if(!data.result) {
          $("#text-danger").text(data.msg);
          $("#login-info-modal").modal('show');
          $('#sigin-button').removeAttr('disabled');
        } else {
          window.location.href = '/question';
        }
      }
    )

    return false;
  });
});

function load_avatar(username_email) {
  $.get(
    '/login/search',
    {
      'username_email' : username_email
    },
    function(data) {
      if (data && data.result) {
        $("#profile-img").fadeOut(400, function() {
          $("#profile-img").attr('src', '/api/1.0/base/filesystem/avatar/' + data.data);
          $('#profile-img').fadeIn(400);
        });
      } else {
        if($("#profile-img").attr('src') != "static/images/guest.png") {
          $("#profile-img").fadeOut(400, function() {
            $("#profile-img").attr('src', 'static/images/guest.png');
            $('#profile-img').fadeIn(400);
          });
        }
      }
    }
  )
}
