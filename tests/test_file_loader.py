from BracketMaker.file_loader import load_from_txt
from BracketMaker.core.bracket import Bracket

def test_file_loader():
    test_file = "data/test_participants.txt"

    store = load_from_txt(test_file)

    participant_names = [participant.name for participant in store.list_participants()]

    assert(len(store.list_participants()) == 14)
    assert("Fire" in participant_names)
    assert("Dope" in participant_names)
    assert("Blood, Sweat, and Tears" in participant_names)
    assert("Save Me" in participant_names)
    assert("Magic Shop" in participant_names)
    assert("Spring Day" in participant_names)
    assert("Crystal Snow" in participant_names)
    assert("Dionysus" in participant_names)
    assert("Agust D" in participant_names)
    assert("Amygdala" in participant_names)
    assert("IDOL" in participant_names)
    assert("Boy with Luv" in participant_names)
    assert("Boy in Luv" in participant_names)
    assert("MIC Drop" in participant_names)
