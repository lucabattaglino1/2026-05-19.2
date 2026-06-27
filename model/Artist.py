from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Artist:
    ArtistId: str
    Name: str

