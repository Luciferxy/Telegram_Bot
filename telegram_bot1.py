import os
import requests
import time
from dotenv import load_dotenv
from email__crew import run_email_agent  

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

def get_updates(offset=None):
    params = {"timeout": 30, "offset": offset}
    response = requests.get(f"{BASE_URL}/getUpdates", params=params)
    return response.json()

def send_message(chat_id, text):
    if not isinstance(text, str):  
        text = str(text)  

    payload = {"chat_id": chat_id, "text": text}
    
    try:
        response = requests.post(f"{BASE_URL}/sendMessage", json=payload)
        if response.status_code != 200:
            print(f"⚠️ Telegram API Error: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"🚨 Error sending message to Telegram: {e}")

def clear_old_updates():
    updates = get_updates()
    if "result" in updates and updates["result"]:
        last_update_id = updates["result"][-1]["update_id"]
        return last_update_id + 1
    return None

def main():
    last_update_id = clear_old_updates() 

    while True:
        updates = get_updates(last_update_id)

        if "result" in updates:
            for update in updates["result"]:
                last_update_id = update["update_id"] + 1
                if "message" in update and "text" in update["message"]:
                    chat_id = update["message"]["chat"]["id"]
                    user_message = update["message"]["text"].strip()

                    print(f"📩 Received: {user_message}")

                    send_message(chat_id, "Processing your email request, please wait...")
                    email_response = run_email_agent(user_message) 
                    send_message(chat_id, email_response)

        time.sleep(2)  

if __name__ == "__main__":
    main()