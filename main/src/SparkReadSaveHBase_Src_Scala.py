# package org.apache.spark.examples.pythonconverters
#
#
# import org.apache.hadoop.hbase.client.Put
# import org.apache.hadoop.hbase.client.Result
# import org.apache.hadoop.hbase.io.ImmutableBytesWritable
# import org.apache.hadoop.hbase.util.Bytes
# import org.apache.spark.api.python.Converter
#
# import scala.collection.JavaConverters._
# import scala.util.parsing.json.JSONObject
# import org.apache.hadoop.hbase.KeyValue.Type
# import org.apache.hadoop.hbase.CellUtil
#
# /**
#  * Implementation of [[org.apache.spark.api.python.Converter]] that converts all
#  * the records in an HBase Result to a String
#  */
# class HBaseResultToStringConverterUserDefine extends Converter[Any, String] {
#   override def convert(obj: Any): String = {
#     val result = obj.asInstanceOf[Result]
#     val output = result.listCells.asScala.map(cell =>
#       Map(
#         "row" -> Bytes.toString(CellUtil.cloneRow(cell)),
#         "columnFamily" -> Bytes.toString(CellUtil.cloneFamily(cell)),
#         "qualifier" -> Bytes.toString(CellUtil.cloneQualifier(cell)),
#         "timestamp" -> cell.getTimestamp.toString,
#         "type" -> Type.codeToType(cell.getTypeByte).toString(),
#         "value" -> Bytes.toString(CellUtil.cloneValue(cell))
#       )
#     )
#     output.map(JSONObject(_).toString()).mkString("\n")
#   }
# }
#
# case class JSONObject (obj : Map[String,Any]) extends JSONType {
#   def toString (formatter : JSONFormat.ValueFormatter) =
#     "{" + obj.map({ case (k,v) => formatter(k.toString) + " : " + formatter(v) }).mkString(", ") + "}"
# }

# type ValueFormatter = Any => String


# /**
#  * Implementation of [[org.apache.spark.api.python.Converter]] that converts an
#  * ImmutableBytesWritable to a String
#  */
# class ImmutableBytesWritableToStringConverterUserDefine extends Converter[Any, String] {
#   override def convert(obj: Any): String = {
#     val key = obj.asInstanceOf[ImmutableBytesWritable]
#     Bytes.toString(key.get())
#   }
# }
#
# /**
#  * Implementation of [[org.apache.spark.api.python.Converter]] that converts a
#  * String to an ImmutableBytesWritable
#  */
# class StringToImmutableBytesWritableConverter extends Converter[Any, ImmutableBytesWritable] {
#   override def convert(obj: Any): ImmutableBytesWritable = {
#     val bytes = Bytes.toBytes(obj.asInstanceOf[String])
#     new ImmutableBytesWritable(bytes)
#   }
# }
#
# /**
#  * Implementation of [[org.apache.spark.api.python.Converter]] that converts a
#  * list of Strings to HBase Put
#  */
# class StringListToPutConverter extends Converter[Any, Put] {
#   override def convert(obj: Any): Put = {
#     val output = obj.asInstanceOf[java.util.ArrayList[String]].asScala.map(Bytes.toBytes).toArray
#     val put = new Put(output(0))
#     put.add(output(1), output(2), output(3))
#   }
# }




