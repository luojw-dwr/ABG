class DataflowRepresentation:
    def __init__(self, V, A, As_DG, W_DG):
        self.n_DG = len(V)
        self.V = V
        self.A = A
        self.As_DG = As_DG
        self.W_DG = W_DG
    def __repr__(self):
        return f"DataflowRepresentation(V={self.V}, A={self.A}, As_DG={self.As_DG}, W_DG={self.W_DG})"
