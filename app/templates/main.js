document.addEventListener('DOMContentLoaded', function() {
  const submitButton = document.getElementById('submitButton');
  const userInput = document.getElementById('userInput');
  const responseDiv = document.getElementById('response');

  // Configure the main button
  Telegram.WebApp.MainButton.setText("Submit");
  Telegram.WebApp.MainButton.show();

  // Handle main button click
  Telegram.WebApp.MainButton.onClick(function() {
      let inputText = userInput.value.trim();
      if (inputText) {
          // Send data back to the bot
          Telegram.WebApp.sendData(JSON.stringify({ input: inputText }));
      } else {
          alert("Please enter some input.");
      }
  });

  // Handle form submit button click
  submitButton.addEventListener('click', function() {
      let inputText = userInput.value.trim();
      if (inputText) {
          // Send data back to the bot
          Telegram.WebApp.sendData(JSON.stringify({ input: inputText }));
      } else {
          alert("Please enter some input.");
      }
  });

  // Initialize the app interface
  initializeAppInterface();

  // Handle data received from the bot
  Telegram.WebApp.onEvent('receiveData', function(data) {
      let parsedData = JSON.parse(data);
      responseDiv.innerText = parsedData.response;
  });
});

function initializeAppInterface() {
  // Customize the UI based on theme parameters
  document.body.style.backgroundColor = Telegram.WebApp.themeParams.bg_color;
  document.body.style.color = Telegram.WebApp.themeParams.text_color;

  // Set the initial values and event listeners for UI elements
  document.getElementById("header").innerText = "Welcome to the UnderKrakow Rave!";
  document.getElementById("description").innerText = "Experience the ultimate rave under the scenic skies of Krakow. Please provide your details below.";

  // Additional UI setup if needed
}
