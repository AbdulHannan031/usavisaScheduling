
# USA Visa Scheduling Auto-Booking

This repository contains a Selenium-based automation script for scheduling USA visa appointments. The script automates the process of booking appointments through the official U.S. visa scheduling website.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Overview

The aim of this project is to simplify the visa appointment booking process by automating it using Selenium WebDriver. This script can be particularly useful for users who need to book appointments quickly and efficiently.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.6 or higher
- [Selenium](https://www.selenium.dev/)
- [ChromeDriver](https://sites.google.com/chromium.org/driver/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Requests](https://requests.readthedocs.io/en/master/)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/usavisaScheduling.git
   ```

2. Navigate to the project directory:

   ```bash
   cd visa-scheduling-auto-booking
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Download ChromeDriver and place it in a directory included in your system’s `PATH`. You can download it [here](https://sites.google.com/chromium.org/driver/).

## Usage

1. Open `config.py` and update the following settings with your credentials and desired appointment details:

   ```python
   USERNAME = 'your-username'
   PASSWORD = 'your-password'
   APPOINTMENT_DATE = 'desired-date'
   ```

2. Run the script:

   ```bash
   python auto_booking.py
   ```

   The script will automatically open a browser window, navigate to the visa scheduling website, log in, and attempt to book an appointment based on the specified date.

## Configuration
-**2CaptchaAPI**:Your 2captcha api
- **USERNAME**: Your username for the visa scheduling portal.
- **PASSWORD**: Your password for the visa scheduling portal.
- **APPOINTMENT_DATE**: The date you wish to book for your visa appointment.


