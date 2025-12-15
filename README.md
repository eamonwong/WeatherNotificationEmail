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

# Service Management 🔧
## Monitoring Commands

```bash
# Check service status
launchctl list | grep weather

# View real-time logs
tail -f /tmp/weatherdaemon.err

# Check recent email sends
grep -i "sending weather email\|sent successfully" /tmp/weatherdaemon.err

# View heartbeat (runs every 30 minutes)
grep "Daemon alive" /tmp/weatherdaemon.err | tail -1
```

## Control Commands

```bash
# Stop the service
launchctl stop com.user.weatherdaemon

# Start the service
launchctl start com.user.weatherdaemon

# Restart (full reload)
launchctl unload ~/Library/LaunchAgents/com.user.weatherdaemon.plist
launchctl load ~/Library/LaunchAgents/com.user.weatherdaemon.plist
launchctl start com.user.weatherdaemon

# Remove service completely
launchctl unload ~/Library/LaunchAgents/com.user.weatherdaemon.plist
rm ~/Library/LaunchAgents/com.user.weatherdaemon.plist
```
## Quick Status Check

```bash
echo "Service PID: $(ps aux | grep weather_daemon | grep -v grep | awk '{print $2}')"
echo "Next email: $(grep 'next run at' /tmp/weatherdaemon.err 2>/dev/null | tail -1 | cut -d' ' -f6- || echo 'Not scheduled')"
echo "Last heartbeat: $(grep 'Daemon alive' /tmp/weatherdaemon.err 2>/dev/null | tail -1 | cut -d' ' -f1-3 || echo 'No heartbeat')"
```

# Customisation ⚙️
## Change Schedule Time
Edit weather_daemon.py:

```python
#  For 8:00 AM instead of 9:30 AM
minute = 0  # Change from 30 to 0
CronTrigger(hour=8, minute=minute, timezone='Europe/London')
```

## Different Timezone
```python
# Available timezones:
CronTrigger(hour=9, minute=30, timezone='Europe/London')      # London, UK
CronTrigger(hour=9, minute=30, timezone='US/Eastern')         # New York, USA
CronTrigger(hour=9, minute=30, timezone='Asia/Kuala_Lumpur')  # Kuala Lumpur, Malaysia
CronTrigger(hour=9, minute=30, timezone='Asia/Shanghai')      # Shanghai, China
CronTrigger(hour=9, minute=30, timezone='Australia/Sydney')   # Sydney, Australia
CronTrigger(hour=9, minute=30, timezone='UTC')                # Coordinated Universal Time
```

# Example Output 📨
The system delivers clean, professional emails with:
- Current Conditions: Real-time temperature, humidity, and wind
- Today's Outlook: High/low temperatures and overall weather pattern
- Easy Scanning: Bullet-point format for quick reading
- Friendly Tone: Positive closing message to start your day right

# Security Considerations 🔐
## Best Practices Implemented
- ✅ Gmail App Passwords: More secure than regular passwords
- ✅ API Key Isolation: Keys stored in configuration only
- ✅ HTTPS Only: All API calls use encrypted connections
- ✅ No Data Storage: No personal data stored locally
- ✅ Virtual Environment: Isolated Python dependencies

## Security Recommendations
- Regularly rotate your Gmail app password
- Monitor OpenWeatherMap API usage
- Keep your API keys confidential
- Use different email for sending/receiving if concerned about privacy
- Review logs periodically for unusual activity

# Performance & Reliability 📊
## System Requirements
- Minimal Resources: Uses < 50MB RAM, < 1% CPU when idle
- Network: Requires internet connection for API calls
- Storage: Logs use < 10MB per month

## Uptime Features
- Auto-restart: macOS launchd keeps service running
- Sleep recovery: Catches up missed jobs after wakeup
- Error resilience: Retries failed API calls (3 attempts)
- Connection timeout: Prevents hanging on network issues

## Monitoring
- Heartbeat: Logs every 30 minutes confirming service alive
- Email confirmation: Logs each successful send
- Error tracking: Detailed error messages with timestamps
- Scheduler status: Logs next scheduled run time

# Why Choose This System? 🎯
## Stop Manual Checking
- No more opening multiple weather apps
- Information arrives exactly when you need it (9:30 AM daily)
- Consistent format makes scanning effortless
- Eliminates the morning weather-checking ritual

## Stay Prepared & Informed
- Know exactly what to wear based on temperatures
- Plan your day around weather conditions
- Never be surprised by rain or temperature drops
- Comprehensive data with current conditions + daily forecast

## Perfect Integration
- Works with your existing email habit
- Minimal setup required (once and done)
- Runs reliably in the background 24/7
- Survives terminal closure and system reboots

## Privacy & Control (important to me 🙈)
- Your data stays with you, no third-party analytics
- Full control over information displayed
- Customisable to your preferences
- No tracking of your weather queries

## Technical Advantages
- True automation - no manual intervention needed
- Sleep-proof - catches up if computer was asleep
- Professional quality - clean, formatted emails
- Enterprise-grade scheduling with APScheduler

# Troubleshooting
Common Solutions:
- "SMTP Error" → Check Gmail App Password is correct and active
- "City not found" → Verify city format: "City,CountryCode" (e.g., "London,UK")
- "API Error" → Confirm OpenWeatherMap API key is active and valid
- No email at scheduled time → Computer was asleep - add misfire_grace_time=None to scheduler job
- Multiple emails sent → Duplicate jobs - add replace_existing=True to scheduler job
- Service not starting → Verify Python and script paths are correct in launchd plist file
- "ModuleNotFoundError: No module named 'apscheduler'" → Run pip install apscheduler pytz requests
- Email sends at wrong time → Check timezone in CronTrigger (should match your location)

Logs Show:
- ✅ Successful sends with timestamps
- ❌ Failed attempts with error details
- 🔄 Automatic retry status

Debug Mode:
For troubleshooting, run manually:

```bash

# Deactivate service first
launchctl stop com.user.weatherdaemon

# Run in foreground with verbose output
cd /path/to/your/project
source venv/bin/activate
python -v weather_daemon.py
```

# Project Status
✅ Production Ready - This system has been running reliably with daily deliveries

---
![WeatherNotificationEmail ](https://github.com/user-attachments/assets/6ef0a5fe-d2e1-41e0-85d1-82f0782db2fb)  

![WeatherNotificationEmail(2)](https://github.com/user-attachments/assets/0d763a85-d8f2-4e25-9f7b-8f4ef26a1914)  


Start your day informed, without lifting a finger. ☕🌤️  
Sips tea ☺️ 




