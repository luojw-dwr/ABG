cp pack_xo.tcl build/merged

cd build/merged && vivado_hls -f pack_xo.tcl
