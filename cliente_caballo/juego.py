# cliente_caballo/juego.py

class CaballoSolver:
    def __init__(self, n=8):
        self.n = n
        self.movs_caballo = [(-2, -1), (-1, -2), (1, -2), (2, -1),
                             (2, 1), (1, 2), (-1, 2), (-2, 1)]
        self.tablero = [[-1 for _ in range(n)] for _ in range(n)]
        self.movimientos = []

    def resolver(self, x, y):
        self.tablero[x][y] = 0
        self.movimientos = [(x, y)]
        if self._backtrack(x, y, 1):
            return self.movimientos
        return []

    def _backtrack(self, x, y, movi):
        if movi == self.n * self.n:
            return True

        siguientes = self._ordenar_movimientos(x, y)
        for nx, ny in siguientes:
            self.tablero[nx][ny] = movi
            self.movimientos.append((nx, ny))
            if self._backtrack(nx, ny, movi + 1):
                return True
            self.tablero[nx][ny] = -1
            self.movimientos.pop()

        return False

    def _ordenar_movimientos(self, x, y):
        siguientes = []
        for dx, dy in self.movs_caballo:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.n and 0 <= ny < self.n and self.tablero[nx][ny] == -1:
                grado = self._grado_movimientos(nx, ny)
                siguientes.append((grado, nx, ny))
        siguientes.sort()
        return [(x, y) for _, x, y in siguientes]

    def _grado_movimientos(self, x, y):
        count = 0
        for dx, dy in self.movs_caballo:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.n and 0 <= ny < self.n and self.tablero[nx][ny] == -1:
                count += 1
        return count
