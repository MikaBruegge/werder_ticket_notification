import requests

def send_push(topic: str, title: str, message: str):
    url = f"https://ntfy.sh/{topic}"
    headers = {
        "Title": title,
        "Priority": "high"
    }
    response = requests.post(url, data=message.encode("utf-8"), headers=headers)
    try:
        response.raise_for_status()
        print("Push erfolgreich gesendet!")
    except Exception as e:
        print("Fehler beim Senden:", e)

#if __name__ == "__main__":
#    send_push(NTFY_TOPIC, "Test Push", "Das ist eine Testnachricht von deinem Bot.")
