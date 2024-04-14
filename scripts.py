import psutil
import requests
import time

API_URL = "http://flask_app:8080/alarm"


def send_alarm():
    try:
        response = requests.post(API_URL)
        if response.status_code == 200:
            print("Alarm successfully sent")
        else:
            print("Failed to send alarm")
    except Exception as e:
        print("Error:", e)


def monitor_memory():
    while True:

        memory_percent = psutil.virtual_memory().percent
        print("Memory usage:", memory_percent)

        if memory_percent > 80:
            send_alarm()

        time.sleep(60)


if __name__ == "__main__":
    monitor_memory()
