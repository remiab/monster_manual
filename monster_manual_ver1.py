import json
from turtle import update


def Options():
    print("Welcome to Our Kinda Sorta Monster Manual \n")
    print("(1)  View Manual")
    print("(2)  Add Creature")
    print("(3)  Edit Creature")
    print("(4)  Remove Creature")
    print("(5)  Exit")

def edit_options():
    print("(1) Edit name")
    print("(2) Edit armour class")
    print("(3) Edit hit points")
    print("(4) Edit challenge rating")
    print("(5) Add new category")

def new_stat_options():
    print("(1) Size")
    print("(2) Creature Type")
    print("(3) Add weapon")
    print("(4) Add resistance or vulnerability")
    print("(5) Other")
    
def load_manual(file):
    with open(file, "r") as f:
        dictionary = json.load(f)
        return dictionary

def update_manual(file_name, update):
     with open(file_name, "w") as f:
        json.dump(update, f, indent=4)


def view_manual(manual):
    dictionary = load_manual(manual)
    i = 0
    for entry in dictionary:
            name = entry["name"]
            ac = entry["ac"]
            hp = entry["hp"]
            cr = entry["cr"]
            print(f"Index Number: {i}")
            print(f"{name}")
            print(f"Armour Class: {ac}")
            print(f"Hit Points: {hp}")
            print(f"Challenge Rating: {cr}")
            print("\n")
            i=i+1

def view_monster_list():
    dictionary = load_manual(manual)
    i = 0
    for entry in dictionary:
        name = entry["name"]
        print(f"({i}) {name}")
        i=i+1

def add_creature():
    dictionary = load_manual(manual)
    creature_info = {}
    creature_name = input("Name: ")
    creature_info["name"] = creature_name.strip().capitalize()
    creature_info["ac"] = input("Armour Class: ")
    creature_info["hp"] = input("Hit Points: ")
    creature_info["cr"] = input("Challenge Rating: ")
    creature_size = input("Size: ")
    creature_info["size"] = creature_size.strip().capitalize()
    print("\nSelect creature type:")
    creature_type = ["aberration", "beast", "construct", "humanoid", "monstrosity", "plant", "undead"]
    for i, type in enumerate(creature_type):
        i = i + 1
        print(str(i) + ":" + str(type))
    type_selection = input("Enter number: ")
    type_selection = int(type_selection) -1
    creature_info["type"] = creature_type[type_selection]
    dictionary.append(creature_info)
    update_manual(manual, dictionary)
    print("Creature successfully added to manual")

def further_edit(index_number):
    while True:
        print("""Would you like to make a further edit?
        (1) To the same creature
        (2) To a different creature
        (3) No, exit""")
        further_edit_choice = input("Select an option from above: ")
        if further_edit_choice == "3": 
            break
        elif further_edit_choice == "1":
            edit_creature(index_number)
        elif further_edit_choice == "2":
            select_creature_to_edit()
        else: 
            input("Please choose a number: ")

def add_stat(index_number):
    new_stat_options()
    new_stat_choice = input("Enter Number: ")
    if new_stat_choice == "5":
        dictionary = load_manual(manual)
        new_stat_name = str(input("Enter new stat name: "))
        new_stat_name = new_stat_name.strip()
        new_stat_value = str(input("Enter new stat value: "))
        new_stat_value = new_stat_value.strip()
        dictionary[index_number][new_stat_name] = new_stat_value
        update_manual(manual, dictionary)


def edit_stat(index_number, stat_choice):
     if stat_choice == "1":
                new_name = input("New name: ")
                dictionary = load_manual(manual)
                dictionary[index_number]["name"] = new_name
                update_manual(manual, dictionary)
                further_edit(index_number)
                
     elif stat_choice == "2":
                new_ac = input("New armour class: ")
                dictionary = load_manual(manual)
                dictionary[index_number]["ac"] = new_ac
                update_manual(manual, dictionary)
                further_edit(index_number)
     elif stat_choice == "3":
                new_hp = input("New hit points: ")
                dictionary = load_manual(manual)
                dictionary[index_number]["hp"] = new_hp
                update_manual(manual, dictionary)
                further_edit(index_number)
     elif stat_choice == "4":
                new_cr = input("New challenge rating: ")
                dictionary = load_manual(manual)
                dictionary[index_number]["cr"] = new_cr
                update_manual(manual, dictionary)
                further_edit(index_number)
     elif stat_choice == "5":
         add_stat(index_number)
     else:
         print("Choose an option")

def edit_creature(index_number):
    dictionary = load_manual(manual)
    i=0
    for entry in dictionary:
        if i == index_number:
            name = entry["name"]
            ac = entry["ac"]
            hp = entry["hp"]
            cr = entry["cr"]
            print(f"""Current Stat Block: 
                Name: {name} 
                Armour Class: {ac} 
                Hit Points: {hp}
                Challenge Rating: {cr} 
            \n""")
            edit_options()
            edit_option = input("Select an option: ")
            edit_stat(index_number, edit_option)
            i=i+1

        else:
            pass
            i = i+1

def select_creature_to_edit():
    view_monster_list()
    dictionary = load_manual(manual)
    data_length = len(dictionary)-1
    print("\nWhich creature would you like to edit?")
    creature_option = input(f"Enter Index Number (0-{data_length}): ")
    creature_option = int(creature_option)
    edit_creature(creature_option)

def remove_creature():
    view_monster_list()
    dictionary = load_manual(manual)
    new_data = []
    data_length = len(dictionary)-1
    print("\nWhich creature would you like to remove?")
    delete_option = input(f"Enter index number (0 - {data_length}): ")
    i=0
    for entry in dictionary:
        if i == int(delete_option):
            pass
            i=i+1
        else:
            new_data.append(entry)
            i=i+1
    update_manual(manual, new_data)


manual = "starter-dictionary.json"

while True:
    Options()
    option = input("\nEnter Number: ")
    if option == "1":
        view_manual(manual)
    elif option == "2":
        add_creature()
    elif option == "3":
        select_creature_to_edit()
    elif option == "4":
        remove_creature()
    elif option == "5":
        break
    else:
        input("Please choose an option: ")