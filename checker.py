import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
from notifier import send_push

NTFY_TOPIC = "werdertickets_test"

def hole_bestellfristen(url: str):
    #url = "https://www.werder.de/tickets/maenner/heimspiele"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    bestellfristen = []

    # Abschnitt oder Tabelle mit Bestellfristen suchen
    bestell_section = soup.find("h2", string="Bestellfristen")
    if bestell_section:
        table = bestell_section.find_next("table")
        if table:
            for row in table.find_all("tr")[1:]:  # Header überspringen
                cols = row.find_all("td")
                if len(cols) >= 3:
                    spieltermin = cols[0].get_text(strip=True)
                    partie = cols[1].get_text(strip=True)
                    bestellphase = cols[2].get_text(strip=True)
                    bestellfristen.append({
                        "spieltermin": spieltermin,
                        "partie": partie,
                        "bestellphase": bestellphase
                    })
    return bestellfristen

def compare_start_date(date_range: str) -> bool:
    """
    Prüft, ob das Startdatum eines Datumsbereichs heute ist.

    Unterstützte Formate:
    - '08.-15.07.2025'
    - '27.10.-03.11.2025'
    - '05.12.2025' oder 'ab 05.12.2025'

    :param date_range: String mit Datumsbereich oder Startdatum
    :return: True, wenn Startdatum heute ist, sonst False
    """
    #today = date(2025, 10, 6)
    today = datetime.today().date()

    # Erstmal nur Zahlen extrahieren (Tag.Monat.Jahr)
    match = re.search(r'(\d{1,2})\.?(\d{1,2})?\.?(\d{4})?', date_range)
    if not match:
        return False  # kein Datum gefunden

    start_day = int(match.group(1))
    start_month = int(match.group(2)) if match.group(2) else None
    year = int(match.group(3)) if match.group(3) else today.year

    # Wenn Monat fehlt, versuchen vom zweiten Teil des Bereichs zu übernehmen
    if not start_month:
        # Beispiel: "05.-07.12.2025"
        match_end = re.search(r'-\s*(\d{1,2})\.(\d{1,2})\.(\d{4})', date_range)
        if match_end:
            start_month = int(match_end.group(2))
            year = int(match_end.group(3))
        else:
            start_month = today.month  # Default: heutiger Monat

    try:
        start_date = date(year, start_month, start_day)
    except ValueError:
        return False  # ungültiges Datum

    return start_date == today



def compare_end_date(date_range: str) -> bool:
    """
    Prüft, ob heute der Tag vor dem Enddatum eines Datumsbereichs ist.

    Unterstützte Formate:
    - '08.-15.07.2025'
    - '27.10.-03.11.2025'
    - '05.12.2025' oder 'bis 05.12.2025'

    :param date_range: String mit Datumsbereich oder Enddatum
    :return: True, wenn heute einen Tag vor dem Enddatum ist, sonst False
    """
    today = datetime.today().date()
    #today = date(2025, 10, 12)

    # Prüfen, ob es einen Bereich gibt (mit Bindestrich)
    match_range = re.search(r'-(\d{1,2})\.?(\d{1,2})?\.?(\d{4})?', date_range)
    if match_range:
        end_day = int(match_range.group(1))
        end_month = int(match_range.group(2)) if match_range.group(2) else None
        year = int(match_range.group(3)) if match_range.group(3) else today.year

        # Wenn Monat fehlt, vom Startdatum übernehmen
        if not end_month:
            match_start = re.search(r'(\d{1,2})\.?(\d{1,2})?\.?(\d{4})?', date_range)
            if match_start and match_start.group(2):
                end_month = int(match_start.group(2))
                if not match_range.group(3):
                    year = int(match_start.group(3)) if match_start.group(3) else today.year
            else:
                end_month = today.month

    else:
        # Kein Bereich, einzelnes Datum nehmen
        match_single = re.search(r'(\d{1,2})\.?(\d{1,2})?\.?(\d{4})?', date_range)
        if not match_single:
            return False
        end_day = int(match_single.group(1))
        end_month = int(match_single.group(2)) if match_single.group(2) else today.month
        year = int(match_single.group(3)) if match_single.group(3) else today.year

    try:
        end_date = date(year, end_month, end_day)
    except ValueError:
        return False

    # Prüfen, ob heute einen Tag vor dem Enddatum ist
    return today == (end_date - timedelta(days=1))

