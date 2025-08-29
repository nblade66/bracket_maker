""" A file I use to create brackets by modifying the code and hard-coding the import file_name.
    For API or interactive CLI where you can create your own bracket, use web_api.py or cli.py.

    Just upload your participants to "data/participants.txt" and this program will walk you through
    each matchup and allow you to select the winner in the command line.
"""

from BracketMaker.file_loader import FileLoader
from BracketMaker.bracket.bracket import Bracket
from BracketMaker.participant.store.sqlite_participant_store import SQLiteParticipantStore
from BracketMaker.bracket.bracket_manager import BracketManager
from BracketMaker.logic.h2h import H2H

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
    h2h = H2H(bracket)

    while True:
        matchup = h2h.get_current_matchup()
        if matchup is None:
            break  # Tournament done!

        p1, p2 = matchup.participant1, matchup.participant2
        print(f"\nMatchup: 1) {p1.name}  vs  2) {p2.name}")

        choice = input("Enter winner (1 or 2, or 'exit' to quit): ").strip()
        if choice.lower() == "exit":
            print("Exiting head-to-head. Progress saved.")
            return
        elif choice == "1":
            h2h.set_winner(matchup, p1)
        elif choice == "2":
            h2h.set_winner(matchup, p2)
        else:
            print("Invalid choice.")
            continue

        print(f"Winner set to {matchup.winner.name}")

    print(f"\nTournament complete! Winner: {bracket.get_winner().name}")



if __name__ == "__main__":
    main()