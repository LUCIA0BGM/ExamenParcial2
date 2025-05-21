# cliente_hanoi/juego.py

class HanoiSolver:
    def __init__(self, num_discos):
        self.num_discos = num_discos
        self.movimientos = []

    def resolver(self):
        self.movimientos = []
        self._mover(self.num_discos, 'A', 'C', 'B')
        return self.movimientos

    def _mover(self, n, origen, destino, auxiliar):
        if n == 1:
            self.movimientos.append((origen, destino))
        else:
            self._mover(n - 1, origen, auxiliar, destino)
            self.movimientos.append((origen, destino))
            self._mover(n - 1, auxiliar, destino, origen)
