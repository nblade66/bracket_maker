""" A file I use to create brackets by modifying the code and hard-coding the import file_name.
    For API or interactive CLI where you can create your own bracket, use web_api.py or cli.py.

    Just upload your participants to "data/participants.txt" and this program will walk you through
    each matchup and allow you to select the winner in the command line.
"""

from BracketMaker.file_loader import FileLoader
from BracketMaker.bracket.bracket import Bracket
from BracketMaker.participant.store.sqlite_participant_store import SQLiteParticipantStore
from BracketMaker.bracket.bracket_manager import BracketManager

def main():
    """ Add BracketStore to this, so that brackets can be saved and resumed """

    bracket_manager = BracketManager()

    track_file = "data/complete_bts_discography.csv"

    store = SQLiteParticipantStore()    # TODO Create a unique Store file name: cli_h2h_date_time.db

    loader = FileLoader(store)

    loader.load(track_file)

    bracket = Bracket(store)

    print(bracket)

    head_to_head(bracket)

def load_bracket(bracket_id: str):
    # TODO: load the bracket from the bracket store
    pass

def head_to_head(bracket: Bracket):
    print("Starting head-to-head matchup selection...")

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
                choice = input("Enter winner (1 or 2): ").strip()
                if choice == "1":
                    winner = matchup.participant1
                    break
                elif choice == "2":
                    winner = matchup.participant2
                    break
                else:
                    print("Invalid choice. Please enter 1 or 2.")

            matchup.set_winner(winner)
            print(f"Winner set to {winner.name}")

    if bracket.is_complete():
        print(f"\nTournament complete! Winner: {bracket.get_winner().name}")
    else:
        print("\nTournament not complete yet. Some matchups remain undecided.")


if __name__ == "__main__":
    main()