def abgVMapToTcl(hierPrefix, vMap):
    if hierPrefix[-1] == "/":
        hierPrefix = hierPrefix[:-1]
    return '\n'.join([
        f"add_cells_to_pblock [get_pblocks {v_SG.name} [get_cells -quiet [list {hierPrefix}/{v_DG.name}]]]"
        for (v_DG, v_SG) in vMap.items()
    ])
