import time
import schedule
from datetime import datetime
import os
import sys

# Add your project path - replace with your actual project directory
sys.path.append('/path/to/your/project/directory')


def send_weather_with_retry():
    try:
        from weather_cron import send_daily_weather
        print(f"🕒 Attempting to send weather email at {datetime.now().strftime('%H:%M:%S')}")
        send_daily_weather()
    except Exception as e:
        print(f"❌ Failed: {e}")
        print("🔄 Retrying in 30 seconds...")
        time.sleep(30)
        try:
            send_daily_weather()
            print("✅ Success on retry!")
        except Exception as e2:
            print(f"❌ Failed again: {e2}")


def run_reliable_daemon():
    print(f"🚀 RELIABLE Weather Daemon Started at {datetime.now()}")
    print("📧 Will send emails daily at 9:30 AM with retry logic")

    # Schedule for 9:30 AM daily (changed from 09:00 to 09:30)
    schedule.every().day.at("09:30").do(send_weather_with_retry)

    # Also send a test immediately
    print("🚀 Sending test email now...")
    send_weather_with_retry()

    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


if __name__ == "__main__":
    run_reliable_daemon()
