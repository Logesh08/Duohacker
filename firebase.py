import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
from decouple import config

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

def disposePrevious():
    container_name = os.environ.get("CONTAINER_NAME")
    ref = db.reference('/containers')
    container_ref = ref.child(container_name)
    container_ref.update({'xp': None, 'failed': None})