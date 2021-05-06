TOP=kernel3
PLATFORM=xilinx_u250_xdma_201830_2
XO="build/merged/polysa.xo"
output_dir="build/vitis_run"

mkdir build/vitis_run

cat build/tcl/prefloorplan.tcl > build/vitis_run/constr.tcl
cat build/tcl/buf_constr.tcl >> build/vitis_run/constr.tcl
cat build/tcl/pe_constr.tcl >> build/vitis_run/constr.tcl

CONSTRAINT=build/vitis_run/constr.tcl

env LC_ALL=C v++ \
    --link \
    --output "${output_dir}/${TOP}_${PLATFORM}.xclbin" \
    --kernel ${TOP} \
    --platform ${PLATFORM} \
    --target hw \
    --report_level 2 \
    --temp_dir "${output_dir}/${TOP}_${PLATFORM}.temp" \
    --optimize 3 \
    --connectivity.nk ${TOP}:1:${TOP}_1 \
    --max_memory_ports ${TOP} \
    --save-temps \
    ${XO} \
    --kernel_frequency 330 \
    --vivado.prop run.impl_1.STEPS.OPT_DESIGN.TCL.PRE=$CONSTRAINT \
    --export_script
