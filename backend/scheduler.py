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
    # every 1 days run (24 hours)
    scheduler.add_job(weekly_job, "interval", days=1)

    scheduler.start()
    print("🟢 Scheduler Started (Runs every 3 days)")