"""Meal plan and grocery list generator using Claude API."""

import json
import anthropic


SYSTEM_PROMPT = """\
Du bist ein erfahrener Koch und Ernaehrungsberater. Du erstellst ausgewogene, \
alltagstaugliche Wochenspeiseplaene mit passender Einkaufsliste.

Antworte AUSSCHLIESSLICH mit validem JSON im folgenden Format:
{
  "meals": [
    {
      "day": "Montag",
      "lunch": "Gericht-Name",
      "dinner": "Gericht-Name"
    }
  ],
  "grocery_list": [
    {
      "name": "Zutat",
      "specification": "Menge/Details"
    }
  ]
}

Wichtige Regeln fuer die Einkaufsliste:
- Fasse gleiche Zutaten zusammen (z.B. nicht 3x Tomaten separat)
- Gib realistische Mengen an, die im Supermarkt erhaeltlich sind
- Grundzutaten wie Salz, Pfeffer, Oel koennen weggelassen werden
- Schreibe Zutaten so, wie man sie im Supermarkt findet
- Die specification sollte Menge und ggf. Details enthalten (z.B. "500g", "1 Bund", "200g, bio")
"""


def generate_meal_plan(
    api_key: str,
    days: int = 7,
    household_size: int = 2,
    preferences: str = "",
    vegan_days: list[str] | None = None,
    aldi_mode: bool = False,
    wishes: dict | None = None,
) -> dict:
    """Generate a weekly meal plan with grocery list using Claude.

    Args:
        api_key: Anthropic API key.
        days: Number of days to plan.
        household_size: Number of people.
        preferences: Dietary preferences string.
        vegan_days: List of day names that should be vegan (e.g. ["Mittwoch", "Freitag"]).
        aldi_mode: If True, only suggest ALDI-available ingredients.
        wishes: Dict from essenswuensche.json with 'wuensche', 'ausschluesse', 'notizen'.

    Returns:
        Dict with 'meals' and 'grocery_list' keys.
    """
    client = anthropic.Anthropic(api_key=api_key)

    user_prompt = (
        f"Erstelle einen Essensplan fuer {days} Tage fuer {household_size} Personen "
        f"mit Mittag- und Abendessen."
    )

    if preferences:
        user_prompt += f"\n\nErnaehrungsvorlieben/Einschraenkungen: {preferences}"

    if vegan_days:
        days_str = ", ".join(vegan_days)
        user_prompt += (
            f"\n\nWICHTIG: An folgenden Tagen muessen ALLE Gerichte (Mittag und Abend) "
            f"komplett vegan sein: {days_str}. "
            f"Kennzeichne diese Gerichte im Namen nicht extra, sie sollen einfach vegan sein."
        )

    if aldi_mode:
        user_prompt += (
            "\n\nALDI-MODUS: Schlage nur Gerichte vor, deren Zutaten bei ALDI "
            "(ALDI Sued/Nord, Deutschland) erhaeltlich sind. Vermeide exotische oder "
            "spezielle Zutaten, die man nur in Biolaeden oder Feinkostgeschaeften findet. "
            "Nutze gaengige ALDI-Eigenmarken-Produkte wo moeglich."
        )

    if wishes:
        if wishes.get("wuensche"):
            wuensche_str = ", ".join(wishes["wuensche"])
            user_prompt += (
                f"\n\nGewuenschte Gerichte (bitte moeglichst einbauen): {wuensche_str}"
            )
        if wishes.get("ausschluesse"):
            ausschluss_str = ", ".join(wishes["ausschluesse"])
            user_prompt += (
                f"\n\nAusgeschlossene Lebensmittel/Gerichte (NICHT verwenden): {ausschluss_str}"
            )
        if wishes.get("notizen"):
            user_prompt += f"\n\nWeitere Hinweise: {wishes['notizen']}"

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    response_text = message.content[0].text.strip()

    # Handle markdown code blocks
    if response_text.startswith("```"):
        lines = response_text.split("\n")
        lines = lines[1:]  # remove opening ```json
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        response_text = "\n".join(lines)

    return json.loads(response_text)
