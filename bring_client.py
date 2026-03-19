"""Bring! Shopping List API Client Wrapper."""

import asyncio
import aiohttp
from bring_api import Bring, BringItemOperation


async def get_bring_lists(email: str, password: str) -> list[dict]:
    """Login and return all available shopping lists."""
    async with aiohttp.ClientSession() as session:
        bring = Bring(session, email, password)
        await bring.login()
        result = await bring.load_lists()
        return result["lists"]


async def add_items_to_list(
    email: str,
    password: str,
    list_uuid: str,
    items: list[dict],
) -> None:
    """Add grocery items to a Bring! shopping list.

    Args:
        email: Bring! account email.
        password: Bring! account password.
        list_uuid: UUID of the target shopping list.
        items: List of dicts with 'name' and optional 'specification'.
              Example: [{"name": "Tomaten", "specification": "500g"},
                        {"name": "Milch"}]
    """
    async with aiohttp.ClientSession() as session:
        bring = Bring(session, email, password)
        await bring.login()

        bring_items = []
        for item in items:
            bring_items.append(
                {
                    "itemId": item["name"],
                    "spec": item.get("specification", ""),
                }
            )

        await bring.batch_update_list(
            list_uuid,
            bring_items,
            BringItemOperation.ADD,
        )


async def select_list_interactive(email: str, password: str) -> str:
    """Show available lists and let the user pick one. Returns the list UUID."""
    lists = await get_bring_lists(email, password)

    if not lists:
        raise RuntimeError("Keine Einkaufslisten in deinem Bring!-Konto gefunden.")

    if len(lists) == 1:
        chosen = lists[0]
        print(f"Einzige Liste gefunden: \"{chosen['name']}\"")
        return chosen["listUuid"]

    print("\nVerfuegbare Bring!-Listen:")
    for i, lst in enumerate(lists, 1):
        print(f"  {i}. {lst['name']}")

    while True:
        try:
            choice = int(input("\nWaehle eine Liste (Nummer): "))
            if 1 <= choice <= len(lists):
                chosen = lists[choice - 1]
                print(f"Gewaehlt: \"{chosen['name']}\"")
                return chosen["listUuid"]
        except (ValueError, EOFError):
            pass
        print("Ungueltige Eingabe, bitte erneut versuchen.")
