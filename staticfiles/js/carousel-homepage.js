document.addEventListener("DOMContentLoaded", function () {
  // Set the hour range for carousel change
  var startHour = 16; // 4 PM
  var endHour = 17;   // 5 PM

  function checkTime() {
      var today = new Date();
      var currentHour = today.getHours();

      if (currentHour >= startHour && currentHour < endHour) {
          // Change the carousel item every 5 seconds (5000 milliseconds)
          setInterval(function () {
              $('#myCarousel').carousel('next');
          }, 5000);
      } else {
          // If the current time is outside the specified range, check again every minute
          setTimeout(checkTime, 60000);
      }
  }

  checkTime();
});