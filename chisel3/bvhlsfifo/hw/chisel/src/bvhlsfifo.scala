import chisel3._
import chisel3.util._

class bvhlsfifo(
  val bw: Int,
  val lat: Int,
  val vname: String,
  val bvname: String
) extends RawModule {
  override val desiredName = bvname
  val clk   = IO(Input(Clock()))
  val reset = IO(Input(AsyncReset()))
  val if_read_ce  = IO(Input(Bool()))
  val if_write_ce = IO(Input(Bool()))
  val if_full_n   = IO(Output(Bool()))
  val if_empty_n  = IO(Output(Bool()))
  val if_write    = IO(Input(Bool()))
  val if_read     = IO(Input(Bool()))
  val if_din      = IO(Input(UInt(bw.W)))
  val if_dout     = IO(Output(UInt(bw.W)))

  val fifo = Module(new vhlsfifo(bw, vname))
  val pipe = Seq.tabulate(lat)(_ => {
      Module(new SkidBuffer(UInt(bw.W), bvname))
  })

  if (lat > 0) {
    fifo.clk   := clk
    fifo.reset := reset
    fifo.if_read_ce  := if_read_ce
    fifo.if_write_ce := if_write_ce
    pipe map (x => {
      x.clk := clk
      x.reset := reset
      x.ce := true.B
    })
    (pipe.slice(0, lat - 1) zip pipe.slice(1, lat)) map ({case (u, v) => {
      u.dout <> v.din
    }})
    if_full_n := fifo.if_full_n
    pipe(0).din.valid := fifo.if_empty_n
    fifo.if_write := if_write
    fifo.if_read := pipe(0).din.ready
    fifo.if_din := if_din
    pipe(0).din.bits := fifo.if_dout
    pipe(lat - 1).dout.ready := if_read
    if_dout := pipe(lat - 1).dout.bits
    if_empty_n := pipe(lat - 1).dout.valid
  } else {
    fifo.clk := clk
    fifo.reset := reset
    fifo.if_read_ce := if_read_ce
    fifo.if_write_ce := if_write_ce
    if_full_n := fifo.if_full_n
    if_empty_n := fifo.if_empty_n
    fifo.if_write := if_write
    fifo.if_read := if_read
    fifo.if_din := if_din
    if_dout := fifo.if_dout
  }
}
