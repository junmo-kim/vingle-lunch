$( document ).ready(function(){
  $(".user_eat_box").change(function() {
    var user_id = this.id.split("user_eat_")[1];
    var text;
    if ($(this).is(":checked")) {
      text = "Yes!";
      $.ajax("/users/" + user_id + "/eat/yes");
    } else {
      text = "Next...";
      $.ajax("/users/" + user_id + "/eat/next");
    }
    $("#user_eat_label_" + user_id).html(text);
  });

  $(".button-collapse").sideNav();
  $('.dropdown-button').dropdown();
  $('select').not('.disabled').material_select();
})