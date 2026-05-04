from apscheduler.schedulers.background import BackgroundScheduler
from services.processor import process_all
from services.tourism_processor import process_country

scheduler = BackgroundScheduler()

def weekly_job():
    print("🚀 WEEKLY JOB STARTED")

    try:
        process_all()
        process_country()
        print("✅ WEEKLY JOB COMPLETED")

    except Exception as e:
        print("❌ WEEKLY JOB ERROR:", e)


def start_scheduler():
    # every 7 days run (168 hours)
    scheduler.add_job(weekly_job, "interval", days=3)

    scheduler.start()
    print("🟢 Scheduler Started (Runs every 7 days)")