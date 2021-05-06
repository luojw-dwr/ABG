import os
import json

top_name = "kernel3"
proj_name = "kernel3_u250"
proj_raw_path = "assets/kernel3_u250/"

try:
    os.makedirs("build/merged")
except FileExistsError:
    pass

os.system(f"cp -r {proj_raw_path} build/merged")
os.system(f"rm -r build/merged/{proj_name}/solution/syn/vhdl/")
os.system(f"rm -r build/merged/{proj_name}/solution/impl/vhdl/")
os.system(f"cp build/verilog/* build/merged/{proj_name}/solution/impl/verilog/")
os.system(f"mv build/merged/{proj_name}/solution/impl/verilog/{top_name}_{top_name}_postABG.v build/merged/{proj_name}/solution/impl/verilog/{top_name}_{top_name}.v")
os.system(f"sed -i 's/module*_postABG/module {top_name}_{top_name}/' build/merged/{proj_name}/solution/impl/verilog/{top_name}_{top_name}.v")

with open(f"build/merged/{proj_name}/solution/solution_data.json", 'r') as f:
    solution_data_json = json.loads(f.read())

del solution_data_json["Files"]["Vhdl"]
for vname in os.listdir("build/verilog/"):
    solution_data_json["Files"]["Verilog"].append(f"impl/verilog/{vname}")
solution_data_json["Files"]["CSource"] = ["src/kernel_kernel_new.cpp"]
os.system("mkdir build/merged/src")
os.system("touch build/merged/sec/kernel_kernel_new.cpp")

with open(f"build/merged/{proj_name}/solution/solution_data.json", 'w') as f:
    f.write(json.dumps(solution_data_json, indent=True))
os.system(f"sed -i 's/\\//\\\\\\//g' build/merged/{proj_name}/solution/solution_data.json")
