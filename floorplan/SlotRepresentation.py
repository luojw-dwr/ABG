class SlotRepresentation:
    def __init__(self, V, A, As_SG, W_SG):
        self.n_SG = len(V)
        self.V = V
        self.A = A
        self.As_SG = As_SG
        self.W_SG = W_SG
    def __repr__(self):
        return f"SlotRepresentation(V={self.V}, A={self.A}, As_SG={self.As_SG}, W_SG={self.W_SG})"
