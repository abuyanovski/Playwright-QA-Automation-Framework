from datetime import datetime
import random


def generate_user():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    return {
        "first_name": "Anton",
        "last_name": "QA",
        "address": "123 Test Street",
        "city": "Seattle",
        "state": "WA",
        "zip_code": "98101",
        "phone": "2065551234",
        "ssn": "123456789",
        "username": f"qa_user_{timestamp}_{random.randint(1000, 9999)}",
        "password": "TestPass123!"
    }
