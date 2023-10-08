# Currency Rate Exchange Alert Agent

**Techfest IIT Bombay[HackAI](https://techfest.org/competitions/hack-aI) Competition.**

## Project Details

# Currency Exchange Rate Alert Agent

This Currency Exchange Rate Alert Agent is a tool that allows users to monitor and receive alerts when there is a change in currency exchange rates for specified currency pairs. It connects to a free currency exchange rate API to fetch real-time exchange rate data and sends notifications to users when the exchange rate for their chosen currency pair crosses predefined thresholds.

## Features

- Connects to a free currency exchange rate API to fetch real-time exchange rate data.
- Allows users to set their preferred currency pair (e.g., USD/EUR, GBP/JPY) and exchange rate thresholds.
- Sends alerts/notifications to the user when the current exchange rate for their chosen currency pair crosses the minimum or maximum threshold they've set.

## Set up the Project

### Install the poetry library

- Make sure you have python installed in your system and the version of the python should be between 3.11 and 3.12. 3.12 also doesn't support the project.

- Install poetry on your system by running
  ```
  pip install poetry
  ```
-Poetry works best with Ubuntu system. If you are Windows user than try WSL.

### Clone the Project

- Run the command on your terminal `git clone <repository_url>`

- Replace `<repository_url>` with the actual URL of the project's Git repository.

- Now navigate to the Project Directory by running `cd project_directory`

### Creating a Virtual environment

- Inside the project directory, your should create a virtual environment using Poetry:

  ```
  poetry install
  ```

  This command reads the project's pyproject.toml file and sets up a virtual environment with the required dependencies.

- Now activate the poetry shell using the following command.

  ```
  poetry shell
  ```

### Generating a MongoDb connection String to use in the .env file (Mentioned in the next point)

- Go to [MongoDb](https://www.mongodb.com/) and create a new account. Answer the basic questions and click on finish

- Choose M0 databse configuration.

- Make a username and password and click on create user

- Add a new IP Address `0.0.0.0/0` and click on create entry

- Click on create and close go the Overview.

- You will be taken to a overview page.

- Now click on Connect and click on drivers and select the driver "Python" and Version as "3.11 or later".

- Copy your connection string and Replace `<password>` with the password for the your account made in one of the above steps.

### Setting up the .env file

- Create an account on [FreeCurrencyAPI](https://app.freecurrencyapi.com/) and get an Api Key.

  - Visit [FreeCurrencyAPI](https://app.freecurrencyapi.com/) and create a new account or Sign-in to your account.

  - Now copy the Default API Key provided.
  
  - This API is only able to consider USD as base currency. Be sure to set base currency as USD while editing the client.py file.

- Create a file in the project directory named `.env` and paste the following code in it.

  ```
  ACCESS_KEY="<your_api_key_here>"

  EMAIL_SENDER = "<email_of_sendor>"
  EMAIL_PASSWORD = "<sender_app_email_password>"

  MONGODB_URL="<your_connection_string>"
  ```

- Replace `<your_api_key_here>` with your your api key

- Replace `<email_sendor>` with the email you want to send the alert from

- Replace `<sendor_email_password>` with app password generated for your google account. Don't write your google account password, it will not work if you enter gmail password.

  If you don't know how to generate app passwords for your google account refer to this [link](https://support.google.com/accounts/answer/185833?hl=en#zippy=)

- Replace the `<your_connection_string>` with your mongodb connection string you generated in the last point

### Run the main script

```
python3 src/main.py
```

Copy the Currency agent address printed in the console.We are going to need it.

### Editing the client script

Now that we have set up the integrations, we need to set up the client script to communicate with our currency agent. 

This script is the client side script to define the minimum and maximum values of the foreign currencies with respect to the base currency. There are many changes you need to make to client_template.py file.

- Change the <your_currency_agent_address> to the address you copied in above step.

- Change the `receiveraddress@gmail.com` to your email address.

- Mention the foreign currency, min and max value of the currency according to your choice.

- The base currency needs to remain fix for this api.

### Run the client script

Open a new terminal.

```sh
python3 client.py
```
