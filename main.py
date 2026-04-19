
"""
    .------..------..------..------..------..------..------..------..------.
    |S.--. ||C.--. ||O.--. ||U.--. ||N.--. ||D.--. ||R.--. ||E.--. ||L.--. |
    | :/\: || :/\: || :/\: || (\/) || :(): || :/\: || :(): || (\/) || :/\: |
    | :\/: || :\/: || :\/: || :\/: || ()() || (__) || ()() || :\/: || (__) |
    | '--'S|| '--'C|| '--'O|| '--'U|| '--'N|| '--'D|| '--'R|| '--'E|| '--'L|
    `------'`------'`------'`------'`------'`------'`------'`------'`------'
"""

#-------------------IMPORTS--------------------------

import pygame
from itertools import product
import random
import sys
import os

if getattr(sys, 'frozen', False):
    BASE_PATH = sys._MEIPASS
else:
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE_PATH, 'assets')

#-------------------GAME SETUP--------------------------

#setting up pygame
pygame.init()
screen = pygame.display.set_mode((1280, 900))
clock = pygame.time.Clock()
#setting up music in pygame
pygame.mixer.init()
pygame.mixer.music.load(os.path.join(ASSETS, 'music.ogg'))
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

#setting up the full screens
start_screen = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS, 'start_screen.png')), (1280, 900))
lose_screen = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS, 'you_lose.png')), (1280, 900))
win_screen = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS, 'you_win.png')), (1280, 900))
background = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS, 'background.png')), (1280, 900))

#setting up fonts
font = pygame.font.Font(os.path.join(ASSETS, 'DungeonFont.ttf'), 36)
font_small = pygame.font.Font(os.path.join(ASSETS, 'DungeonFont.ttf'), 18)
font_big = pygame.font.Font(os.path.join(ASSETS, 'DungeonFont.ttf'), 28)

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

# Setting ranks to values, suits symbols to suits,
# assigning cards to images
dict_rank_to_value = {'2':2, '3':3, '4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':11,'Q':12,'K':13,'A':14}

suit_symbols_to_strings = {
    '♠': 'spades',
    '♣': 'clubs',
    '♥': 'hearts', 
    '♦': 'diamonds'
}

card_images = {}
for card in deck:
    card_path = os.path.join(ASSETS, f'cards/{card[0]}_{suit_symbols_to_strings[card[1]]}.png')
    card_images[card] = pygame.image.load(card_path)
 
#setting start state
health = 20
rooms_to_play = 14
room = []
weapon = []
weapon_cap = float('inf')
music_on = True

#-----------------------MECHANICS--------------------------

def form_room():
    global deck, room
    room = []
    for i in range(4):
        room.append(deck.pop(0))
    # ----- print statements will not work, must be rendered -----
    #print()
    #print("As you enter the dungeon, you look around. This is what you see:")
    #print()
    #print(room)


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

def refill_room():
    global deck, room, game_phase, rooms_to_play
    #1 Karte bleibt immer übrig
    if len(deck) == 1:
        room.append(deck.pop(0))
        game_phase = 'win'
    else:  
        for i in range(3):
            room.append(deck.pop(0))
        rooms_to_play -= 1
        game_phase = 'flee_or_play'
    

def card_effect(card, use_weapon=False):
    global health, weapon, weapon_cap, game_phase
    if card[1] in black_suits:    
        
        #if you use a weapon
        if use_weapon == True:
            #if player chooses to use weapon: subtract weapon strength from hit
            blocked_hit = dict_rank_to_value.get(card[0]) - dict_rank_to_value.get(weapon[0])
            #cant gain health from hits, min cap at 0
            if blocked_hit < 0:
                blocked_hit = 0
            health = health - blocked_hit
            weapon_cap = dict_rank_to_value.get(card[0]) - 1
            if weapon_cap == 1:
                weapon = []
        #if you dont use a weapon
        else:
            damage = dict_rank_to_value.get(card[0])
            health = health - damage
        if health <= 0:
            game_phase = 'lose_screen'
        else:
            game_phase = 'playing'

    elif card[1] == '♦':
        weapon = card
        weapon_cap = float('inf')
        game_phase = 'playing'

    elif card[1] == '♥':
        health = health + dict_rank_to_value.get(card[0])
        #max health cap at 20
        if health > 20:
            health = 20
        game_phase = 'playing'


#-------SETUP------------

form_room()
game_phase = 'start_screen'

#-------STARTING PYGAME MAIN LOOP------------

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        #-------EVENT BLOCK------------
        if game_phase != 'lose_screen':
            if event.type == pygame.MOUSEBUTTONDOWN:
                #setting the music to toggle
                if music_on == True:
                    if music_toggle_rect.collidepoint(event.pos):
                        pygame.mixer.music.pause()
                        music_on = False
                else:
                    if music_toggle_rect.collidepoint(event.pos):
                        pygame.mixer.music.unpause()
                        music_on = True

                #-------GAME PHASE LOGIC------------
                #independent of phase rules button
                if rules_rect.collidepoint(event.pos):
                        game_phase = 'rules_screen'
                
                #start screen
                if game_phase == 'start_screen':
                    if play_start_rect.collidepoint(event.pos):
                        game_phase = 'flee_or_play'
                    
                    elif rules_rect_start.collidepoint(event.pos):
                        game_phase = 'rules_screen'
                    
                #rules screen
                elif game_phase == 'rules_screen':
                    if play_button.collidepoint(event.pos):
                        game_phase = 'flee_or_play'

                #play or flee phase
                elif game_phase == 'flee_or_play':
                    if play_button.collidepoint(event.pos):
                        game_phase = 'playing'
                    elif flee_button.collidepoint(event.pos):
                        while room:
                            deck.append(room.pop())
                        form_room()
                        game_phase = 'playing'
                #playing phase
                elif game_phase == 'playing':
                    #click on card detection
                    card_rects_room = (card_1_rect, card_2_rect, card_3_rect, card_4_rect)
                    for i, card_rects in enumerate (card_rects_room):
                        if card_rects.collidepoint(event.pos):
                            #set the played card
                            played_card = room[i]
                            #pop played card from room
                            room.pop(i)
                            if played_card[1] in black_suits and len(weapon) > 0 and weapon_cap >= dict_rank_to_value.get(played_card[0]):
                                game_phase = 'weapon_or_barehand'
                            else:card_effect(played_card)
                            #refill room if 1 card
                            if len(room) == 1 and game_phase != 'weapon_or_barehand'and game_phase != 'lose_screen':
                                refill_room()
                
                #decision: use weapon?
                elif game_phase == 'weapon_or_barehand':
                    #player must choose to use weapon or not
                    if use_weapon_button.collidepoint(event.pos):
                        card_effect(played_card, True)
                    elif barehand_button.collidepoint(event.pos):
                        card_effect(played_card)
                    if len(room) == 1 and game_phase != 'lose_screen':
                        refill_room()
           
                        

    #-------RENDERING BLOCK------------

    #rendering the background first
    screen.blit(background, (0, 0))

    #rendering the deck
    image_deck = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS, 'cards/back_side.png')), (200, 280))
    screen.blit(image_deck, (60, 260))

    #rendering the rules button
    rules_rect = pygame.Rect(80, 120, 150, 80)
    rules_button_image = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS, 'stone.png')), (150, 80))
    text_rules = font.render("RULES", True, (255, 255, 255))
    text_rules_rect = text_rules.get_rect(center = (155, 160))
    screen.blit(rules_button_image, (80,120))
    screen.blit(text_rules, text_rules_rect)

    #rendering the room
    if len(room)>= 1:
        card_1_rect = pygame.Rect(300, 260, 200, 280)
        card_1_image = pygame.transform.scale(card_images[room[0]],(200, 280))
        screen.blit(card_1_image, card_1_rect)

    if len(room)>= 2:
        card_2_rect = pygame.Rect(510, 260, 200, 280)
        card_2_image = pygame.transform.scale(card_images[room[1]],(200, 280))
        screen.blit(card_2_image, card_2_rect)

    if len(room)>= 3:
        card_3_rect = pygame.Rect(720, 260, 200, 280)
        card_3_image = pygame.transform.scale(card_images[room[2]],(200, 280))
        screen.blit(card_3_image, card_3_rect)

    if len(room)>= 4:
        card_4_rect = pygame.Rect(930, 260, 200, 280)
        card_4_image = pygame.transform.scale(card_images[room[3]],(200, 280))
        screen.blit(card_4_image, card_4_rect)
    
    #rendering the weapon
    if len(weapon) == 2:
        weapon_rect = pygame.Rect(60, 550, 100, 140)
        weapon_image = pygame.transform.scale(card_images[weapon],(200, 280))
        screen.blit(weapon_image, weapon_rect)

    #render phase specifics
    if game_phase == 'flee_or_play':
        #render question p/f?
        p_f_text_bg_image = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS, 'stone.png')), (800, 50))
        text_f_or_p = font.render("Do you want to play this room or flee?", True, (0, 0, 0))
        text_f_or_p_rect = text_f_or_p.get_rect(center = (715, 95))
        screen.blit(p_f_text_bg_image, (315, 70))
        screen.blit(text_f_or_p, text_f_or_p_rect)
        #render play button
        play_button = pygame.Rect(325, 150, 150, 80)
        play_button_bg_image = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS, 'stone.png')), (150, 80))
        text_play = font.render("PLAY", True, (0, 0, 0))
        text_play_rect = text_play.get_rect(center = (400, 190))
        screen.blit(play_button_bg_image, (325, 150))
        screen.blit(text_play, text_play_rect)

        #render flee button
        flee_button = pygame.Rect(955, 150, 150, 80)
        flee_button_bg_image = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS, 'stone.png')), (150, 80))
        text_flee = font.render("FLEE", True, (0, 0, 0))
        text_flee_rect = text_flee.get_rect(center = (1025, 190))
        screen.blit(flee_button_bg_image, (950, 150))
        screen.blit(text_flee, text_flee_rect)

    if game_phase == 'weapon_or_barehand':
        #render question w/b?
        w_b_text_bg_image = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS, 'stone.png')), (900, 50))
        text_w_or_b = font.render("Do you want to use your weapon or fight barehanded?", True, (0, 0, 0))
        text_w_or_b_rect = text_w_or_b.get_rect(center = (715, 95))
        screen.blit(w_b_text_bg_image, (265, 70))
        screen.blit(text_w_or_b, text_w_or_b_rect)
        #render play button
        use_weapon_button = pygame.Rect(250, 150, 300, 80)
        use_weapon_button_bg_image = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS, 'stone.png')), (300, 80))
        text_play = font.render("USE WEAPON", True, (0, 0, 0))
        text_play_rect = text_play.get_rect(center = (400, 190))
        screen.blit(use_weapon_button_bg_image, (250,150))
        screen.blit(text_play, text_play_rect)
        #render flee button
        barehand_button = pygame.Rect(900, 150, 300, 80)
        barehand_button_image = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS, 'stone.png')), (300, 80))
        text_flee = font.render("BAREHAND", True, (0, 0, 0))
        text_flee_rect = text_flee.get_rect(center = (1050, 190))
        screen.blit(barehand_button_image, (900, 150))
        screen.blit(text_flee, text_flee_rect)

    #render text (health, weapon cap, room count)
    text_health = font.render(f'HP: {health}', True, (255, 255, 255))
    screen.blit(text_health, (400, 20))
    if weapon_cap == float('inf'):
        text_weapon_cap = font.render(f'Weapon Cap: -', True, (255, 255, 255))
    elif weapon_cap in (2,3,4,5,6,7,8,9,10):
        text_weapon_cap = font.render(f'Weapon Cap: {weapon_cap}', True, (255, 255, 255))
    elif weapon_cap == 11:
        text_weapon_cap = font.render(f'Weapon Cap: J', True, (255, 255, 255))
    elif weapon_cap == 12:
        text_weapon_cap = font.render(f'Weapon Cap: Q', True, (255, 255, 255))
    elif weapon_cap == 13:
        text_weapon_cap = font.render(f'Weapon Cap: K', True, (255, 255, 255))
    screen.blit(text_weapon_cap, (850, 20))
    text_room_count = font.render(f'Rooms to Win: {rooms_to_play}', True, (255, 255, 255))
    screen.blit(text_room_count, (550,20))
    


     #rendering game phase screens over everything else (start, loose, win, rules)
    if game_phase == 'start_screen':
        screen.blit(start_screen, (0, 0))
        play_start_rect = pygame.Rect(530, 450, 220, 115)
        text_play_start = font.render("PLAY", True, (0, 0, 0))
        text_play_start_rect = text_play_start.get_rect(center = (640, 507))
        screen.blit(text_play_start, text_play_start_rect)
        rules_rect_start = pygame.Rect(530, 633, 220, 115)
        text_rules_start = font.render("RULES", True, (0, 0, 0))
        text_rules_start_rect = text_rules.get_rect(center = (640, 690))
        screen.blit(text_rules_start, text_rules_start_rect)
    
    if game_phase == 'rules_screen':
        screen.fill((0, 0, 0))
        book = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS, 'book.png')), (800, 900))
        screen.blit(book,(245,0))
        rules_lines = [
            "--------------------------------------- INTRO ---------------------------------------",
            "Welcome, young hero, to the depths of the Scoundrel dungeon! Monsters lurk in every room,",
            "weapons lie scattered in the dark, and potions may restore your body - but only if you have the strength to reach",
            "them.",
            "",
            "--------------------------------------- RULES ---------------------------------------",
            "Scoundrel is played with a modified 52-card deck of standard playing cards. Red face cards (J, Q, K, A of hearts",
            "and diamonds) are removed, leaving a deck of 44 cards. You start with a health of 20 HP.",
            "",
            "At the beginning of each round, 4 cards are dealt, representing a room. After the cards are dealt you can choose",
            "to either face the room in front of you (press play button) or flee (flee button). If you flee, the cards in the",
            "room go back to the bottom of the deck, and 4 new cards are dealt. You cannot flee two rooms in a row.",
            "",
            "To play a card in a room simply click on the card you want to play. The cards effect gets applied immediately.",
            "Effects depend on the cards suit and rank. Rank = card number (2-10) or face value (J=11, Q=12, K=13, A=14).",
            "",
            "- Clubs & Spades: Represent monsters, and deal damage equal to their rank (e.g. King of Clubs = - 13 HP).",
            "You can use a weapon to reduce damage (see below).",
            "",
            "- Hearts: Represent potions. Heal equal to their rank value, up to a max of 20 HP. (e.g. 9 of Hearts= + 9 HP)",
            "",
            "- Diamonds: Represent weapons. Play a weapon to equip it. When you have a weapon equiped and you are facing",
            "a monster you can choose to either use your weapon or fight barehanded. If you choose to use your weapon",
            "the damage gets reduced: Damage = monster rank - weapon rank. After you use your weapon, your weapon cap will",
            "reduce to one rank lower than the last monsters rank you fought using the waepon (e.g. 10 of Diamonds vs",
            "King of Spades = 13-10 = 3 damage and the weapons cap becomes Q (12). This weapon can from thereon only be", 
            "used against monsters of rank Q or lower). You can only carry one weapon at a time. If you play a Diamond",
            "card while already equipted with a weapon you will drop the old weapon and equipt the new one. A new weapon",
            "always starts with an infinite cap.",
            "",
            "A round ends after 3 of 4 cards of a room are played. The remaining card carries over and 3 new",
            "cards are dealt. If your HP hits 0 you die and it is game over! If you finish the last room and there are not",
            "enough cards left in the deck to fill up the room, you win!",
        ]
        for i, line in enumerate(rules_lines):
            text_surface = font_small.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(centerx=640)
            screen.blit(text_surface, (text_rect.x, 20 + i * 21))
            play_button = pygame.Rect(570, 730, 150, 80)
            play_button_bg_image = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS, 'stone.png')), (150, 80))
            text_play = font.render("PLAY", True, (0, 0, 0))
            text_play_rect = text_play.get_rect(center = (645, 770))
            screen.blit(play_button_bg_image, (570, 730))
            screen.blit(text_play, text_play_rect)
        
    if game_phase == 'lose_screen':
            screen.blit(lose_screen, (0, 0))
    if game_phase == 'win':
            screen.blit(win_screen, (0, 0))
        
    #render music toggle
    music_toggle_rect = pygame.Rect(1190,15,50,50)
    if music_on == True:
        music_toggle_image = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS, 'vol_on.png')), (30, 30))
    if music_on == False:
        music_toggle_image = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS, 'vol_off.png')), (30, 30))
    screen.blit(music_toggle_image, (1200, 25))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

"""


Future Feature Dev notes:
1. As of now flee adds cards to room in opposite order. Leave or change? Might create interesting new rooms.

"""

""" Unused print statements from CLI version:
print(f"You strike with your weapon, blocking some of the blow. You take {blocked_hit} damage. Health: {health}")
print(f"You fight bare handed and take {dict_rank_to_value.get(played_card[0])} damage. Health: {health}")
print("
    Your health has been depleted. Darkness closes in.
    Your legs give way and you crumble to the dungeon floor.
    The monsters loom over you as your torch flickers out...

    You have fallen in the depths of the Scoundrel dungeon.

    *** GAME OVER - better luck next time, hero. ***
    ")


print(f"You drop your old weapon and pick up a new one with a strength of {card[0]}.")


print(f"You pick up a weapon with a strength of {card[0]} and equip it. You feel stronger.")

print(f"You look around and find a healing elixir. You drink it and feel your wounds close. Health: {health}.")

print("
You clear the final room and look around - silence at last.
You look around at the scattered cards, the broken weapons, the empty potion vials -
remnants of a battle hard fought and barely won.

With trembling legs you climb back toward the light, a legend forged in the dark.

*** YOU HAVE CONQUERED THE SCOUNDREL DUNGEON! ***
")
print(f'remaining cards: {room}')

print(f"Your weapon is too weak for this foe - you fight bare handed and take {damage} damage. Health: {health}")

print(f"You fight bare handed and take {damage} damage. Health: {health}")

"""
