# Cesal Room Availability Checker

This Python script automates the process of checking room availability at Cesal Residential by scraping the Cesal website. It notifies the user via email if a room is available for a specified end date.

## Getting Started

### Prerequisites

- Python 3.x
- Google Chrome Browser
- ChromeDriver
- A Gmail address is required to receive automatic alerts

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/LaFerraille/Cesal_scraper.git
   cd project
   ```
2. **Install dependencies:**

   `pip install -r requirements.txt`

3. **Chromedriver:**
Ensure you have ChromeDriver installed in the same directory as this project or in your PATH. Ensure that ChromeDriver match the version of your Google Chrome browser. Go this website to download the right version for your [Google Chrome version](https://chromedriver.chromium.org/downloads).

4. **Environment Variables:**
Create a `.env` file in the root directory and populate it with the necessary credentials. You will need two personal email addresses: sender_email (which must be a Gmail address) and recipient_email.

```bash
CESAL_ID=your_cesal_id
CESAL_PASSWORD=your_cesal_password
SENDER_EMAIL=your_gmail_address
SENDER_PASSWORD=your_gmail_password
RECIPIENT_EMAIL=another_email_address
```

5. **App Password:**
You need to configure your own "App Password" for you to send email automatically with the smtplib package. See [App Password tutorial](https://support.google.com/accounts/answer/185833?hl=fr)

## Usage

Execute the script using the following command, replacing 'end_date' with your preferred departure time. Please ensure it is in the DD/MM/YYYY format and set to a date at least 80 days from the current datetime:

```bash
python3 cesal.py --end_date "DD/MM/YYYY"
```
Optional: Use `--headless False` to run Chrome in visible mode.

## Scheduling with Cron Jobs

1. Open terminal and type `crontab -e` to edit your cron jobs.
2. Press `Esc` then `i` to insert a new job.
3. Define the frequency and command format:

```bash
{frequency} {path_to_python3} {path_to_cesal.py} --end_date "DD/MM/YYYY" >> {path_to_cron.log} 2>&1
```
Use [crontab.guru](https://crontab.guru) for help with cron syntax.

4. To save and exit, press `Esc` followed by `:wq`.
5. To delete your cron jobs, use the command `crontab -r`.
