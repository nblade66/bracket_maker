""" A file I use to create brackets by modifying the code and hard-coding the import file_name.
    For API or interactive CLI where you can create your own bracket, use web_api.py or cli.py.

    Just upload your participants to "data/participants.txt" and this program will walk you through
    each matchup and allow you to select the winner in the command line.
"""

from BracketMaker.file_loader import load_from_txt
from BracketMaker.core.bracket import Bracket

def main():
    test_file = "data/participants.txt"

    store = load_from_txt(test_file)

    participants = store.list_participants()

    participant_names = [participant.name for participant in participants]

    bracket = Bracket(participants)

    print(bracket)

if __name__ == "__main__":
    main()