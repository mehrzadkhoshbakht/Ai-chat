# Generating API Keys

This guide explains how to generate the necessary API keys for the AI-chat application.

## OpenAI API

1.  **Create an account:** Go to [https://platform.openai.com](https://platform.openai.com) and create an account.
2.  **Generate an API key:** Navigate to the [API keys](https://platform.openai.com/account/api-keys) page and click on "Create new secret key".
3.  **Copy the key:** Copy the generated key and store it in a safe place. You will need it later.
4.  **Usage limits:** OpenAI has usage limits based on your subscription plan. You can monitor your usage and billing information in the [Usage](https://platform.openai.com/account/usage) page.

## YouTube Data API

1.  **Create a project:** Go to the [Google Cloud Console](https://console.cloud.google.com) and create a new project.
2.  **Enable the API:** In the project dashboard, go to "APIs & Services" > "Library" and search for "YouTube Data API v3". Enable the API for your project.
3.  **Create credentials:** Go to "APIs & Services" > "Credentials" and click on "Create credentials" > "OAuth client ID".
4.  **Configure the consent screen:** Before creating the client ID, you need to configure the OAuth consent screen. Select "External" and fill in the required information.
5.  **Create the client ID:** Choose "Desktop app" as the application type and give it a name.
6.  **Download the client secrets:** After creating the client ID, click on the download button to get the `client_secrets.json` file. You will need this file later.
7.  **Quota limits:** The YouTube Data API has a daily quota limit. You can monitor and request an increase in the "Quotas" tab of the API dashboard.

## Telegram Bot API

1.  **Talk to BotFather:** Open Telegram and search for the "BotFather" bot.
2.  **Create a new bot:** Send the `/newbot` command to BotFather and follow the instructions.
3.  **Get the bot token:** After creating the bot, BotFather will give you a bot token. Copy it and store it in a safe place.
4.  **API limits:** The Telegram Bot API has limits on the number of messages you can send per second. You can find more information in the [Telegram Bot API documentation](https://core.telegram.org/bots/api#rate-limits).

## Updating and Rotating API Keys

To update or rotate an API key, follow these steps:

1.  **Generate a new key:** Follow the instructions above to generate a new API key for the desired service.
2.  **Update the `.env` file:** Open the `.env` file in the root of the project and replace the old API key with the new one.
3.  **Restart the application:** Restart the application for the changes to take effect.
4.  **Revoke the old key:** Once you have confirmed that the new key is working correctly, you should revoke the old key from the service provider's dashboard. This will prevent the old key from being used maliciously.
