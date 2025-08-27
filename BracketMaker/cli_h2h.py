""" A file I use to create brackets by modifying the code and hard-coding the import file_name.
    For API or interactive CLI where you can create your own bracket, use web_api.py or cli.py.

    Just upload your participants to "data/participants.txt" and this program will walk you through
    each matchup and allow you to select the winner in the command line.
"""

from BracketMaker.file_loader import FileLoader
from BracketMaker.bracket.bracket import Bracket
from BracketMaker.participant.store.sqlite_participant_store import SQLiteParticipantStore
from BracketMaker.bracket.bracket_manager import BracketManager

def prompt_user_id():
    return input("Enter your user ID: ").strip()

def prompt_main_menu():
    print("1) Create new bracket\n2) Load existing bracket")
    return input("Choose an option (1 or 2): ").strip()

def prompt_bracket_selection(bracket_tuples):
    print("Available brackets:")
    for idx, (bracket_id, bracket) in enumerate(bracket_tuples, start=1):
        bracket_name = getattr(bracket, 'name', '[no name]')
        print(f"{idx}) ID: {bracket_id} | Name: {bracket_name}")
    sel = input("Enter the number of the bracket to load: ").strip()
    try:
        sel_idx = int(sel) - 1
        if sel_idx < 0 or sel_idx >= len(bracket_tuples):
            print("Invalid selection.")
            return None
        return bracket_tuples[sel_idx][0]  # Return the bracket_id
    except Exception:
        print("Invalid input.")
        return None

def prompt_bracket_name():
    return input("Enter a name for your new bracket: ").strip()

def main():
    user_id = prompt_user_id()
    bracket_manager = BracketManager(user_id=user_id)
    choice = prompt_main_menu()

    if choice == "1":
        track_file = "data/imports/complete_bts_discography.csv"
        store = SQLiteParticipantStore()
        loader = FileLoader(store)
        loader.load(track_file)
        bracket_name = prompt_bracket_name()
        bracket = Bracket(bracket_name, store)
        bracket_id = bracket_manager.add_bracket(bracket)
        print(f"Created new bracket with ID: {bracket_id}")
    elif choice == "2":
        bracket_tuples = bracket_manager.list_brackets_with_ids()
        if not bracket_tuples:
            print("No brackets found for this user.")
            return
        bracket_id = prompt_bracket_selection(bracket_tuples)
        if not bracket_id:
            return
        bracket = bracket_manager.get_bracket(bracket_id)
        if bracket is None:
            print("Bracket not found.")
            return
    else:
        print("Invalid choice.")
        return

    print(bracket)
    head_to_head(bracket)

def head_to_head(bracket: Bracket):
    print("Starting head-to-head matchup selection...")
    print("Type 'exit' at any prompt to quit and save your progress.\n")

    # Iterate over rounds and matchups in order
    for round_num, rnd in enumerate(bracket.rounds, start=1):
        print(f"\nRound {round_num}:")
        for matchup in rnd:
            # If matchup already decided, skip
            if matchup.is_decided():
                continue

            p1_name = matchup.participant1.name
            p2_name = matchup.participant2.name

            print(f"Matchup: 1) {p1_name}  vs  2) {p2_name}")
            while True:
                choice = input("Enter winner (1 or 2, or 'exit' to quit): ").strip()
                if choice.lower() == "exit":
                    print("Exiting head-to-head. Progress saved.")
                    return
                if choice == "1":
                    winner = matchup.participant1
                    break
                elif choice == "2":
                    winner = matchup.participant2
                    break
                else:
                    print("Invalid choice. Please enter 1, 2, or 'exit'.")

            matchup.set_winner(winner)
            print(f"Winner set to {winner.name}")

    if bracket.is_complete():
        print(f"\nTournament complete! Winner: {bracket.get_winner().name}")
    else:
        print("\nTournament not complete yet. Some matchups remain undecided.")


if __name__ == "__main__":
    main()