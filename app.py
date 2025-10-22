from typing import Callable, Dict
import random

# Global Support Functions

def _clear():
    """Lightweight console clear (portable)."""
    print("\n" * 50)

def handle_boot(game_state_dict):
    _clear()
    print("Aladdin and the Evil Genie Lamp")
    print("Press Enter to start...")
    input()
    game_state_dict["state"] = WELCOME_STATE_ID

def handle_welcome(game_state_dict: Dict[str, object]):
    _clear()
    print("Welcome")
    print(
        "Aladdin tried to steal the genie's lamp from Jafar "
        "but a spell trapped him inside."
    )
    input("Press Enter to continue...")
    game_state_dict["state"] = INTRO_STATE_ID

def handle_intro(game_state_dict: Dict[str, object]):
    _clear()
    print("Aladdin is stuck in the lamp. Solve challenges to escape.")
    print(f"You have {game_state_dict['lives']} lives.")
    input("Press Enter to face Level 1...")
    game_state_dict["state"] = LEVEL_1_STATE_ID

def handle_level(game_state_dict, level_fn):
    """Run a level function and apply its result to the controller."""
    result, next_state = level_fn()
    _clear()
    if result:
        print("Success! Moving on...")
        game_state_dict["state"] = next_state
    else:
        game_state_dict["lives"] = int(game_state_dict["lives"]) - 1  # type: ignore[index]
        print(f"Miss! Lives left: {game_state_dict['lives']}")
        if int(game_state_dict["lives"]) <= 0:  # type: ignore[index]
            game_state_dict["state"] = END_STATE_ID
        else:
            # On failure, navigate to provided next state (diagram’s branch)
            game_state_dict["state"] = next_state
    input("Press Enter...")

def handle_end(game_state_dict):
    _clear()
    print("Game over.")
    choice = input("Play again? (y/n): ").strip().lower()
    if choice == "y":
        game_state_dict["lives"] = 3
        game_state_dict["state"] = BOOT_STATE_ID
    else:
        game_state_dict["exit"] = True

def level_1():
    """Math check: decide if division has a remainder.

    - Dividend: random 3-digit number (100..998).
    - Divisor: random 1..99.
    - Ask player if a % b == 0 (no remainder) or there is a remainder.
    - Correct answer -> proceed to Level 2. Wrong -> stay on Level 1.
    """
    a = random.randint(100, 998)
    b = random.randint(1, 99)
    print(f"Level 1: Is {a} divisible by {b}? (no remainder)")

    ans = input("Answer 'y' for divisible, 'n' for remainder: ").strip().lower()
    # if different than 'y' or 'n', ask again and again
    while ans not in ("y", "n"):
        print("Invalid input. Please answer 'y' or 'n'.")
        ans = input("Answer 'y' for divisible, 'n' for remainder: ").strip().lower()
    divisible = (a % b) == 0
    player_says_divisible = ans in ("y", "yes")
    correct = (player_says_divisible == divisible)
    if correct:
        print(f"Correct! {a} % {b} = {a % b}")
        return True, LEVEL_2_STATE_ID
    else:
        print(f"Incorrect. {a} % {b} = {a % b}")
        return False, LEVEL_1_STATE_ID
    
def level_2():

    print("Level 2: Welcome to the game on the second level.")

    choice = input("You see a path ahead. Do you want to (1) Move forward or (2) Rest? ")
        
    # Validate user input
    while not choice.isdigit() or int(choice) not in [1, 2]:
        print("Invalid choice, try again.")
        # global choice
        choice = input("You see a path ahead. Do you want to (1) Move forward or (2) Rest? ")
    
    # Propert the choice to integer for further processing
    if choice.isdigit() and int(choice) in [1, 2]:



        # Option 1: Move forward
        if choice == '1':

            # Function to simulate taking damage
            # fight_enemy()
            print("An enemy appears!")
            dates = 3
            while True:
                print(f"You have {dates} dates left.")
                action = input("Do you want to (3) Slash with a scimitar or (4) Throw a date? (enter 3 or 4): ")
                if action == '3':
                    print("You slash the enemy with your scimitar!")
                    print("Enemy defeated!\n")
                    break
                elif action == '4':
                    if dates <= 0:
                        print("You ran out of dates! Game over.")
                        return False, LEVEL_2_STATE_ID
                        break
                    dates -= 1
                    print("You throw an dates at the enemy!")
                    print("Enemy defeated!\n")
                else:
                    print("Invalid choice, try again.")
            # End of function fight_enemy()

            # Random chance to take damage (simulate enemy attack)
            # 33 % chance of taking damage when enemy will simulate died and then take damage when wakeup when you will not looking
            from random import randint
            if randint(0,2) == 1:
                print("You take damage from the enemy! (when enemy simulates died and then take damage when wakeup when you will not looking)")
                import time
                time.sleep(2)
                game_state_dict["lives"] -= 1
                return False, LEVEL_2_STATE_ID

            print("You moved forward and found a hidden door and finded exit to end of the game.")
            return True, END_STATE_ID



        # Option 2: Rest
        elif choice == '2':
            print("You rest and restore your health to full.")
            # Set in global variable health to 3
            game_state_dict["lives"] = 3
            return True, END_STATE_ID

# Global Variables

# ------------- State identifiers (no enums) -------------
BOOT_STATE_ID = "BOOT_STATE_ID"
WELCOME_STATE_ID = "WELCOME_STATE_ID"
INTRO_STATE_ID = "INTRO_STATE_ID"
LEVEL_1_STATE_ID = "LEVEL_1_STATE_ID"
LEVEL_2_STATE_ID = "LEVEL_2_STATE_ID"
END_STATE_ID = "END_STATE_ID"


game_state_dict = {
    "lives": 3,
    "state": BOOT_STATE_ID,
    "exit": False,  # set to True to break main loop
}

def handler_boot(gs: Dict[str, object]):
    handle_boot(gs)


def handler_welcome(gs: Dict[str, object]):
    handle_welcome(gs)


def handler_intro(gs: Dict[str, object]):
    handle_intro(gs)


def handler_level_1(gs: Dict[str, object]):
    handle_level(gs, level_1)


def handler_level_2(gs: Dict[str, object]):
    handle_level(gs, level_2)

def handler_end(gs: Dict[str, object]):
    handle_end(gs)


def build_handlers(gs: Dict[str, object]):
    """Return a mapping from state id to a handler(gs) function (no lambdas)."""
    return {
        BOOT_STATE_ID: handler_boot,
        WELCOME_STATE_ID: handler_welcome,
        INTRO_STATE_ID: handler_intro,
        LEVEL_1_STATE_ID: handler_level_1,
        LEVEL_2_STATE_ID: handler_level_2,
        END_STATE_ID: handler_end,
    }

def controller_current_state_name(game_state_dict: Dict[str, object]):
    """Return the current state name as a string."""
    return str(game_state_dict.get("state", "UNKNOWN"))

def main():
    
    """Main loop: dispatch handler for the current state until exit."""
    while not game_state_dict.get("exit", False):
        state = game_state_dict["state"]
        handler_map = build_handlers(game_state_dict)
        handler = handler_map[state]
        handler(game_state_dict)


if __name__ == "__main__":
    main()
