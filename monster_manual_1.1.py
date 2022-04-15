from audioop import add
import json

def start_menu():
    print("Welcome to the Monster Manual\n")
    start_options = ["View Creature List", "View Creature", "Add Creature", "Exit"]
    for i, option in enumerate(start_options):
        i=i+1
        print(f"({i}) {option}")
        i=i+1
    chosen_option = input("\nEnter Number: ")
    if chosen_option == "1":
        view_creature_list()
    elif chosen_option == "2":
        view_creature()
    elif chosen_option == "3":
        add_creature()
    elif chosen_option == "4":
        quit()
    else:
        chosen_option

def print_list(list):
    for i, type in enumerate(list):
        i=i+1
        print(f"({i}): {type}")
        i=i+1

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
    additional_damage_type = input("add additional damage type? Y/N: ")
    additional_damage_type = additional_damage_type.strip().lower()
    if additional_damage_type == "y":
        add_damage(actions, action, aspect, damage)
    else:
        weapon_atk_st = input("Does this attack require the target to make a saving throw to avoid further damage/condition? Y/N: ")
        weapon_atk_st = weapon_atk_st.strip().lower()
        if weapon_atk_st == "y":
            saving_throw_skill = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
            print_list(saving_throw_skill)
            entered_skill = input("Enter number: ")
            entered_skill = int(entered_skill) - 1
            entered_skill = saving_throw_skill[entered_skill]
            throw_dc = input("Enter throw DC: ")
            effect_description = input("Enter effect description on failed save: ")
            action["saving throw"] = {entered_skill: throw_dc}
            action["saving throw description"] = effect_description
        else:
            pass
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
    spell_book = {}
    spell_name = input("Enter spell name: ")
    spell_name = spell_name.strip().lower()
    if spell_name in spell_book:
        print(spell_name)
    else:
        action["name"] = spell_name
        action_aspects = ["saving throw or attack roll", "range/reach(ft)", "damage", "description"]
        for aspect in action_aspects:
            if aspect == "saving throw or attack roll":
                st_atk = ["saving throw", "attack roll"]
                print_list(st_atk)
                spell_type = input("Enter number: ")
                spell_type = int(spell_type) - 1
                if spell_type == 0:
                    saving_throw_skill = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
                    print_list(saving_throw_skill)
                    entered_skill = input("Enter number: ")
                    entered_skill = int(entered_skill) - 1
                    entered_skill = saving_throw_skill[entered_skill]
                    throw_dc = input("Enter throw DC: ")
                    damage_reduction_options = ["halved", "no damage"]
                    action["saving throw"] = {entered_skill: throw_dc}
                    print_list(damage_reduction)
                    damage_reduction = input("Enter number: ")
                    damage_reduction = int(damage_reduction) - 1
                    action["damage on successful saving throw"] = damage_reduction_options[damage_reduction]
                elif spell_type == 1:
                    action["to hit"] = input("Enter to hit: ")
                action[aspect] = st_atk[spell_type]
            elif aspect == "range/reach(ft)":
                action[aspect] = input(f"Enter {aspect}: ")
            elif aspect == "description":
                desc_query = input("Add spell description? Y/N: ")
                desc_query = desc_query.strip().lower()
                if desc_query == "y":
                    action[aspect] = input(f"Enter {aspect}: ")
            else:
                damage = []
                add_damage(actions, action, aspect, damage)

def add_other_action(actions, action):
    action_name = input("Enter action name: ")
    action_description = input("Enter action description: ")
    action[action_name] = action_description
    actions.append(action)

def add_actions(creature, stat, actions):
    dictionary = load_manual(manual)
    action = {}
    attack_types = ["Melee weapon attack", "Ranged weapon attack", "Melee spell attack", "Ranged spell attack", "N/A"]
    print_list(attack_types)
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

def add_speeds(creature, stat, speeds, speed):
    dictionary = load_manual(manual)
    speed_types = ["walk", "swim", "fly", "hover", "burrow", "climb"]
    print_list(speed_types)
    chosen_type = input("Enter number: ")
    chosen_type = int(chosen_type) - 1
    chosen_type = speed_types[chosen_type]
    print(chosen_type)
    speed_value = input("Enter speed(ft): ")
    speed[chosen_type] = speed_value
    print(speed)
    add_another_speed = input("Add another speed type? Y/N: ")
    add_another_speed = add_another_speed.strip().lower()
    if add_another_speed == "y":
        add_speeds(creature, stat, speeds, speed)
    else:
        speeds.append(speed)
        print(speeds)
        dictionary[creature][stat] = speeds
        update_manual(manual, dictionary)
        more_stats_query(creature)


def add_additional_stat(creature, stat):
    stat_categories = ["actions", "speed", "stat_block", "damage v/r", "senses", "special feature", "other"]
    stat_category = stat_categories[stat]
    dictionary = load_manual(manual)
    creature_search = dictionary.get(creature)
    key_list = creature_search.keys()
    if stat == 0:
        if stat_category in key_list:
            actions = dictionary[creature][stat_category]
        else:
            actions = []
            dictionary[creature][stat] = {}
        add_actions(creature, stat_category, actions)
    if stat == 1:
        speed = {}
        if stat_category in key_list:
            speeds = dictionary[creature][stat_category]
        else:
            speeds = []
            dictionary[creature][stat_category] = {}
        add_speeds(creature, stat_category, speeds, speed)

def more_stats_query(creature_key):
    more_stats = input("Would you like to add more stats to this creature? Y/N: ")
    more_stats = str(more_stats).strip().lower()
    if more_stats == "y":
        new_stat_options = ["Action", "Speed", "Ability Scores and Modifiers", "Damage Vulnerabilities/Resistances", "Senses", "Special feature", "Other"]
        for i, option in enumerate(new_stat_options):
            i=i+1
            print(f"({i}): {option}")
        stat_choice = input("Enter number: ")
        stat_choice = int(stat_choice) - 1
        add_additional_stat(creature_key, stat_choice)
    else:
        start_menu()

def add_creature():
    dictionary = load_manual(manual)
    new_creature_name = input("Enter new creature name: ")
    new_creature_key = new_creature_name.strip().lower()
    if new_creature_key in dictionary:
        query_overwrite = input(f"{new_creature_key} already in monster manual, would you like to add further stats to it? Y/N: ")
        query_overwrite = query_overwrite.strip().lower()
        if query_overwrite == "y":
            creature_key = new_creature_key
            more_stats_query(creature_key)
        else:
            start_menu()
    else:
        dictionary[new_creature_key] = {}
        new_creature_name = new_creature_key.capitalize()
        dictionary[new_creature_key]["name"] = new_creature_name
        core_stats = ["ac", "hp", "cr", "size", "type"]
        for stat in core_stats:
            dictionary[new_creature_key][stat] = input(f"Enter {stat}: ")
        update_manual(manual, dictionary)
        more_stats_query(new_creature_key)

manual = "monsters.json"
start_menu()