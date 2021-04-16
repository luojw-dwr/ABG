import csv
import io

def latencyGraphToBufferSpec(lg):
    s = io.StringIO()
    fc = csv.DictWriter(s, fieldnames=[
        "bw", "lat", "vname", "bvname"
    ])
    fc.writeheader()
    for e_LG in lg.E:
        for e_MG in e_LG.components:
            fc.writerow({
                "bw": e_MG.width,
                "lat": e_LG.lat + e_LG.bal,
                "vname": e_MG.module_name,
                "bvname": f"{e_MG.name}_M"
            })
    spec = s.getvalue()
    s.close()
    return spec
