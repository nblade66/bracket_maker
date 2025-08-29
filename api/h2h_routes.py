from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/h2h", tags=["head-to-head"])

# Example data models
class Matchup(BaseModel):
    player1: str
    player2: str

class WinnerSubmission(BaseModel):
    winner: str


# In-memory "state" for now — replace with DB or your bracket logic later
_current_matchup = Matchup(player1="Alice", player2="Bob")
_final_bracket = None


@router.get("/matchup/current", response_model=Matchup)
def read_current_matchup():
    """Return the current head-to-head matchup."""
    return _current_matchup


@router.patch("/matchup/winner")
def update_winner(data: WinnerSubmission):
    """Submit a winner for the current matchup and advance the bracket."""
    global _final_bracket
    # TODO: hook into your real bracket logic
    _final_bracket = {"champion": data.winner}
    return {"message": f"Winner recorded: {data.winner}"}


@router.get("/bracket/final")
def read_final_bracket():
    """Return the final completed bracket (once finished)."""
    if not _final_bracket:
        return {"message": "Bracket not completed yet."}
    return _final_bracket
