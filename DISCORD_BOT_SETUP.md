# Discord Bot Setup Guide

This guide provides step-by-step instructions on how to set up a Discord bot and obtain the necessary credentials (`guild_id` and `bot_token`) for your `config.json` file.

## Prerequisites

- A Discord account and a server where you have administrative privileges.
- Node.js installed on your local machine.

## Step 1: Create a Discord Bot Account

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click on the "New Application" button.
3. Name your application and click "Create".
4. Go to the "Bot" tab and click "Add Bot".
5. Under the "TOKEN" section, click "Copy" to save your bot's token. This is your `bot_token`.

## Step 2: Set Up Your Bot's Permissions

1. In the "Bot" tab, under "Privileged Gateway Intents", enable the intents your bot needs.
2. Go to the "OAuth2" tab.
3. Under "SCOPES", select "bot".
4. In the "BOT PERMISSIONS" section, check the permissions your bot requires.
5. Copy the generated URL and paste it into your web browser.
6. Select your server and click "Authorize" to add the bot to your server.

## Step 3: Obtain Your Server's Guild ID

1. Open Discord and go to your server.
2. Right-click the server name and click "Copy ID" to save your `guild_id`.
   - If you do not see the "Copy ID" option, enable "Developer Mode" in Discord's settings under "Appearance".

## Step 4: Update the Config File

1. Create or update your `config.json` file in your project directory with the `bot_token` and `guild_id`:

```json
{
  "guild_id": "YOUR_GUILD_ID",
  "bot_token": "YOUR_BOT_TOKEN",
  "hue_username": "", 
  "hue_access": ""
}
