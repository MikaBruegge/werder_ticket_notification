from notifier import send_push
from checker import hole_bestellfristen, compare_start_date, compare_end_date


# Dein ntfy Topic hier eintragen
NTFY_TOPIC = "werdertickets_test"

bestellfristen_heim = hole_bestellfristen("https://www.werder.de/tickets/maenner/heimspiele")
bestellfristen_ausw = hole_bestellfristen("https://www.werder.de/tickets/maenner/auswaertsspiele")


for eintrag in bestellfristen_heim:
    phase = eintrag['bestellphase'].split(",")[0]
    if compare_start_date(phase):
        #print(f"Bestellphase öffnet heute für Werder vs {eintrag['partie']} am {eintrag['spieltermin']}")
        send_push(NTFY_TOPIC, "Bestellphase Heim beginnt", f"Bestellphase öffnet heute für Werder vs {eintrag['partie']} am {eintrag['spieltermin']}")

for eintrag in bestellfristen_ausw:
    phase = eintrag['bestellphase'].split(",")[0]
    if compare_start_date(phase):
        #print(f"Bestellphase öffnet heute für Werder vs {eintrag['partie']} am {eintrag['spieltermin']}")
        send_push(NTFY_TOPIC, "Bestellphase Auswaerts beginnt", f"Bestellphase öffnet heute für Werder vs {eintrag['partie']} am {eintrag['spieltermin']}")



for eintrag in bestellfristen_heim:
    phase = eintrag['bestellphase'].split(",")[0]
    if compare_end_date(phase):
        #print(f"Bestellphase öffnet heute für Werder vs {eintrag['partie']} am {eintrag['spieltermin']}")
        send_push(NTFY_TOPIC, "Bestellphase Heim begendetinnt", f"Bestellphase endet morgen für Werder vs {eintrag['partie']} am {eintrag['spieltermin']}")

for eintrag in bestellfristen_ausw:
    phase = eintrag['bestellphase'].split(",")[0]
    if compare_end_date(phase):
        #print(f"Bestellphase öffnet heute für Werder vs {eintrag['partie']} am {eintrag['spieltermin']}")
        send_push(NTFY_TOPIC, "Bestellphase Auswaerts endet", f"Bestellphase endet morgen für Werder vs {eintrag['partie']} am {eintrag['spieltermin']}")