let clickCount = 0;

  function checkClicks() {
    clickCount++;

    // Change the threshold (5) to any number of clicks you desire
    if (clickCount === 5) {
      // Play the sound
      
      setTimeout(function(){
        document.getElementById('clickSound2').play();
         }, 2000);
          document.getElementById('clickSound').play();
      
    }

    // Stop the music and reset the click count on the 6th click
    if (clickCount === 6) {
      document.getElementById('clickSound2').pause();
      document.getElementById('clickSound2').currentTime = 0;
      clickCount = 0;
    }
  }