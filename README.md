# Cesal Scraper

This project automates the process of checking room availabilities on the Cesal website.

## Setup

1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Ensure you have ChromeDriver installed in the same directory as this project or in your PATH. Ensure that ChromeDriver match the version of your Google Chrome browser. Go this website to download the right version for your [Google Chrome version](https://chromedriver.chromium.org/downloads).

## Usage

Run the script with the following command, replacing the placeholders with your actual information:

```bash
python3 scraper.py --email YOUR_EMAIL --password YOUR_PASSWORD --sender_email YOUR_SENDER_EMAIL --sender_password YOUR_SENDER_PASSWORD --recipient_email YOUR_RECIPIENT_EMAIL --time_frequency 'daily'
```