// Initialize Telegram Web App
Telegram.WebApp.onEvent('DOMContentLoaded', function() {
    // Set the background color of the Mini App
    Telegram.WebApp.setBackgroundColor("#ffccff");

    // Set the header color
    Telegram.WebApp.setHeaderColor("#660066");

    // Configure the main button
    Telegram.WebApp.MainButton.setText("Let’s Groove!");
    Telegram.WebApp.MainButton.show();

    // Handle main button click
    Telegram.WebApp.MainButton.onClick(function() {
        let userInput = document.getElementById("userInput").value;
        if (userInput) {
            // Send data back to the bot
            Telegram.WebApp.sendData(JSON.stringify({ input: userInput }));
            logInfo("User input sent: " + userInput);
            updateEvent({ "user_input": userInput });
        } else {
            alert("Drop your details to join the rave!");
        }
    });

    // Set up event listeners for real-time theme changes
    Telegram.WebApp.onEvent('themeChanged', function() {
        document.body.style.backgroundColor = Telegram.WebApp.themeParams.bg_color;
        document.body.style.color = Telegram.WebApp.themeParams.text_color;
        logInfo("Theme changed: " + JSON.stringify(Telegram.WebApp.themeParams));
    });

    // Initialize the app interface
    initializeAppInterface();
});

function initializeAppInterface() {
    // Customize the UI based on theme parameters
    document.body.style.backgroundColor = Telegram.WebApp.themeParams.bg_color;
    document.body.style.color = Telegram.WebApp.themeParams.text_color;
    document.body.style.backgroundImage = "url('path/to/rave_background_image.jpg')"; // Add rave-themed background

    // Set the initial values and event listeners for UI elements
    document.getElementById("header").innerText = "Welcome to the UnderKrakow Rave!";
    document.getElementById("description").innerText = "Experience the ultimate rave under the scenic skies of Krakow. Please provide your details below.";

    // Additional UI setup if needed
}

// Handle data received from the bot
Telegram.WebApp.onEvent('receiveData', function(data) {
    let parsedData = JSON.parse(data);
    document.getElementById("response").innerText = parsedData.response;
    logInfo("Data received: " + data);
});

// Main Mini App setup
Telegram.WebApp.MainButton.setParams({
    text: "Launch UnderKrakow Mini App",
    color: "#660066",
    textColor: "#ffffff"
});

// Implement vertical swipes for navigation
Telegram.WebApp.enableVerticalSwipes();
logInfo("Vertical swipes enabled.");

// Customize section separator color
Telegram.WebApp.setThemeParams({
    section_separator_color: "#ff66cc"
});
logInfo("Section separator color set.");

// Enable biometric authentication (if supported)
if (Telegram.WebApp.BiometricManager) {
    Telegram.WebApp.BiometricManager.init().then(() => {
        logInfo("Biometric authentication initialized.");
    }).catch((error) => {
        logError("Biometric authentication initialization failed: " + error);
    });
}

// Setup the settings button
Telegram.WebApp.SettingsButton.show();
Telegram.WebApp.SettingsButton.onClick(function() {
    logInfo("Settings button clicked.");
});

// Utilize CloudStorage
Telegram.WebApp.CloudStorage.setItem("userPreferences", JSON.stringify({ theme: "dark" })).then(() => {
    logInfo("User preferences saved.");
}).catch((error) => {
    logError("Failed to save user preferences: " + error);
});

// Validate data
Telegram.WebApp.onEvent('initData', function(initData) {
    let dataCheckString = Telegram.WebApp.initDataUnsafe.data_check_string;
    let secretKey = 'your_bot_secret_key';
    let hash = Telegram.WebApp.initDataUnsafe.hash;

    if (validateData(dataCheckString, secretKey, hash)) {
        logInfo("Data validation successful.");
    } else {
        logError("Data validation failed.");
    }
});

function validateData(dataCheckString, secretKey, hash) {
    const crypto = require('crypto');
    const hmac = crypto.createHmac('sha256', secretKey);
    hmac.update(dataCheckString);
    const computedHash = hmac.digest('hex');
    return computedHash === hash;
}

// Function to update event data
async function updateEvent(data) {
    try {
        const response = await fetch('/update_event', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        if (result.status === "success") {
            logInfo("Event data updated successfully.");
        } else {
            logError("Failed to update event data: " + result.message);
        }
    } catch (error) {
        logError("Error updating event data: " + error);
    }
}

// Payment handling
function processPayment(amount, description, providerToken) {
    const paymentRequest = {
        provider_token: providerToken,
        start_parameter: 'pay',
        currency: 'USD',
        prices: [{ label: description, amount: amount }],
        payload: 'payment_payload'
    };

    Telegram.WebApp.openInvoice(paymentRequest);
    logInfo("Payment request initiated: " + JSON.stringify(paymentRequest));
}

// Handle payment response
Telegram.WebApp.onEvent('invoiceClosed', function(invoiceData) {
    if (invoiceData.status === 'paid') {
        showPaymentConfirmationScreen('Payment successful! Time to rave!');
        logInfo("Payment successful: " + JSON.stringify(invoiceData));
    } else {
        showPaymentConfirmationScreen('Payment failed or was cancelled.');
        logError("Payment failed or cancelled: " + JSON.stringify(invoiceData));
    }
});

function showPaymentConfirmationScreen(message) {
    document.getElementById("confirmationMessage").innerText = message;
    document.getElementById("paymentConfirmationScreen").style.display = "block";
}

// Payment options
document.getElementById("payWithApplePay").addEventListener("click", function() {
    processPayment(5000, 'Rave Ticket - Apple Pay', 'apple_pay_provider_token');
});

document.getElementById("payWithGooglePay").addEventListener("click", function() {
    processPayment(5000, 'Rave Ticket - Google Pay', 'google_pay_provider_token');
});

document.getElementById("payWithBitcoin").addEventListener("click", function() {
    processPayment(5000, 'Rave Ticket - Bitcoin', 'bitcoin_provider_token');
});

document.getElementById("payWithTether").addEventListener("click", function() {
    processPayment(5000, 'Rave Ticket - Tether', 'tether_provider_token');
});

function logInfo(message) {
    fetch('/log', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ level: 'info', message: message })
    });
}

function logError(message) {
    fetch('/log', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ level: 'error', message: message })
    });
}
