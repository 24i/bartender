import json

class APIClient:


    def fetch_drinks(self):
        return json.loads('[{"id": 1,"name": "Moscow Mule"},{"id": 2,"name": "Sex on the Beach"},{"id": 3,"name": "Dark & Stormy"},{"id": 4,"name": "Vodka Coke"}]')