"""
Name: Dylan Atkinson
Final Project Spring 2025

Idea: Garden

features:
- Grow flowers
- Random Events
    > Weather
    > Animals
- Stats (?)
- min 3 types of flowers
"""

import sys
from random import randint

#############
# CONSTANTS
#############
_BREAK = "=" * 40
_FLOWER_SEEDS = {1001: "🪷", 1002: "🌷", 1003: "🌹", 1004: "🌺"}
_MAIN_MENU = 4
_GARDEN_MENU = 4
_STORE_ITEMS = {1: [10, "pack of seeds"], 2: [25, "scarecrow"], 3: [50, "cool glasses"], 4: [65, "upgraded watering can"]}
_ANIMAL_EVENT = ["Crows destroyed you're whole garden in the middle of the night", "A squirrel trampled some flowers",
                 "No animals visited","Some bees are pollinating your flowers", "Some birds planted some seeds of their own!"]
_WEATHER = {"Cold": -4,"Thunder Storm": -2,"Nice": 0, "Warm": 2, "Raining": 4}
_SEED_MAX = 99

#function to determine if user input is a valid menu selection
def valid_menu(user_text, menu_len):
    while True:
        if user_text.isnumeric():
            if 1 <= int(user_text) <= menu_len:
                output = int(user_text)
                break
            else:
                user_text = input("Not a valid input, please try again:  ")
        else:
            user_text = input("Not a valid input, please try again:  ")

    return output

#print function of main menu
def menu():
    print("1. View Garden")
    print("2. Store")
    print("3. Sleep")
    print("4. Exit")

#print function of garden submenu
def garden_menu():
    print("1. Plant seeds")
    print("2. Water plants")
    print("3. Smell the flowers")
    print("4. Return")

#print function of store menu
def store_menu():
    i = 1
    for items in _STORE_ITEMS.values():
        print(f"{i}. BUY {items[1]} - ${items[0]}")
        i += 1

#function of first checking if user is able to buy item and purchase item if available
def buy(item, cost, spent):
    afford = False
    if cost > spent:
        print("You don't have enough to buy this!")
    else:
        print(f"You bought {item}")
        afford = True
    return afford

#function to check is user already has bought item
def bought(held_item):
    purchased = False
    if held_item:
        purchased = True
        print("You have already bought this item")
    return purchased

#function to plant user selected amount of seeds and randomly select type of flower to plant
def plant_seeds(seedling, soil):
    if seedling > 0:
        for i in range(seedling):
            bloom = randint(1001, 1004)
            soil.append(_FLOWER_SEEDS.get(bloom))
    return soil

#function to set random animal event when user sleeps
def animal_event(luck, scarecrow, garden_list):
    #animal event based on luck
    animals = round(luck/2)
    #if statement used for when user luck is 11 due to glasses item
    if animals == 6:
        animals -= 1
    #animals can't be 0 due to list
    if animals == 0:
        animals += 1
    #scarecrow makes it so you CAN'T have a crows event
    if scarecrow and animals < 5:
        animals += 1

    print(_ANIMAL_EVENT[animals - 1])

    match animals:
        case 1:
            garden_list.clear()
        case 2:
            if len(garden_list) != 0:
                garden_list.pop()
        case 3:
            pass
        case 4:
            if len(garden_list) < 99:
                garden_list.append(_FLOWER_SEEDS[randint(1001,1004)])
        case 5:
            if len(garden_list) < 98:
                garden_list.extend([_FLOWER_SEEDS[randint(1001, 1004)], _FLOWER_SEEDS[randint(1001, 1004)]])
            elif len(garden_list) < 99:
                garden_list.append(_FLOWER_SEEDS[randint(1001, 1004)])

    return garden_list

#function of setting the new daily weather
def daily_weather():
    rand_weather = randint(1,5)
    temp = ""
    match rand_weather:
        case 1:
            temp = "Cold"
        case 2:
            temp = "Thunder Storm"
        case 3:
            temp = "Nice"
        case 4:
            temp = "Warm"
        case 5:
            temp = "Raining"

    return temp

#main function
def main():
    ############
    # VARIABLES
    ############
    garden = []
    seeds = 3
    planted_seeds = 0
    money = 50
    day_luck = randint(1,10)
    water_percent = 15
    weather = "Nice"
    scare_bought = False
    glasses_bought = False
    upgrade_bought = False
    watered = False

    print("Welcome to the Garden")
    # menu loop
    while True:
        print(_BREAK)
        menu()
        select = input("Enter choice: ")

        match valid_menu(select,_MAIN_MENU):
            #Garden Branch
            case 1:
                print(_BREAK)
                # check if garden is empty
                if len(garden) == 0:
                    print("Garden is empty")
                else:
                # print off each flower in garden
                    for i, flowers in enumerate(garden):
                        #if amount of flowers, wrap print onto a new line to keep flowers neat
                        if i%18 == 0 and i != 0:
                            print()
                        print(flowers, end="")
                    print()
                print(f"Your garden is {len(garden) + planted_seeds}/99 filled")

                #Garden submenu
                while True:
                    #print off Garden menu and take user input
                    print(_BREAK)
                    print("What would you like to do in your garden?")
                    garden_menu()
                    garden_input = input("Enter choice: ")


                    #checks if user input is valid and how long the menu is
                    match valid_menu(garden_input, _GARDEN_MENU):
                        #plant seeds and tells user how many seeds they have
                        case 1:
                            if seeds == 0:
                                print(_BREAK)
                                print("You have no seeds left")
                            elif (len(garden) + planted_seeds) == _SEED_MAX:
                                print(_BREAK)
                                print("Your garden is full")
                            else:
                                plant = input(f"You have {seeds} seeds left, how many do you want to plant? ")
                                while True:
                                    if plant.isnumeric():
                                        if int(plant) <= seeds and (int(plant) + len(garden) + planted_seeds) <= _SEED_MAX and int(plant) <= _SEED_MAX:
                                            print(_BREAK)
                                            print(f"you plant {plant} seeds")
                                            planted_seeds = planted_seeds + int(plant)
                                            seeds = seeds - int(plant)
                                            break
                                        elif int(plant) > seeds:
                                            plant = input("You don't have this many seeds, please try again: ")
                                        elif len(garden) == _SEED_MAX:
                                            print("You ran out of space")
                                            break
                                        else:
                                            plant = input("You don't have that many pots left, please try again:")
                                    else:
                                        plant = input("Not a valid input, please try again: ")
                        #water plants, ~15% chance for a new seed to be planted on own
                        case 2:
                            if (len(garden) + planted_seeds) == _SEED_MAX:
                                print(_BREAK)
                                print("No need to water the plants, the garden is full")
                            else:
                                water_plant = randint(1, 100)
                                print(_BREAK)
                                if not watered and weather != "Raining":
                                    print("You fill up your watering can and water the flowers")
                                    if (water_percent + day_luck/2 + int(_WEATHER.get(weather))) > water_plant:
                                        planted_seeds += 1
                                        print("+1 planted seed")
                                    watered = True
                                elif weather == "Raining":
                                    print("It's raining, no need to water the plants today")
                                    if (water_percent + day_luck/2 + int(_WEATHER.get(weather))) > water_plant and (len(garden) + planted_seeds) != _SEED_MAX:
                                        planted_seeds += 1
                                        print("+1 planted seed")
                                else:
                                    print("You already watered your plants today")
                        #smell the flowers, no purpose atm
                        case 3:
                            print(_BREAK)
                            print("You smell the flowers, they smell beautiful")
                        #return back to main menu
                        case 4:
                            break
            #Store Branch
            case 2:
                #Store Submenu
                while True:
                    #print store menu and takes user input, displays user money amount
                    print(_BREAK)
                    print(f"--> STORE <--   Current Money: ${money}")
                    store_menu()
                    #extra print for exiting menu due to how function store_menu works
                    print("5. Exit")

                    store_select = input(f"What would you like to buy: ")

                    #checks if user input is valid and how long menu is (+1 for exit)
                    match valid_menu(store_select, len(_STORE_ITEMS) + 1):
                        #purchase of seed packs, can buy multiple
                        case 1:
                            print(_BREAK)
                            num_packs = input("How many packs do you want to buy: ")
                            while True:
                                try:
                                    int(num_packs)
                                    break
                                except ValueError:
                                    num_packs = input("Invalid input, please try again: ")

                            if buy(_STORE_ITEMS.get(1)[1], _STORE_ITEMS.get(1)[0] * int(num_packs), money):
                                for i in range(int(num_packs)):
                                    seeds += randint(1,3)
                                    money -= _STORE_ITEMS.get(1)[0]
                        #purchase of scarecrow, increases minimum animal event to 2 (+1), only purchasable once
                        case 2:
                            print(_BREAK)
                            if not bought(scare_bought) and buy(_STORE_ITEMS.get(2)[1], _STORE_ITEMS.get(2)[0], money):
                                scare_bought = True
                                money -= _STORE_ITEMS.get(2)[0]
                        #purchase of sunglasses, permanently increases luck by 1, only purchasable once
                        case 3:
                            print(_BREAK)
                            if not bought(glasses_bought) and buy(_STORE_ITEMS.get(3)[1], _STORE_ITEMS.get(3)[0], money):
                                money -= _STORE_ITEMS.get(3)[0]
                                glasses_bought = True
                        #purchase of upgraded watering can, increases chance of watering growing extra flower by 5%, only purchasable once
                        case 4:
                            print(_BREAK)
                            if not bought(upgrade_bought) and buy(_STORE_ITEMS.get(4)[1], _STORE_ITEMS.get(4)[0], money):
                                money -= _STORE_ITEMS.get(4)[0]
                                upgrade_bought = True
                                water_percent += 5
                        case 5:
                        #return to main menu
                            break
            #Sleep cycle and random event handler branch
            case 3:
                print(_BREAK)
                print("You sleep the night away...")

                # weather for the next day
                weather = daily_weather()
                print(f"You check the news for the forecast today: {weather}")

                #generate random amount of money
                payday = randint(15,30) + day_luck
                print(f"You return to your garden after a day of work +${payday}")
                money += payday

                #plant seeds in garden
                plant_seeds(planted_seeds, garden)

                #random animal event
                animal_event(day_luck, scare_bought, garden)

                #generate new daily luck stat and reset variables if needed
                day_luck = randint(1,10)
                if glasses_bought:
                    day_luck += 1
                planted_seeds = 0
                watered = False
            #exit program
            case 4:
                sys.exit()
            #default error value
            case _:
                print(_BREAK)
                print("ERROR, not a valid input")

if __name__ == "__main__":
    main()