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
    """Two-variant outcome. Success -> Level 4, Fail -> back to Level 1."""
    print("Level 2: Riddle mock. Type 'open' to succeed.")
    ok = input("); answer: ").strip().lower() == "open"
    return (ok, LEVEL_4_STATE_ID if ok else LEVEL_1_STATE_ID)


def level_3():
    """Two-variant outcome. Success -> Level 5, Fail -> back to Level 1."""
    print("Level 3: Switch mock. Type 'on' to succeed.")
    ok = input("); answer: ").strip().lower() == "on"
    return (ok, LEVEL_5_STATE_ID if ok else LEVEL_1_STATE_ID)


def level_4():
    """One-variant success mock forwarding to Level 6."""
    print("Level 4: Simple step forward. Auto-success.")
    return True, LEVEL_6_STATE_ID


def level_5():
    """One-variant success mock forwarding to Level 6."""
    print("Level 5: Simple step forward. Auto-success.")
    return True, LEVEL_6_STATE_ID


def level_6():
    """Final gate. Success ends with win, fail reduces life and loops here."""
    print("Level 6: Final wish. Type 'wish' to win.")
    ok = input("); answer: ").strip().lower() == "wish"
    return (ok, END_STATE_ID if ok else LEVEL_6_STATE_ID)

# Global Variables

# ------------- State identifiers (no enums) -------------
BOOT_STATE_ID = "BOOT_STATE_ID"
WELCOME_STATE_ID = "WELCOME_STATE_ID"
INTRO_STATE_ID = "INTRO_STATE_ID"
LEVEL_1_STATE_ID = "LEVEL_1_STATE_ID"
LEVEL_2_STATE_ID = "LEVEL_2_STATE_ID"
LEVEL_3_STATE_ID = "LEVEL_3_STATE_ID"
LEVEL_4_STATE_ID = "LEVEL_4_STATE_ID"
LEVEL_5_STATE_ID = "LEVEL_5_STATE_ID"
LEVEL_6_STATE_ID = "LEVEL_6_STATE_ID"
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


def handler_level_3(gs: Dict[str, object]):
    handle_level(gs, level_3)


def handler_level_4(gs: Dict[str, object]):
    handle_level(gs, level_4)


def handler_level_5(gs: Dict[str, object]):
    handle_level(gs, level_5)


def handler_level_6(gs: Dict[str, object]):
    handle_level(gs, level_6)


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
        LEVEL_3_STATE_ID: handler_level_3,
        LEVEL_4_STATE_ID: handler_level_4,
        LEVEL_5_STATE_ID: handler_level_5,
        LEVEL_6_STATE_ID: handler_level_6,
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
