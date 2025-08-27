Run with `python -m BracketMaker.cli_h2h`.
I got the bts playlist ("data/complete_bts_discography.csv") from https://open.spotify.com/playlist/3ofZ4VaQrKkgE8KaDKxP1b?si=V1JsibuzS669Gd30ngfv9Q&pi=EnHxvW9yTOuOE&nd=1&dlsi=1a653f0c27944850 (from reddit post https://www.reddit.com/r/bangtan/comments/1l04vet/a_complete_guide_to_bts_discography_from_debut_to/) and exported to a csv file using https://exportify.net/.

TODO:
* User authentication and passwords; this will require a user database linked to BracketStore user_ids
  * Maybe let's try FastAPI to learn it
  * Can I use Auth and FastAPI with my current structure?
* Certain Bracket types will call specific ParticipantStore, while the general Bracket will accept all types of stores. E.g. SongBracket will accept SongParticipantStore, which will only use SongParticipant. Bracket will accept anything that extends ParticipantStore, which will accept anything that extends Participant.
* Feature to reset the bracket to round 1 or reset the round
* Web front end for click selection and nicer UI
* Ability to play a short clip of the song
  * I think Participant should be extended by "Song" and "Song" should be extended by "SpotifySong"
    so that in the future if brackets aren't SongBrackets, they can still work

Features:
* Ranking feature that sorts all the participants based on head-to-head matchups
  * Implement a MergeSort(?) algorithm that compares based on head-to-heads
* Ranking just the top 10 (or 15 or 20) out of all the participants based on
  head-to-head matchups. What is the fastest way to do this when there are many participants?