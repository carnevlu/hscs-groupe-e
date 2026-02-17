# Groupe-E Energy for Home Assistant

This Home Assistant integration allows you to monitor your energy consumption from Groupe-E (Switzerland). It fetches data from the Groupe-E smart meter API and makes it available as energy sensors compatible with the Home Assistant Energy Dashboard.

## Features

- **OAuth2 Authentication**: Secure login using your official Groupe-E credentials via OpenID Connect.
- **Energy Dashboard Ready**: Sensors are configured with `device_class: energy` and `state_class: total_increasing`.
- **Configurable Polling**: Adjust how often data is fetched from the API (default: every 60 minutes).
- **Daily Consumption**: Automatically aggregates quarter-hourly data into daily totals.

## Installation

### Manual Installation

1. Download the `groupe_e` folder from this repository.
2. Copy it into your Home Assistant `custom_components` directory.
3. Restart Home Assistant.

### HACS (Recommended)

1. Open HACS in Home Assistant.
2. Click on **Integrations**.
3. Click the three dots in the top right corner and select **Custom repositories**.
4. Paste the URL of this repository: `https://github.com/carnevlu/hscs-groupe-e`
5. Select **Integration** as the category.
6. Click **Add** and then install the **Groupe-E Energy** integration.
7. Restart Home Assistant.

## Configuration

1. In Home Assistant, go to **Settings** > **Devices & Services**.
2. Click **Add Integration** and search for **Groupe-E Energy**.
3. A login window will appear. Sign in with your Groupe-E credentials.
4. Once authenticated, the integration will automatically detect your energy data.

### Settings & Options

You can change the update frequency at any time:
1. Go to **Settings** > **Devices & Services**.
2. Find the **Groupe-E Energy** card.
3. Click **Configure** to change the polling interval (in minutes).

## Security and Privacy

- **No Hardcoded Tokens**: This module uses official OAuth2 flows. Your session tokens are managed securely by Home Assistant's `config_entry_oauth2_flow`.
- **Storage**: Credentials (refresh tokens) are stored encrypted by Home Assistant in its internal configuration files (`.storage/core.config_entries`).
- **Logout/Login**: To log out, simply delete the integration entry. To log in again, re-add the integration.

## Support

This is an unofficial integration. For issues related to the API or your Groupe-E account, please contact Groupe-E support. For issues with this integration, please open an issue on GitHub.
