from dataclasses import dataclass


@dataclass(frozen=True)
class Government:
    chancellor_uid: int
    president_uid: int
    elected: bool = False
