import chisel3._
import chisel3.util._

import scala.io.Source

case class ReqEntry (
  val bw:  Int,
  val lat: Int,
  val vname:  String,
  val bvname: String
)

object ReqEntry {
  def parseReqCSV(path: String) = {
    val source = Source.fromFile(path)
    val lines = source.getLines.toArray
    source.close
    val lines_head = lines(0)
    val lines_tail = lines.slice(1, lines.size)
    val keymap =
      lines_head.split(",").zipWithIndex.map({case (key, idx) => {
        key -> idx
    }}).toMap
    lines_tail map (x => {
      val xs = x.split(",")
      ReqEntry(
        xs(keymap("bw")).toInt,
        xs(keymap("lat")).toInt,
        xs(keymap("vname")),
        xs(keymap("bvname"))
      )
    })
  }
}

object Main extends App {
  val reqs = ReqEntry.parseReqCSV("../req.csv")
  reqs map (req => {
    Driver.execute(args, () => new bvhlsfifo(
      req.bw,
      req.lat,
      req.vname,
      req.bvname
    ))
  })
}
