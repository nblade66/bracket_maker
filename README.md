Run with `python -m BracketMaker.cli_h2h`.
I got the bts playlist ("data/complete_bts_discography.csv") from https://open.spotify.com/playlist/3ofZ4VaQrKkgE8KaDKxP1b?si=V1JsibuzS669Gd30ngfv9Q&pi=EnHxvW9yTOuOE&nd=1&dlsi=1a653f0c27944850 (from reddit post https://www.reddit.com/r/bangtan/comments/1l04vet/a_complete_guide_to_bts_discography_from_debut_to/) and exported to a csv file using https://exportify.net/.

TODO:
* Should BracketManager handle both BracketStore and ParticipantStore? BracketStore and ParticipantStore tend to be pretty tightly coupled, considering Brackets rely on the ParticipantStore. How can we keep them together? Not all databases will be sqlite databases in the future, right? They might not be a file-based database. How can we keep the database style we use de-coupled from the functionality? And how can we make sure that when we load in a Bracket from BracketStore, the corresponding ParticipantStore is also loaded?
  * I feel like BracketStore and ParticipantStore should be combined into a single database. But this would lock me into using Sqlite or SQL. Is there some way to create a DatabaseManager that will synchronize the two? Then if I do want to combine them into a single database, I can just implement a single database and the ParticipantStore and BracketStore can still be separate. They will just both call the same database.
* Certain Bracket types will call specific ParticipantStore, while the general Bracket will accept all types of stores. E.g. SongBracket will accept SongParticipantStore, which will only use SongParticipant. Bracket will accept anything that extends ParticipantStore, which will accept anything that extends Participant.
* I need a BracketManager class that will create Brackets, assign them IDs, etc.
* Bracket needs to use the store, not its own participant list
* Feature to save the bracket and come back to it later
* Feature to reset the bracket to round 1 or reset the round
* Front end for click selection and nicer UI
* Ability to play a short clip of the song
  * I think Participant should be extended by "Song" and "Song" should be extended by "SpotifySong"
    so that in the future if brackets aren't SongBrackets, they can still work

Features:
* Ranking feature that sorts all the participants based on head-to-head matchups
  * Implement a MergeSort(?) algorithm that compares based on head-to-heads
* Ranking just the top 10 (or 15 or 20) out of all the participants based on
  head-to-head matchups. What is the fastest way to do this when there are many participants?