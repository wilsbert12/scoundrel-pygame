# Scoundrel

    .------..------..------..------..------..------..------..------..------.
    |S.--. ||C.--. ||O.--. ||U.--. ||N.--. ||D.--. ||R.--. ||E.--. ||L.--. |
    | :/\: || :/\: || :/\: || (\/) || :(): || :/\: || :(): || (\/) || :/\: |
    | :\/: || :\/: || :\/: || :\/: || ()() || (__) || ()() || :\/: || (__) |
    | '--'S|| '--'C|| '--'O|| '--'U|| '--'N|| '--'D|| '--'R|| '--'E|| '--'L|
    `------'`------'`------'`------'`------'`------'`------'`------'`------'
A text-based Python implementation of the card game Scoundrel, playable in the terminal.

## How to play

You move through a dungeon one room at a time. Each room contains 4 cards drawn from a modified deck — a standard 52-card deck with the red face cards (J, Q, K, A of ♥ and ♦) removed, leaving 44 cards. At the start of each room, you can choose to **flee or play** the room. If you flee, the remaining cards get added to the bottom of the deck — you cannot flee two consecutive rooms.

If you stay, choose a card to play. Once you have played 3 of the 4 cards, you move to the next room — the 1 remaining card carries over and the 3 empty slots are refilled from the deck. Each suit has a different effect:

- **♣ / ♠ (black)** — Monsters. They deal damage equal to their rank value (J=11, Q=12, K=13, A=14). If you have a weapon, you can use it to block some of the damage.
- **♥ (red)** — Potions. Heal equal to the card's rank value, up to a max of 20 HP.
- **♦ (red)** — Weapons. Equip the card as your weapon. You can only carry one weapon at a time — equipping a new one loses the old. When facing a monster, you can choose to use your weapon or fight barehanded. Using the weapon reduces the monster's damage by the weapon's rank value. However, the weapon then gets capped and can only be used against monsters of lower rank than the last one you blocked.

You start with 20 HP. The game ends when there are not enough cards left in the deck to refill the room (you win) or your HP hits 0 (you lose).

## Requirements

- Python 3

## Running the game

```
python main.py
```
