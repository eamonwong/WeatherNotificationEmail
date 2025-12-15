# WeatherNotificationEmail 
This automated weather service is designed to streamline my morning routine. While checking weather apps has become second nature, I wanted to eliminate that extra step by integrating forecasts directly into my existing email habit. Now, instead of manually searching for weather updates, I receive a comprehensive daily forecast delivered automatically to my inbox each morning.

# Features ✨
## 🌤️ Comprehensive Daily Forecast
- Current temperature and "feels like" temperature
- Today's high and low temperature range
- Detailed weather conditions (e.g., "Overcast Clouds")
- Humidity percentage and wind speed

## 📧 Professional Email Format
Receive beautifully formatted emails like this:
```text
🌤️ Your Daily Weather Forecast for London
📅 Thursday, November 06 2025

RIGHT NOW:
• Temperature: 15.4°C
• Feels like: 15.2°C
• Conditions: Overcast Clouds
• Humidity: 86%
• Wind: 1.54 m/s

TODAY'S FORECAST:
• High: 16.4°C
• Low: 13.1°C  
• Overall: Overcast Clouds

Have a wonderful day! ☀️
```
## ⚡ Reliable 24/7 Automation
- Scheduled delivery: Daily at 9:30 AM (configurable to any time)
- macOS background service: Runs continuously, survives reboots and terminal closures
- Sleep-proof scheduling: Catches up if computer was asleep at scheduled time
- Automatic error recovery: Retry logic for failed API calls or email sends
- Detailed logging: Comprehensive logs for monitoring and debugging

# Technologies Used 🛠️
| Component	| Description |
| ---- | ---- |
| Python | Core automation and data processing |
| OpenWeatherMap API | Real-time weather data and 5-day forecasts |
| SMTP | Secure email delivery via Gmail |
| APScheduler | Reliable task scheduling |
| Requests | HTTP API calls to weather service |
| macOS launchd | Background service management on macOS |
| Pytz | Timezone handling for accurate scheduling |

# Architecture Overview 🔄

<img width="1660" height="2904" alt="WeatherEmail" src="https://github.com/user-attachments/assets/2ada1987-17a2-4b33-af0e-5bbfddbc2bb7" />

# Quick Setup 🔧
## 1. Get Your API Keys
### OpenWeatherMap API
- Free account at OpenWeatherMap
- Copy your API key

### Gmail Setup
- Enable 2-factor authentication
- Generate an App Password for Python scripts

## 2. Configure the Script
Edit weatherEmail.py:

```python
OPENWEATHER_API_KEY = "your_actual_api_key_here"
CITY = "your_location" 
EMAIL_USER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_gmail_app_password"
TO_EMAIL = "recipient@email.com"
```

### 3. Install & Run

```bash
# Clone or create project directory
cd /path/to/your/project

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install apscheduler pytz requests

# Test the script
python weatherEmail.py
```

# Deployment as macOS Service 🚀
## Automated Setup (One Command)

```bash
# Run setup script (creates everything automatically)
chmod +x setup_macos_service.sh
./setup_macos_service.sh
```
## Manual macOS Service Setup
### 1. Create the launchd service file:

```bash
cat > ~/Library/LaunchAgents/com.user.weatherdaemon.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.weatherdaemon</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/your/venv/bin/python</string>
        <string>/path/to/your/project/weather_daemon.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/weatherdaemon.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/weatherdaemon.err</string>
    <key>WorkingDirectory</key>
    <string>/path/to/your/project</string>
</dict>
</plist>
EOF
```
### 2. Load and start the service:

```bash
launchctl load ~/Library/LaunchAgents/com.user.weatherdaemon.plist
launchctl start com.user.weatherdaemon
```

### 3. Verify it's running:

```bash
launchctl list | grep weather
# Should show: [PID] 0 com.user.weatherdaemon
```

# Example Output 📨
The system delivers clean, professional emails with:
- Current Conditions: Real-time temperature, humidity, and wind
- Today's Outlook: High/low temperatures and overall weather pattern
- Easy Scanning: Bullet-point format for quick reading
- Friendly Tone: Positive closing message to start your day right

# Why Choose This System? 🎯
## Stop Manual Checking
- No more opening multiple weather apps
- Information arrives exactly when you need it
- Consistent format makes scanning effortless

## Stay Prepared
- Know exactly what to wear based on temperatures
- Plan your day around weather conditions
- Never be surprised by rain or temperature drops

## Perfect Integration
- Works with your existing email habit
- Minimal setup required
- Runs reliably in the background

# Security 🔐
- Uses Gmail App Passwords (more secure)
- No sensitive data stored locally
- API keys kept in configuration only
- All communications over HTTPS

# Troubleshooting
Common Solutions:
- "SMTP Error" → Check Gmail App Password
- "City not found" → Verify city format: "City,CountryCode"
- "API Error" → Confirm OpenWeatherMap API key is active

Logs Show:
- ✅ Successful sends with timestamps
- ❌ Failed attempts with error details
- 🔄 Automatic retry status

---
![WeatherNotificationEmail ](https://github.com/user-attachments/assets/6ef0a5fe-d2e1-41e0-85d1-82f0782db2fb)  

![WeatherNotificationEmail(2)](https://github.com/user-attachments/assets/0d763a85-d8f2-4e25-9f7b-8f4ef26a1914)  


Start your day informed, without lifting a finger. ☕🌤️  
Sips tea ☺️ 




