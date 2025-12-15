import smtplib
import requests
import time
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

OPENWEATHER_API_KEY = "YOUR_API_KEY_HERE"  # Get from: https://openweathermap.org/api
CITY = "your_location" # Your location
EMAIL_USER = "your_email@gmail.com"  # Your Gmail address
EMAIL_PASSWORD = "your_app_password"  # Gmail app password
TO_EMAIL = "recipient@email.com"  # Where to send weather emails

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds


def setup_email():
    """Connect to email server with retry logic"""
    for attempt in range(MAX_RETRIES):
        try:
            smtp = smtplib.SMTP('smtp.gmail.com', 587, timeout=30)
            smtp.ehlo()
            smtp.starttls()
            smtp.login(EMAIL_USER, EMAIL_PASSWORD)
            logger.info("Successfully connected to email server")
            return smtp
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                logger.warning(f"Email connection attempt {attempt + 1} failed: {e}. Retrying...")
                time.sleep(RETRY_DELAY)
            else:
                logger.error(f"Failed to connect to email server after {MAX_RETRIES} attempts: {e}")
                raise


def get_daily_forecast():
    """Get today's weather forecast with retry logic"""
    for attempt in range(MAX_RETRIES):
        try:
            url = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={OPENWEATHER_API_KEY}&units=metric"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            city_name = data['city']['name']
            today = datetime.now().date()

            # Filter forecasts for today only
            todays_forecasts = []
            for forecast in data['list']:
                forecast_date = datetime.fromtimestamp(forecast['dt']).date()
                if forecast_date == today:
                    todays_forecasts.append(forecast)

            if not todays_forecasts:
                logger.warning("No forecast data available for today")
                return None

            # Calculate min/max temps for today
            min_temp = min([f['main']['temp_min'] for f in todays_forecasts])
            max_temp = max([f['main']['temp_max'] for f in todays_forecasts])

            # Get most common weather condition for today
            conditions = [f['weather'][0]['description'] for f in todays_forecasts]
            main_condition = max(set(conditions), key=conditions.count)

            # Get current weather
            current_url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={OPENWEATHER_API_KEY}&units=metric"
            current_response = requests.get(current_url, timeout=10)
            current_response.raise_for_status()
            current_data = current_response.json()

            return {
                'city': city_name,
                'current_temp': current_data['main']['temp'],
                'current_condition': current_data['weather'][0]['description'].title(),
                'today_min': min_temp,
                'today_max': max_temp,
                'today_condition': main_condition.title(),
                'humidity': current_data['main']['humidity'],
                'feels_like': current_data['main']['feels_like'],
                'wind_speed': current_data['wind']['speed']
            }

        except requests.exceptions.RequestException as e:
            if attempt < MAX_RETRIES - 1:
                logger.warning(f"Weather API attempt {attempt + 1} failed: {e}. Retrying...")
                time.sleep(RETRY_DELAY)
            else:
                logger.error(f"Failed to get weather data after {MAX_RETRIES} attempts: {e}")
                return None
        except Exception as e:
            logger.error(f"Unexpected error getting forecast: {e}")
            return None


def create_weather_message(weather):
    """Create a friendly daily weather message"""
    if not weather:
        return "Sorry, couldn't get weather data today. ☹️"

    return f"""
🌤️ Your Daily Weather Forecast for {weather['city']}
📅 {datetime.now().strftime('%A, %B %d, %Y')}

RIGHT NOW:
• Temperature: {weather['current_temp']:.1f}°C
• Feels like: {weather['feels_like']:.1f}°C
• Conditions: {weather['current_condition']}
• Humidity: {weather['humidity']}%
• Wind: {weather['wind_speed']} m/s

TODAY'S FORECAST:
• High: {weather['today_max']:.1f}°C
• Low: {weather['today_min']:.1f}°C  
• Overall: {weather['today_condition']}

Have a wonderful day! ☀️
"""


def send_daily_weather():
    """Send the daily weather email with proper error handling"""
    logger.info(f"Starting daily forecast at {datetime.now().strftime('%H:%M:%S')}")

    # Get weather data
    weather = get_daily_forecast()
    if not weather:
        logger.error("Failed to retrieve weather data")
        return

    message_text = create_weather_message(weather)

    # Create email
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = TO_EMAIL
    msg['Subject'] = f"🌤️ Daily Weather - {datetime.now().strftime('%m/%d')}"
    msg.attach(MIMEText(message_text))

    # Send email
    try:
        smtp = setup_email()
        smtp.sendmail(from_addr=EMAIL_USER, to_addrs=[TO_EMAIL], msg=msg.as_string())
        smtp.quit()
        logger.info("✅ Daily weather forecast sent successfully!")
    except Exception as e:
        logger.error(f"❌ Failed to send email: {e}")
