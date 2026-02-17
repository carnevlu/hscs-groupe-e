# Groupe-E Energy for Home Assistant

This Home Assistant integration allows you to monitor your energy consumption from Groupe-E (Switzerland). It fetches data from the Groupe-E smart meter API and makes it available as energy sensors compatible with the Home Assistant Energy Dashboard.

## Features

- **Direct Login**: Secure login using your official Groupe-E email and password.
- **Energy Dashboard Ready**: Sensors are configured with `device_class: energy` and `state_class: total_increasing`.
- **Daily Sensor**: A new sensor that specifically shows today's consumption.
- **Configurable Polling**: Adjust how often data is fetched from the API (default: every 60 minutes).
- **Daily Consumption**: Automatically aggregates data into daily totals.

## Installation

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
3. Enter the following information:
   - **Username**: Your Groupe-E email.
   - **Password**: Your Groupe-E password.
   - **Premise ID**: Your location identifier (see below).
   - **Partner ID**: Your customer identifier (see below).

### How to find your Premise and Partner ID

To obtain your specific IDs, you need to inspect the network traffic on the official portal:

1. Log in to [my.groupe-e.ch](https://my.groupe-e.ch).
2. Go to the page where you can see your daily consumption graphs.
3. Press `F12` to open the **Developer Tools** and go to the **Network** tab.
4. Refresh the page or click on a different date to trigger a data reload.
5. In the "Filter" box, type `smartmeter-data`.
6. Click on the request and look at the **Payload** (or Request Body). You will see a JSON like this:
   ```json
   {
     "premise": "106180",
     "partner": "6050184",
     ...
   }
   ```
7. Use these values in the Home Assistant setup form.

## Security and Privacy

- **No Third-Party OAuth**: The integration communicates directly with Groupe-E's servers.
- **Storage**: Your credentials and IDs are stored securely in Home Assistant's internal configuration.
- **Logout/Login**: To update your password or IDs, you can either re-run the setup or delete and re-add the integration.

## Support

This is an unofficial integration. For issues related to the API or your Groupe-E account, please contact Groupe-E support. For issues with this integration, please open an issue on GitHub.
