import requests

TOKEN = "8485762290:AAECB_dUuXbgDaIub-dKxFWNd9cFAR7IFBw"
WEBHOOK_URL = "https://ziyoilm.page.gd/webhook.php"

def set_webhook():
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
    params = {"url": WEBHOOK_URL}
    response = requests.post(url, json=params)
    print(response.json())

if __name__ == "__main__":
    set_webhook()
