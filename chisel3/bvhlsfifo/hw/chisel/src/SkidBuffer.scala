import chisel3._
import chisel3.util._

class SkidBuffer[T <: Data](private val gen: T, val bvname: String) extends RawModule {

  override val desiredName = f"${bvname}_SkidBuffer"

  val clk   = IO(Input(Clock()))
  val ce    = IO(Input(Bool()))
  val reset = IO(Input(AsyncReset()))
  val din  = IO(Flipped(Decoupled(gen)))
  val dout = IO(Decoupled(gen))
  
  val idata  = din.bits
  val iready = withClockAndReset(clk, reset){RegInit(true.B)}
  val ivalid = din.valid

  val rdata  = withClockAndReset(clk, reset){Reg(gen)}
  val rvalid = withClockAndReset(clk, reset){RegInit(false.B)}

  val odata  = withClockAndReset(clk, reset){Reg(gen)}
  val oready = dout.ready
  val ovalid = withClockAndReset(clk, reset){RegInit(false.B)}

  when (ce) {
    iready := ~rvalid

    when (((~rvalid) & ovalid & (~oready) & iready & ivalid)) {
      rdata := idata
    }
    rvalid := Mux(rvalid,
      ovalid & (~oready),
      ovalid & (~oready) & iready & ivalid
    )

    when (ovalid & oready) {
      odata := Mux(rvalid, rdata, idata)
    }
    ovalid := Mux(ovalid,
      (~oready) || (iready & ivalid) || rvalid,
      (iready & ivalid) || rvalid
    )
  }

  din.ready := iready

  dout.bits  := odata
  dout.valid := ovalid
}
