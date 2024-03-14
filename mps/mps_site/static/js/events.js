  // Fetch JSON data from the file
  fetch('event-data.json')
      .then(response => response.json())
      .then(data => {
          // Display data on the website
          document.getElementById('event_1_name').textContent = data.event_1_name;
          document.getElementById('event_1_image').src = data.event_1_image;
          document.getElementById('event_1_start').textContent = data.event_1_start;
          document.getElementById('event_1_end').textContent = data.event_1_end;
          document.getElementById('event_1_description').textContent = data.event_1_description;
          document.getElementById('event_1_location').textContent = data.event_1_location;

          document.getElementById('event_2_name').textContent = data.event_2_name;
          document.getElementById('event_2_image').src = data.event_2_image;
          document.getElementById('event_2_start').textContent = data.event_2_start;
          document.getElementById('event_2_end').textContent = data.event_2_end;
          document.getElementById('event_2_description').textContent = data.event_2_description;
          document.getElementById('event_2_location').textContent = data.event_2_location;
          
      })
      .catch(error => console.error('Error fetching data:', error));