# Grocery List Automation

Automatische Erstellung eines Wochenessensplans mit KI und direktem Import in die **Bring!** Einkaufslisten-App.

## Funktionsweise

1. **Claude AI** generiert einen ausgewogenen Wochenessensplan (Mittag + Abendessen)
2. Beruecksichtigt deine Essenswuensche, vegane Tage und ALDI-Verfuegbarkeit
3. Aus dem Plan wird automatisch eine konsolidierte Einkaufsliste erstellt
4. Die Einkaufsliste wird direkt in deine **Bring!**-App gepusht

## Setup

```bash
# Dependencies installieren
pip install -r requirements.txt

# Konfiguration anlegen
cp .env.example .env
# .env mit deinen Daten ausfuellen
```

### Benoetigte Zugangsdaten

| Variable | Beschreibung |
|---|---|
| `BRING_EMAIL` | Deine Bring!-Login-E-Mail |
| `BRING_PASSWORD` | Dein Bring!-Passwort |
| `ANTHROPIC_API_KEY` | Dein Anthropic API-Key |

### Optionale Einstellungen

| Variable | Standard | Beschreibung |
|---|---|---|
| `HOUSEHOLD_SIZE` | 2 | Anzahl Personen |
| `MEAL_PLAN_DAYS` | 7 | Tage im Essensplan |
| `DIETARY_PREFERENCES` | - | z.B. "vegetarisch, glutenfrei" |
| `VEGAN_DAYS` | - | Kommagetrennte vegane Tage, z.B. "Mittwoch, Freitag" |
| `ALDI_MODE` | false | Nur ALDI-verfuegbare Zutaten vorschlagen |

## Essenswuensche

In der Datei `essenswuensche.json` kannst du deine Vorlieben pflegen:

```json
{
  "wuensche": [
    "Pasta Bolognese",
    "Gemueselasagne",
    "Thai Curry mit Reis"
  ],
  "ausschluesse": [
    "Innereien",
    "Meeresfruechte"
  ],
  "notizen": "Gerne saisonale Gerichte. Nicht zu kompliziert, max. 45 Min. Zubereitung."
}
```

- **wuensche**: Gerichte, die moeglichst im Plan auftauchen sollen
- **ausschluesse**: Zutaten/Gerichte, die NICHT verwendet werden sollen
- **notizen**: Freie Hinweise an die KI (Zubereitungszeit, Saisonalitaet, etc.)

## Verwendung

```bash
python main.py
```

Das Script:
1. Laedt deine Essenswuensche und Einstellungen
2. Generiert einen Essensplan (mit veganen Tagen und ALDI-Modus falls aktiv)
3. Zeigt Plan und Einkaufsliste an
4. Fragt, welche Bring!-Liste verwendet werden soll
5. Fragt zur Bestaetigung, bevor Artikel hinzugefuegt werden
6. Pusht alle Zutaten auf die gewaehlte Bring!-Liste
