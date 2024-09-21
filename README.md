# Job Application Automation Script

This script automates the process of searching and applying for jobs on a website using Selenium WebDriver. It uses environment variables to configure search parameters and personal information required for job applications.

## Prerequisites
- Python 3.x
- Google Chrome
- ChromeDriver
- pip package manager

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/bi-kash/jobvite_robot
   cd jobvite_robot
   ```

2. Install required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Replace filters in a `.env` file in the root directory according to your need

4. Add proxy addresses, one per line, if you want to use proxies. This assumes proxy does not require credentials for given IP

## Usage

Run the script:

```bash
python apply.py
```


## Features
- **Custom User-Agent**: Sets a custom user-agent string to mimic a real browser.
- **Random Sleep**: Introduces random sleep times between actions to mimic human behavior.
- **Proxy Usage**: Optionally uses proxy servers to distribute requests and avoid IP-based detection.
- **Session Management**: Uses `user-data-dir` to maintain session data across multiple interactions.

## Preventing Bot Detection
The script includes several measures to prevent bot detection:
- Custom user-agent string.
- Random sleep times between actions.
- Optional proxy usage.
- Session management using `user-data-dir`.

### Additional Measures
To further enhance bot detection prevention, consider:
- Simulating realistic mouse movements and keyboard inputs.
- Randomizing browser fingerprinting attributes.
- Adding more human-like interactions such as scrolling and hovering.
- Implementing CAPTCHA solving techniques if necessary.