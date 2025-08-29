Run with `python -m BracketMaker.cli_h2h`.

Start the FastAPI Back End by running `fastapi dev api/main.py`

I got the bts playlist ("data/complete_bts_discography.csv") from https://open.spotify.com/playlist/3ofZ4VaQrKkgE8KaDKxP1b?si=V1JsibuzS669Gd30ngfv9Q&pi=EnHxvW9yTOuOE&nd=1&dlsi=1a653f0c27944850 (from reddit post https://www.reddit.com/r/bangtan/comments/1l04vet/a_complete_guide_to_bts_discography_from_debut_to/) and exported to a csv file using https://exportify.net/.

TODO:
* Manually created brackets:
  * Currently, all brackets are auto-generated based on a list of participants. Users may want to create a manual bracket.
  * I think Matchup having an ID that I can refer to them by would be easier than using a Matchup Index for add_participant. This would make coding the manual addition of participants easier.
  * Perhaps there should be an add_participant_1 and add_participant_2 function instead of just add_participant. When manually adding participants, the participant's spot should be known already.
* User authentication and passwords; this will require a user database linked to BracketStore user_ids
  * Maybe let's try FastAPI to learn it
  * Can I use Auth and FastAPI with my current structure?

* Song Class Implementations:
  * Certain Bracket types will call specific ParticipantStore, while the general Bracket will accept all types of stores. E.g. SongBracket will accept SongParticipantStore, which will only use SongParticipant. Bracket will accept anything that extends ParticipantStore, which will accept anything that extends Participant.
    * Will need to modify FileLoader::load_from_csv to be more Spotify specific with naming and documentation, since currently load_from_csv is for Spotify csv files.
  * Ability to play a short clip of the song
    * I think Participant should be extended by "Song" and "Song" should be extended by "SpotifySong"
    so that in the future if brackets aren't SongBrackets, they can still work

Wishlist:
* Ranking feature that sorts all the participants based on head-to-head matchups
  * Implement a MergeSort(?) algorithm that compares based on head-to-heads
* Ranking just the top 10 (or 15 or 20) out of all the participants based on
  head-to-head matchups. What is the fastest way to do this when there are many participants?
* Feature to reset the bracket to round 1 or reset the round
* Web front end for click selection and nicer UI
* Create ParticipantStore manually, not from an imported file
* Is there a way to construct a "tier list" using a tournament style bracket? Basically, if there are songs/participants that are too hard to decide between, they are placed in the same tier
* Feature to send two participants forward into the next round and re-shuffle only that round; I think this could help generate a tier list
  * By extension, feature to hold both participants back from the round because they both don't deserve to advance