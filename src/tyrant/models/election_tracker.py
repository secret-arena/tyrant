from dataclasses import dataclass
from typing import Final

FAILURES_UNTIL_TOP_DECK: Final = 3


@dataclass(frozen=True)
class ElectionTracker:
    failed_elections: int = 0


def increment_election_tracker(
    tracker: ElectionTracker,
) -> tuple[ElectionTracker, bool]:
    new_failed_elections = (tracker.failed_elections + 1) % FAILURES_UNTIL_TOP_DECK
    return ElectionTracker(
        failed_elections=new_failed_elections
    ), new_failed_elections == 0
