from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from api.jobs.hotspot_job import recompute_hotspots

scheduler = BackgroundScheduler()

def background_hotspot_job():
    print("⏰ Scheduler triggered at", datetime.utcnow())
    recompute_hotspots()

def start_scheduler():
    scheduler.add_job(
        background_hotspot_job,
        trigger="interval",
        hours=6,
        id="hotspot_recompute",
        replace_existing=True
    )
    scheduler.start()
