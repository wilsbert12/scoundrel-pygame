from itertools import product
import random

""" Future developement notes:
1. As of now flee adds cards to room in opposite order. Leave or change? Might create interesting new rooms.
2. Add room count instead of "cards in deck"
3. Add room cleaned message
"""



#-----------------------SETUP--------------------------

#creating the deck
black_suits = ['♣', '♠']
red_suits = ['♥', '♦']
ranks_black = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
ranks_red = ['2','3','4','5','6','7','8','9','10']

deck = []
deck.extend(list(product(ranks_black, black_suits)))
deck.extend(list(product(ranks_red, red_suits)))

#shuffle the deck
random.shuffle(deck)

#create an empty weapon slot
weapon = []
weapon_cap = float('inf')

# Setting ranks to values and suits to classes
dict_rank_to_value = {'2':2, '3':3, '4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':11,'Q':12,'K':13,'A':14}



#-----------------------MECHANICS--------------------------

def form_room():
    global deck, room
    room = []
    for i in range(4):
        room.append(deck.pop(0))
    print()
    print("As you enter the dungeon, you look around. This is what you see:")
    print()
    print(room)

def choose_card():
    global room, played_card
    #check for correct input
    choice = None
    while choice is None:
        try:
            #only set choice to number if correct number is entered
            
            choice = int(input("Choose a card to play (enter number): "))
            if choice not in range(1,len(room)+1):
                print("Invalid choice, try again.")
                choice = None
        except ValueError:
            print(f"Please enter a number from 1 - {len(room)}.")
    played_card = room[choice - 1]
    room.pop(choice - 1)
    print()
    print(f'You played the card {played_card}')
    
def card_effect():
    global health, weapon, weapon_cap
    if played_card[1] in black_suits:
        #if you have a weapon and the weapon cap is at least the rank of the card
        if len(weapon) > 0 and weapon_cap >= dict_rank_to_value.get(played_card[0]):
            #player must choose to use weapon or not
            choice = None
            while choice is None:
                try:
                    #only set choice to answer if correct letter is entered
                    choice = input("Do you want to use your weapon to lower the damage. Your weapon cap will decrease (y/n): ")
                    if choice not in ('y','n'):
                        print("Invalid choice, try again.")
                        choice = None
                except ValueError:
                    print(f"Please answer with y or n (yes/no)")
            #if player chooses to use weapon: subtract weapon strength from hit
            if choice == 'y':
                blocked_hit = dict_rank_to_value.get(played_card[0]) - dict_rank_to_value.get(weapon[0])
                #cant gain health from hits, min cap at 0
                if blocked_hit < 0:
                    blocked_hit = 0
                health = health - blocked_hit
                weapon_cap = dict_rank_to_value.get(played_card[0]) - 1
                if health > 0:
                    print(f"You strike with your weapon, blocking some of the blow. You take {blocked_hit} damage. Health: {health}")
                else:
                    loose()
            #otherwise subtract full hit from health
            else:
                health = health - dict_rank_to_value.get(played_card[0])
                print(f"You fight bare handed and take {dict_rank_to_value.get(played_card[0])} damage. Health: {health}")
        #if you dont have a weapon or weapon is too weak
        else:
            damage = dict_rank_to_value.get(played_card[0])
            health = health - damage
            if health > 0:
                if len(weapon) > 0:
                    print(f"Your weapon is too weak for this foe — you fight bare handed and take {damage} damage. Health: {health}")
                else:
                    print(f"You fight bare handed and take {damage} damage. Health: {health}")
            else:
                loose()
    elif played_card[1] == '♥':
        health = health + dict_rank_to_value.get(played_card[0])
        #max health cap at 20
        if health > 20:
            health = 20
        print(f"You look around and find a healing elixir. You drink it and feel your wounds close. Health: {health}.")
    elif played_card[1] == '♦':
        if len(weapon) > 0:
            print(f"You drop your old weapon and pick up a new one with a strength of {played_card[0]}.")
        else:
            print(f"You pick up a weapon with a strength of {played_card[0]} and equip it. You feel stronger.")
        weapon = played_card
        weapon_cap = float('inf')

def refill_room():
    global deck, room
    #1 Karte bleibt immer übrig
    if len(deck) == 1:
        room.append(deck.pop(0))
        win()
    else:  
        for i in range(3):
            room.append(deck.pop(0))
        print()
        print ('your new room is:')
        print(room)
        print()
        print(f'cards in deck:{len(deck)}')

def win():
    print("""
    You clear the final room and look around — silence at last.
    You look around at the scattered cards, the broken weapons, the empty potion vials —
    remnants of a battle hard fought and barely won.

    With trembling legs you climb back toward the light, a legend forged in the dark.

    *** YOU HAVE CONQUERED THE SCOUNDREL DUNGEON! ***
    """)
    print(f'remaining cards: {room}')
    exit()

def loose():
    print("""
    Your health has been depleted. Darkness closes in.
    Your legs give way and you crumble to the dungeon floor.
    The monsters loom over you as your torch flickers out...

    You have fallen in the depths of the Scoundrel dungeon.

    *** GAME OVER — better luck next time, hero. ***
    """)
    exit()

def flee_or_play():
    choice = None
    while choice is None:
        try:
            #only set choice to answer if correct letter is entered
            choice = input("Do you want to play this room or flee (p/f): ")
            if choice not in ('p','f'):
                print("Invalid choice, try again.")
                choice = None
        except ValueError:
            print(f"Please answer with p or f (play/flee)")
    if choice == 'p':
        pass
    else:
        while room:
            deck.append(room.pop())



#-----------------------GAMING PROCESS--------------------------

#starting the game
print("""
    .------..------..------..------..------..------..------..------..------.
    |S.--. ||C.--. ||O.--. ||U.--. ||N.--. ||D.--. ||R.--. ||E.--. ||L.--. |
    | :/\: || :/\: || :/\: || (\/) || :(): || :/\: || :(): || (\/) || :/\: |
    | :\/: || :\/: || :\/: || :\/: || ()() || (__) || ()() || :\/: || (__) |
    | '--'S|| '--'C|| '--'O|| '--'U|| '--'N|| '--'D|| '--'R|| '--'E|| '--'L|
    `------'`------'`------'`------'`------'`------'`------'`------'`------'
""")
print("""
------------------------------------ INTRO ------------------------------------
Welcome, young hero, to the depths of the Scoundrel dungeon!
You stand at the entrance, torch in hand, heart pounding with courage and dread.
Monsters lurk in every room, weapons lie scattered in the dark, and potions
may restore your weary body — but only if you have the strength to reach them.

------------------------------------ RULES ------------------------------------
- Each room contains 4 cards drawn from the dungeon deck.
- MONSTERS (♣ / ♠): Fight them or flee — but fleeing has a cost.
- WEAPONS (♦): Equip them to fight monsters with less damage.
- POTIONS (♥): Restore health, but only up to your starting 20 HP.
- You can flee a room, but you cannot flee two rooms in a row.
- The game ends when your health reaches 0... or you clear the entire dungeon.

Good luck! You'll need it...
""")

health = 20
print("---------------------------------- GAME START ----------------------------------")
print(f'Your health = {health}')
form_room()
#playing the game
#mail loop runs forever 
#winning / loosing conditions defined in other functions
while True:
    flee_or_play()
    if len(room) == 0:
        form_room()
    else:
        pass
    while len(room) > 1:
        choose_card()
        card_effect()
        print()
        print(f'cards still in room: {room}')
        print()
        if len(weapon) > 0:
            print(f'your weapon: {weapon}')
            print(f'your weapon cap:{weapon_cap}')
        else:
            pass
        
        
    refill_room()
