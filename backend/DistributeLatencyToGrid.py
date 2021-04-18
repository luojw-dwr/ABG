from collections import deque

def distributeLatencyToGridAsTcl(hierPrefix, lg, dg, gg, vMap):
    hierPrefix = hierPrefix[:-1] if hierPrefix[-1] == '/' else hierPrefix
    ss = deque()
    for e_LG in lg.E:
        lat = e_LG.lat + e_LG.bal
        src_GG = gg.V_dict[vMap[dg.V_dict[e_LG.srcName]].name]
        dst_GG = gg.V_dict[vMap[dg.V_dict[e_LG.dstName]].name]
        s_X = 1 if src_GG.X < dst_GG.X else -1
        s_Y = 1 if src_GG.Y < dst_GG.Y else -1
        p_GG = [
            gg.V_coordDict[x, src_GG.Y]
            for x in range(src_GG.X, dst_GG.X + s_X, s_X)
        ] + [
            gg.V_coordDict[dst_GG.X, y]
            for y in range(src_GG.Y, dst_GG.Y + s_Y, s_Y)
        ] 
        q, r = divmod(lat, len(p_GG) - 1)
        for comp in e_LG.components:
            v_GG = p_GG[0]
            s = deque()
            acc = 0
            s.append(
                f"add_cells_to_pblock [get_pblocks {v_GG.name}] [get_cells -quiet [list {hierPrefix}/{comp.name}_M/fifo]]")
            for i in range(r):
                s.append(
                    f"add_cells_to_pblock [get_pblocks {v_GG.name}] [get_cells -quiet [list {hierPrefix}/{comp.name}_M/pipe_{acc}]]")
                acc += 1
            for k in range(1, len(p_GG)):
                v_GG = p_GG[k]
                for i in range(q):
                    s.append(f"add_cells_to_pblock [get_pblocks {v_GG.name}] [get_cells -quiet [list {hierPrefix}/{comp.name}_M/pipe_{acc}]]")
                acc += 1
            ss.extend(s)
    return "\n".join(ss)
