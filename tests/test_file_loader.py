from BracketMaker.file_loader import FileLoader
from BracketMaker.participant.store.in_memory_participant_store import InMemoryParticipantStore

def test_load_from_txt():
    test_file = "data/test_participants.txt"

    store = InMemoryParticipantStore()

    loader = FileLoader(store)

    loader.load_from_txt(test_file)

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

def test_load_from_csv():
    """ This tests loading from a csv file from a playlist that was exported from Spotify """
    test_file = "data/test_bts_spotify_export.csv"

    store = InMemoryParticipantStore()

    loader = FileLoader(store)

    loader.load_from_csv(test_file)

    participant_names = [participant.name for participant in store.list_participants()]

    assert(len(store.list_participants()) == 8)
    assert("Burning Up (Fire)" in participant_names)
    assert("Dionysus" in participant_names)
    assert("ProMeTheUs" in participant_names)
    assert("Agust D" in participant_names)
    assert("Give It to Me" in participant_names)
    assert("IDOL" in participant_names)
    assert("Dope" in participant_names)
    assert("Tony Montana" in participant_names)
