# Amul Stock Notifier Bot

This project monitors the [Amul Protein](https://shop.amul.com/en/browse/protein) page and sends you an email notification when selected whey protein products are back in stock for your delivery pincode.

## Features
- Monitors multiple products by name
- Supports pincode-based stock checking (enters pincode in popup)
- Sends email notifications when products are in stock
- Can be run locally or automated with GitHub Actions

---

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/amul-stock-bot.git
cd amul-stock-bot
```

### 2. Install Requirements
```bash
pip install -r requirements.txt
pip install python-dotenv
```

### 3. Create a `.env` File
Create a `.env` file in the project root with the following content:
```env
EMAIL=your_email@gmail.com
PASSWORD=your_email_app_password
TO_EMAIL=recipient_email@gmail.com
PINCODE=400060
```
- Use a Gmail **App Password** (not your regular password) for `PASSWORD`.
- Set `TO_EMAIL` to your recipient address (can be the same as `EMAIL`).
- Set `PINCODE` to your delivery area.

### 4. Install ChromeDriver
- Download [ChromeDriver](https://sites.google.com/chromium.org/driver/) matching your Chrome version.
- Add it to your system PATH or specify its path in the script if needed.

---

## Usage

To run the script locally:
```bash
python main.py
```
- The script will enter your pincode, check stock, and send an email if any products are in stock.

---

## Automate with GitHub Actions

1. **Push your code to GitHub.**
2. **Add your secrets** (`EMAIL`, `PASSWORD`, `TO_EMAIL`, `PINCODE`) in your repo's Settings → Secrets and variables → Actions.
3. **Add the provided workflow file** in `.github/workflows/stock-check.yml` to run the script every 10 minutes.

---

## Security
- **Never commit your real `.env` file or app passwords.**
- Use GitHub Secrets for sensitive data in CI/CD.

---

## Troubleshooting
- If you get authentication errors, make sure you are using an App Password and have enabled 2FA on your Gmail account.
- If Selenium cannot find ChromeDriver, ensure it is installed and in your PATH.
- For merge or push errors, see the GitHub/Git troubleshooting section above.

---

## License
MIT