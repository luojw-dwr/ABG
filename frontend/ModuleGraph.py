class ModuleVertex:
    def __init__(self, func_name, module_name, instance_name, area):
        self.func_name = func_name
        self.module_name = module_name
        self.instance_name = instance_name
        self.name = instance_name
        self.area = area
    def __repr__(self):
        return f"ModuleVertex(func_name={self.func_name}, module_name={self.module_name}, instance_name={self.instance_name}, area={self.area})"

class ModuleEdge:
    def __init__(self, module_name, instance_name, width, depth, instance_read_name, instance_write_name):
        self.module_name = module_name
        self.instance_name = instance_name
        self.name = instance_name
        self.width = width
        self.depth = depth
        self.instance_read_name = instance_read_name
        self.instance_write_name = instance_write_name
    def __repr__(self):
        return f"ModuleEdge(module_name={self.module_name}, instance_name={self.instance_name}, width={str(self.width)}, depth={str(self.depth)}, instance_read_name={self.instance_read_name}, instance_write_name={self.instance_write_name})"

class ModuleGraph: # Mono Vertex, Multi Edge
    def __init__(self, V, E):
        self.V = V
        self.E = E
        self.V_dict = {v.instance_name : v for v in self.V}
        self.E_dict = {e.instance_name : e for e in self.E}
    def __repr__(self):
        return f"ModuleGraph(V={self.V}, E={self.E})"
