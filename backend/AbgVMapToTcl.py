def abgVMapToTcl(hierPrefix, vMap):
    return '\n'.join([
        f"add_cells_to_pblock [get_pblocks {v_SG.name} [get_cells -quiet [list {hierPrefix}/{v_DG.name}]]]"
        for (v_DG, v_SG) in vMap.items()
    ])
