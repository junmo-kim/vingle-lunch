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

  function upcomming_friday() {
    var date = new Date()
    var dayDiff = ((5 - date.getDay()) + 7) % 7
    date.setDate(date.getDate() + dayDiff)
    date.setHours(11, 05, 0, 0)
    return date
  }
  $('#count_down').countdown(upcomming_friday(), function(event) {
    var totalHours = event.offset.totalDays * 24 + event.offset.hours;
    $(this).html(event.strftime(totalHours + ' hr %M min %S sec'));
  });

  $(".button-collapse").sideNav();
  $('.dropdown-button').dropdown();
  $('select').not('.disabled').material_select();
})
