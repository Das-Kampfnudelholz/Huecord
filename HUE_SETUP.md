# Philips Hue Setup Guide

Welcome to the Philips Hue Setup Guide. This document will guide you through the process of setting up your Philips Hue environment for remote API access.

## Prerequisites

- Philips Hue Bridge connected to your network.
- Philips Hue lights set up and connected to the Hue Bridge.
- A device with internet access to sign up for a Philips Hue developer account.

## Step 1: Create a Philips Hue Developer Account

1. Go to the [Philips Hue Developer Portal](https://developers.meethue.com/).
2. Sign up for a new account or log in if you already have an account.

## Step 2: Find Your Hue Bridge IP Address

1. You can find the IP address of your Hue Bridge in your router's settings page under connected devices.
2. Alternatively, use a network scanning tool to find the Bridge on your local network.

## Step 3: Create a User on the Hue Bridge

1. Send a POST request to `http://{Bridge_IP_Address}/api` with the body `{"devicetype":"your_app_name#device_name"}`.
2. Press the link button on your Hue Bridge and then send the POST request within 30 seconds.
3. You'll receive a username in the response. Note this down as your `hue_username`.

## Step 4: Set Up Remote API Access

To control your Hue lights remotely, you'll need to use the remote API provided by Philips Hue.

1. Log in to your Philips Hue developer account and navigate to the Remote API section.
2. Register a new app to obtain your `Client ID` and `Client Secret`.
3. Set the Redirect URI to a URI where you can receive the authorization code, such as `http://localhost`.

### Authorizing Your Application

1. Construct the authorization URL with your `Client ID` and `Redirect URI`:
    https://api.meethue.com/oauth2/auth?clientid=<YOUR_CLIENT_ID>&appid=<YOUR_APP_ID>&state=<YOUR_STATE>&response_type=code
2. Visit the authorization URL in a web browser, log in with your Philips Hue account, and grant permission.
3. You'll be redirected to your `Redirect URI` with an authorization `code` in the URL parameters.

### Obtaining the Access Token

1. Use an HTTP client like Insomnia or Postman to send a POST request to exchange the authorization code for an access token:

2. You will receive an `access_token` in the response.

## Step 5: Update the Config File

1. Open the `Config.json` file in your project directory.
2. Fill in the `hue_username` and `hue_access` (the `access_token` you received) fields with your credentials.

## Step 6: Test Your Setup

1. Use an HTTP client to send a test request to your Hue Bridge or the remote API endpoint.
2. Verify that you can control your lights using the API.

Congratulations! You've set up your Philips Hue environment for local and remote access.

Please ensure that you replace placeholder text like <YOUR_CLIENT_ID>, <YOUR_APP_ID>, <YOUR_STATE>, <AUTHORIZATION_CODE>, and <YOUR_CLIENT_SECRET> with the actual values you receive during the setup process.