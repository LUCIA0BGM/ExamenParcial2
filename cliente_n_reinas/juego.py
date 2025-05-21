# cliente_n_reinas/juego.py

class NReinasSolver:
    def __init__(self, n):
        self.n = n
        self.solucion = []
        self.pasos = 0

    def resolver(self):
        self.solucion = []
        self.pasos = 0
        self._backtrack([])
        return self.solucion, self.pasos

    def _backtrack(self, estado_parcial):
        if len(estado_parcial) == self.n:
            self.solucion.append(estado_parcial[:])
            return

        for col in range(self.n):
            self.pasos += 1
            if self._es_valido(estado_parcial, col):
                estado_parcial.append(col)
                self._backtrack(estado_parcial)
                estado_parcial.pop()

    def _es_valido(self, estado_parcial, col):
        fila_actual = len(estado_parcial)
        for fila_anterior in range(fila_actual):
            if (estado_parcial[fila_anterior] == col or
                abs(estado_parcial[fila_anterior] - col) == abs(fila_actual - fila_anterior)):
                return False
        return True
