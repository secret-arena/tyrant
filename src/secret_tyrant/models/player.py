from dataclasses import dataclass
from secret_tyrant.models.enums import Party, Role

@dataclass
class Player:
    uid: int
    party: Party
    role: Role
