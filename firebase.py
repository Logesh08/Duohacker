import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
from decouple import config
from datetime import datetime
from pytz import timezone

def initialize_firebase():
    cred = credentials.Certificate("secrects/key.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': config('DB_REF')
    })

def writeXp(count):
    container_name = os.environ.get("CONTAINER_NAME")
    ref = db.reference('/containers')
    container_ref = ref.child(container_name)
    current_value = container_ref.child('xp').get() or 0
    updated_value = current_value + count
    container_ref.update({'xp': updated_value})

def writeFailed():
    container_name = os.environ.get("CONTAINER_NAME")
    ref = db.reference('/containers')
    container_ref = ref.child(container_name)
    current_value = container_ref.child('failed').get() or 0
    updated_value = current_value + 1
    container_ref.update({'failed': updated_value})

def savePrevious(xp,failed):
    container_name = os.environ.get("CONTAINER_NAME")
    time_stamp = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d-%H')
    ref = db.reference('/history/'+str(time_stamp))
    container_ref = ref.child(container_name)
    container_ref.set({'failed': failed,'xp': xp})

def disposePrevious():
    container_name = os.environ.get("CONTAINER_NAME")
    ref = db.reference('/containers')
    container_ref = ref.child(container_name)
    xp = container_ref.child('xp').get() or 0
    failed = container_ref.child('failed').get() or 0
    savePrevious(xp,failed)
    container_ref.update({'xp': None, 'failed': None})