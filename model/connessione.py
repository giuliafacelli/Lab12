from dataclasses import dataclass
from model.rifugio import Rifugio
import datetime

@dataclass
class Connessione:
    rifugio1: Rifugio
    rifugio2: Rifugio
    distanza: float
    difficolta: str
    durata: datetime.time

    def __str__(self):
        return (f'Sentiero: {self.rifugio1} - {self.rifugio2} --> {self.distanza} km'
                f'Difficolta: {self.difficolta}'
                f'Durata: {self.durata}'
                f'Anno: {self.anno}')

    def __repr__(self):
        return (f'Sentiero: {self.rifugio1} - {self.rifugio2} --> {self.distanza} km'
                f'Difficolta: {self.difficolta}'
                f'Durata: {self.durata}'
                f'Anno: {self.anno}')