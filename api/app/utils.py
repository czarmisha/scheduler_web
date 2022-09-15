import os
import requests
from dotenv import load_dotenv

from app import db
from .models import Event

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
token = os.environ['BOT_TOKEN']

def send_message(chat_id, text):
    method = "sendMessage"
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)

def get_events(start, end):
    events = Event.query.filter(Event.start > start, Event.end < end).order_by(Event.start).all()
    return events