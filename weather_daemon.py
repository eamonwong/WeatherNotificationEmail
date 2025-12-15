import time
import signal
import sys
import os
import random
import logging
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add your project path - replace with your actual project directory
sys.path.append('/path/to/your/project/directory')


def send_weather():
    try:
        from weatherEmail import send_daily_weather
        current_time = datetime.now().strftime('%H:%M:%S')
        logger.info(f"🕒 [{current_time}] Sending weather email...")
        send_daily_weather()
    except Exception as e:
        logger.error(f"❌ Error: {e}")

def main():
    logger.info(f"🚀 Weather Daemon Started at {datetime.now()}")

    scheduler = BackgroundScheduler()

    minute = 30

    # Schedule for morning (adjust timezone if needed)
    scheduler.add_job(
        send_weather,
        CronTrigger(hour=9, minute=minute, timezone='Europe/London'),
        id='daily_weather'
    )
    logger.info(f"📧 Scheduled: Daily at 09:{minute:02d}")

    # Keep-alive heartbeat (every 30 minutes)
    scheduler.add_job(
        lambda: logger.info(f"💚 Daemon alive at {datetime.now().strftime('%H:%M:%S')}"),
        'interval',
        minutes=30,
        id='heartbeat'
    )

    # Test immediately
    logger.info("🚀 Sending test email now...")
    send_weather()

    scheduler.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("\n👋 Shutting down daemon...")
        scheduler.shutdown()
        logger.info("✅ Daemon stopped cleanly")

if __name__ == "__main__":
    main()

