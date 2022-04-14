from audioop import add
import json

def start_menu():
    print("Welcome to the Monster Manual\n")
    print("(1) View Creature List")
    print("(2) View Creature")
    print("(3) Add Creature")
    print("(4) Exit")

def new_stat_options():
    print("(1) Action")
    print("(2) Damage Vulnerabilities/Resistances")
    print("(3) Senses")
    print("(4) Special feature")
    print("(5) Other")

def load_manual(file):
    with open(file, "r") as f:
        dictionary = json.load(f)
        return dictionary

def update_manual(file_name, update):
     with open(file_name, "w") as f:
        json.dump(update, f, indent=4)

def view_creature_list():
    dictionary = load_manual(manual)
    names = dictionary.keys()
    i = 1
    for creature in names:
        creature = str(creature).capitalize()
        print(f"{i}: {creature}")
        i=i+1

def retrieve_stat(creature, key):
    key_name = str(key).upper()
    stat_name = creature.get(key)
    stat_name = str(stat_name).capitalize()
    print(f"{key_name}: {stat_name}")

def view_creature():
    dictionary = load_manual(manual)
    creature = input("Enter creature name: ")
    creature = creature.strip().lower()
    if creature in dictionary:
        creature = dictionary.get(creature)
        key_list = creature.keys()
        for key in key_list:
            retrieve_stat(creature, key)
    else:
        print(f"sorry, can't find {creature}")

def add_damage(actions, action, aspect, damage):
    damage_to_add = input(f"Enter {aspect}: ")
    damage_type_to_add = input("Enter damage type: ")
    damage_type_and_value = {damage_to_add: damage_type_to_add}
    damage.append(damage_type_and_value)
    action[aspect] = damage
    additional_damage_type = input("add additional damage type? Y/N")
    additional_damage_type = additional_damage_type.strip().lower()
    if additional_damage_type == "y":
        add_damage(actions, action, aspect, damage)
    else:
        actions.append(action)

def add_weapon_attack(actions, action):
    action_aspects = ["name", "to hit","range/reach(ft)", "damage"]
    for aspect in action_aspects:
        if aspect != "damage":
            action[aspect] = input(f"Enter {aspect}: ")
        else:
            damage = []
            add_damage(actions, action, aspect, damage)

def add_spell_action(actions, action):
    pass

def add_other_action(actions, action):
    action_name = input("Enter action name: ")
    action_description = input("Enter action description: ")
    action[action_name] = action_description
    actions.append(action)

def add_actions(creature, stat, actions):
    dictionary = load_manual(manual)
    dictionary[creature][stat] = {}
    action = {}
    attack_types = ["Melee weapon attack", "Ranged weapon attack", "Melee spell attack", "Ranged spell attack", "N/A"]
    for i, type in enumerate(attack_types):
        i=i+1
        print(f"({i}): {type}")
        i=i+1
    attack_type = input("Enter number: ")
    attack_type = int(attack_type) - 1
    if attack_type < 2:
        action["type"] = attack_types[attack_type]
        add_weapon_attack(actions, action)
    elif attack_type >=2 and attack_type < 4:
        action["type"] = attack_types[attack_type]
        add_spell_action(actions, action)
    else:
        add_other_action(actions, action)  
    dictionary[creature][stat]= actions
    update_manual(manual, dictionary)
    another_action = input("Would you like to add another action? Y/N: ")
    another_action = another_action.strip().lower()
    if another_action == "y":
        add_actions(creature, stat, actions)
    else:
        more_stats_query(creature)

def action_count(creature, stat):
    actions = []
    add_actions(creature, stat, actions)


def add_additional_stat(creature, stat):
    stat_categories = ["actions", "damage v/r", "senses", "special feature", "other"]
    stat_category = stat_categories[stat]
    if stat == 0:
        action_count(creature, stat_category)

def more_stats_query(new_creature_key):
    more_stats = input("Would you like to add more stats to this creature? Y/N: ")
    more_stats = str(more_stats).strip().lower()
    if more_stats == "y":
        new_stat_options()
        stat_choice = input("Enter number to add stat: ")
        stat_choice = int(stat_choice) - 1
        add_additional_stat(new_creature_key, stat_choice)

def add_creature():
    dictionary = load_manual(manual)
    new_creature_name = input("Enter new creature name: ")
    new_creature_key = new_creature_name.strip().lower()
    dictionary[new_creature_key] = {}
    new_creature_name = new_creature_key.capitalize()
    core_stats = ["ac", "hp", "cr", "size", "type"]
    for stat in core_stats:
        dictionary[new_creature_key][stat] = input(f"Enter {stat}: ")
    update_manual(manual, dictionary)
    more_stats_query(new_creature_key)
    


manual = "monsters.json"

while True:
    start_menu()
    option = input("\nEnter Number: ")
    if option == "1":
        view_creature_list()
    elif option == "2":
        view_creature()
    elif option == "3":
        add_creature()
    elif option == "4":
        break
    else:
        option