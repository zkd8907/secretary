#!/usr/bin/env python3
import os
import time
import signal
import sys
import threading
from datetime import datetime
from main import main
from dotenv import load_dotenv

load_dotenv()

class GracefulScheduler:
    def __init__(self):
        self.running = True
        self.interval = int(os.getenv('SCHEDULE_INTERVAL_MINUTES', '5'))
        self.next_run = time.time() + (self.interval * 60)
        
    def signal_handler(self, signum, frame):
        print(f"\nReceived signal {signum}. Shutting down gracefully...")
        self.running = False
        
    def run_task(self):
        """Run the main task with error handling"""
        try:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting scheduled task...")
            main()
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Task completed successfully")
        except Exception as e:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Task failed with error: {e}")
            import traceback
            traceback.print_exc()
    
    def start(self):
        """Start the scheduler"""
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        print(f"Scheduler started. Running every {self.interval} minutes.")
        print(f"Next run at: {datetime.fromtimestamp(self.next_run).strftime('%Y-%m-%d %H:%M:%S')}")
        print("Press Ctrl+C to stop gracefully...")
        
        # Run once immediately if requested
        if os.getenv('RUN_ON_START', '').lower() == 'true':
            self.run_task()
        
        while self.running:
            current_time = time.time()
            
            if current_time >= self.next_run:
                # Run task in a separate thread to avoid blocking
                task_thread = threading.Thread(target=self.run_task)
                task_thread.daemon = True
                task_thread.start()
                
                # Schedule next run
                self.next_run = current_time + (self.interval * 60)
                print(f"Next run scheduled for: {datetime.fromtimestamp(self.next_run).strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Sleep for 30 seconds before checking again
            time.sleep(30)
        
        print("Scheduler stopped.")

if __name__ == "__main__":
    scheduler = GracefulScheduler()
    try:
        scheduler.start()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received. Exiting...")
        sys.exit(0)