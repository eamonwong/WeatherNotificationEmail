import time
import schedule
from datetime import datetime
import os
import sys

# Add your project path - replace with your actual project directory
sys.path.append('/path/to/your/project/directory')


def send_weather():
    try:
        from weatherEmail import send_daily_weather
        current_time = datetime.now().strftime('%H:%M:%S')
        print(f"🕒 [{current_time}] Sending weather email...")
        send_daily_weather()
    except Exception as e:
        print(f"❌ [{current_time}] Error: {e}")


def main():
    print(f"🚀 RELIABLE Weather Daemon Started at {datetime.now()}")
    print("📧 Scheduled: Daily at 09:30")
    print("💚 Will log every hour to stay alive")

    # Schedule for 9:30 AM
    schedule.every().day.at("09:30").do(send_weather)

    schedule.every().hour.do(lambda: print(f"💚 Alive at {datetime.now().strftime('%H:%M:%S')}"))

    print("🚀 Sending test email now...")
    send_weather()

    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
        except Exception as e:
            print(f"❌ Daemon error: {e}")
            time.sleep(60)


if __name__ == "__main__":
    main()
