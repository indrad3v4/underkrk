## README.md for UnderKrakowRave

# UnderKrakowRave

Welcome to the UnderKrakowRave project! This repository contains the code for a comprehensive Telegram Mini App and bot designed to provide an engaging and seamless experience for rave enthusiasts in Krakow. This project utilizes Flask for the web application and Python-Telegram-Bot for the bot functionality.

## Project Structure

Here's an overview of the project's directory structure:

- **rave_bot/**
  - **app/**
    - `__init__.py`
    - `config.py`
    - `models.py`
    - `controllers.py`
    - `views.py`
    - `utils.py`
    - **templates/**
      - `index.html`
      - `styles.css`
      - `main.js`
    - **static/**
      - **js/**
        - `telegram-web-app.js`
  - **bot/**
    - `__init__.py`
    - `handlers.py`
    - `main.py`
    - `messages.py`
    - `ai_responses.py`
    - `payments.py`
  - **data/**
    - `events.json`
    - `participants.json`
    - `donations.json`
    - `soundsystem.json`
  - **logs/**
    - `bot.log`
    - `error.log`
  - **tests/**
    - `test_models.py`
    - `test_controllers.py`
    - `test_views.py`
    - `test_bot.py`
    - `test_payments.py`
  - `.env`
  - `requirements.txt`
  - `README.md`
  - `run.py`

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**
- **Pip**

### Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/underkrakow-rave-bot.git
    cd underkrakow-rave-bot
    ```

2. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

3. **Set up environment variables:**

    Create a `.env` file in the root directory and add the following variables:

    ```sh
    YOUR_BOT_TOKEN='your-telegram-bot-token'
    OPENAI_API_KEY='your-openai-api-key'
    ```

### **Running the Application:**

    To start the bot and web app:

```sh
python run.py
```
    

    
This will start the Flask web application and the Telegram bot concurrently.


## Contributing

We welcome contributions!

## License

This project is licensed under the **MIT License**. 

**Under Krakow Rave Bot** is here to enhance your rave experience with real-time updates, interactive features, and more. Stay tuned and enjoy the rave!

### Want experience? Open [webapp](t.me/UnderKrakowBot).
