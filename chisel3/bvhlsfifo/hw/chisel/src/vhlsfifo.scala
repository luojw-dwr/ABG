import chisel3._
import chisel3.util._
import chisel3.experimental.ExtModule

class vhlsfifo(val bw: Int, val vname: String) extends ExtModule {
  override val desiredName = vname
  val clk         = IO(Input(Clock()))
  val reset       = IO(Input(Reset()))
  val if_read_ce  = IO(Input(Bool()))
  val if_write_ce = IO(Input(Bool()))
  val if_full_n   = IO(Output(Bool()))
  val if_empty_n  = IO(Output(Bool()))
  val if_write    = IO(Input(Bool()))
  val if_read     = IO(Input(Bool()))
  val if_din      = IO(Input(UInt(bw.W)))
  val if_dout     = IO(Output(UInt(bw.W)))
}
