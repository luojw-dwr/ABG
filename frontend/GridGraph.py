class GridVertex:
    def __init__(self, name, X, Y, area):
        self.name = name
        self.X = X
        self.Y = Y
        self.area = area
    def __repr__(self):
        return f"GridVertex(X={self.X}, Y={self.Y}, area={self.area})"

class GridGraph:
    def __init__(self, V):
        self.V = V
        self.V_dict = {v.name : v for v in V}
        self.V_coordDict = {(v.X, v.Y) : v for v in V}
    def __repr__(self):
        return f"GridGraph(V={self.V}, V_dict={self.V_dict})"
