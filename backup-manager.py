import os
import time
import datetime
import schedule
import shutil

import config as CONFIG

def create_backup():
    '''
    Creates the backup
    '''
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(CONFIG.BACKUP_DIR, f"backup_{timestamp}")

    try:
        shutil.copytree(CONFIG.TARGET, backup_path)
        print(f"Backup was created: {backup_path}")
    except Exception as ex:
        print(f"Error: {ex}")

def delete_backups():
    '''
    Deletes the backup
    '''
    now = datetime.datetime.now()
    retention_period = datetime.timedelta(days=CONFIG.DAYS_TO_EXPIRE)
    
    for backup in os.listdir(CONFIG.BACKUP_DIR):
        backup_path = os.path.join(CONFIG.BACKUP_DIR, backup)
        if os.path.isdir(backup_path):
            try:
                backup_time_str = backup.split("_")[1] + "_" + backup.split("_")[2]
                backup_time = datetime.datetime.strptime(backup_time_str, "%Y%m%d_%H%M%S")
                if now - backup_time > retention_period:
                    shutil.rmtree(backup_path)
                    print(f"Backup was deleted: {backup_path}")
            except Exception as e:
                print(f"Error: {backup}: {e}")

def main():
    create_backup()
    delete_backups()

for backup_time in CONFIG.TIME_TO_BACKUP:
    schedule.every().day.at(backup_time).do(main)

if not os.path.exists(CONFIG.BACKUP_DIR):
    os.makedirs(CONFIG.BACKUP_DIR)

print(f"{CONFIG.TARGET}: BACKUP MANAGER STARTED")
while True:
    schedule.run_pending()
    time.sleep(60)