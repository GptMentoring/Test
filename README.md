# Grocery List Automation

Automatische Erstellung eines Wochenessensplans mit KI und direktem Import in die **Bring!** Einkaufslisten-App.

## Funktionsweise

1. **Claude AI** generiert einen ausgewogenen Wochenessensplan (Mittag + Abendessen)
2. Aus dem Plan wird automatisch eine konsolidierte Einkaufsliste erstellt
3. Die Einkaufsliste wird direkt in deine **Bring!**-App gepusht

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

## Verwendung

```bash
python main.py
```

Das Script:
1. Generiert einen Essensplan und zeigt ihn an
2. Fragt, welche Bring!-Liste verwendet werden soll
3. Fragt zur Bestaetigung, bevor Artikel hinzugefuegt werden
4. Pusht alle Zutaten auf die gewaehlte Bring!-Liste
