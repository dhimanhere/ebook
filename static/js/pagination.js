var infinite = new Waypoint.Infinite({
  element: $('.infinite-container')[0],
  offset: 'bottom-in-view',
  onBeforePageLoad: function () {
    $('.loader-wrapper').show();
  },
  onAfterPageLoad: function () {
    $('.loader-wrapper').hide();
    $(".infinite-item").css("opacity","1");
  }
});