#!/usr/bin/env python3
"""Grocery List Automation: Generate a meal plan and push items to Bring!"""

import asyncio
import os
import sys

from dotenv import load_dotenv

from bring_client import add_items_to_list, select_list_interactive
from meal_planner import generate_meal_plan


def print_meal_plan(plan: dict) -> None:
    """Pretty-print the generated meal plan."""
    print("\n" + "=" * 50)
    print("  WOCHENPLAN")
    print("=" * 50)
    for meal in plan["meals"]:
        print(f"\n  {meal['day']}:")
        print(f"    Mittag: {meal['lunch']}")
        print(f"    Abend:  {meal['dinner']}")

    print("\n" + "=" * 50)
    print("  EINKAUFSLISTE")
    print("=" * 50)
    for item in plan["grocery_list"]:
        spec = item.get("specification", "")
        spec_str = f" ({spec})" if spec else ""
        print(f"  - {item['name']}{spec_str}")
    print()


def main() -> None:
    load_dotenv()

    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    bring_email = os.getenv("BRING_EMAIL")
    bring_password = os.getenv("BRING_PASSWORD")
    household_size = int(os.getenv("HOUSEHOLD_SIZE", "2"))
    days = int(os.getenv("MEAL_PLAN_DAYS", "7"))
    preferences = os.getenv("DIETARY_PREFERENCES", "")

    if not anthropic_key:
        print("Fehler: ANTHROPIC_API_KEY nicht gesetzt. Siehe .env.example")
        sys.exit(1)
    if not bring_email or not bring_password:
        print("Fehler: BRING_EMAIL und BRING_PASSWORD muessen gesetzt sein. Siehe .env.example")
        sys.exit(1)

    # 1. Generate meal plan with Claude
    print("Erstelle Essensplan mit Claude...")
    plan = generate_meal_plan(
        api_key=anthropic_key,
        days=days,
        household_size=household_size,
        preferences=preferences,
    )
    print_meal_plan(plan)

    # 2. Select Bring! list
    print("Verbinde mit Bring!...")
    list_uuid = asyncio.run(select_list_interactive(bring_email, bring_password))

    # 3. Confirm before adding
    item_count = len(plan["grocery_list"])
    answer = input(
        f"\n{item_count} Artikel auf die Bring!-Liste setzen? (j/n): "
    ).strip().lower()

    if answer not in ("j", "ja", "y", "yes"):
        print("Abgebrochen.")
        sys.exit(0)

    # 4. Push items to Bring!
    print("Fuege Artikel zur Bring!-Liste hinzu...")
    asyncio.run(
        add_items_to_list(bring_email, bring_password, list_uuid, plan["grocery_list"])
    )
    print(f"Fertig! {item_count} Artikel wurden zur Bring!-Liste hinzugefuegt.")


if __name__ == "__main__":
    main()
