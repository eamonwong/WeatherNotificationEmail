import smtplib
import requests
import schedule
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

OPENWEATHER_API_KEY = "YOUR_API_KEY_HERE"  # Get from: https://openweathermap.org/api
CITY = "your_location" # Your location
EMAIL_USER = "your_email@gmail.com"  # Your Gmail address
EMAIL_PASSWORD = "your_app_password"  # Gmail app password
TO_EMAIL = "recipient@email.com"  # Where to send weather emails


def setup_email():
    """Connect to email server"""
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(EMAIL_USER, EMAIL_PASSWORD)
    return smtp


def get_daily_forecast():
    """Get today's weather forecast"""
    try:
        # Use the 5-day forecast API
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={OPENWEATHER_API_KEY}&units=metric"
        data = requests.get(url).json()

        city_name = data['city']['name']
        today = datetime.now().date()

        # Filter forecasts for today only
        todays_forecasts = []
        for forecast in data['list']:
            forecast_date = datetime.fromtimestamp(forecast['dt']).date()
            if forecast_date == today:
                todays_forecasts.append(forecast)

        if not todays_forecasts:
            return None

        # Calculate min/max temps for today
        min_temp = min([f['main']['temp_min'] for f in todays_forecasts])
        max_temp = max([f['main']['temp_max'] for f in todays_forecasts])

        # Get most common weather condition for today
        conditions = [f['weather'][0]['description'] for f in todays_forecasts]
        main_condition = max(set(conditions), key=conditions.count)

        # Get current weather
        current_url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={OPENWEATHER_API_KEY}&units=metric"
        current_data = requests.get(current_url).json()

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

    except Exception as e:
        print(f"Weather API error: {e}")
        return None


def create_weather_message(weather):
    """Create a friendly daily weather message"""
    if not weather:
        return "Sorry, couldn't get weather data today. ☹️"

    return f"""
🌤️ Your Daily Weather Forecast for {weather['city']}
📅 {datetime.now().strftime('%A, %B %d %Y')}

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
    """Send the daily weather email"""
    print(f"🌤️ Sending daily forecast at {datetime.now().strftime('%H:%M')}...")

    # Get weather data
    weather = get_daily_forecast()
    message_text = create_weather_message(weather)

    # Create email
    msg = MIMEMultipart()
    msg['Subject'] = f"🌤️ Daily Weather - {datetime.now().strftime('%m/%d')}"
    msg.attach(MIMEText(message_text))

    # Send email
    try:
        smtp = setup_email()
        smtp.sendmail(from_addr=EMAIL_USER, to_addrs=[TO_EMAIL], msg=msg.as_string())
        smtp.quit()
        print("✅ Daily weather forecast sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

if __name__ == "__main__":
    # Simple test mode - send one email and exit
    send_daily_weather()
