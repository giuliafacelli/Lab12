from dataclasses import dataclass

@dataclass
class Rifugio:
    id: int
    nome: str
    localita: str

    def __str__(self):
        return f'[{self.id}] {self.nome} ({self.localita})'

    def __eq__(self, other):
        return isinstance(other, Rifugio) and self.id == other.id

    def __hash__(self):
        return hash(self.id)