package sca

/**
 * Created by dell on 2017/9/12.
 */

import java.net.InetAddress


import org.apache.hadoop.hbase.mapreduce.TableInputFormat
import org.apache.hadoop.hbase.util.Bytes
import org.apache.hadoop.hbase.{CellUtil, HBaseConfiguration}
import org.elasticsearch.hadoop.cfg.PropertiesSettings

import org.elasticsearch.spark._
import org.apache.spark.{TaskContext, SparkConf, SparkContext}
import org.elasticsearch.spark.cfg.SparkSettingsManager
import org.elasticsearch.spark.rdd.{ESWriter, EsSpark, EsRDDWriter}
//import org.elasticsearch.spark.rdd.EsSpark

object SparkSaveES_Socket {

   def main(args: Array[String]) {
     val conf = new SparkConf().setAppName("save2es")
     conf.set("es.index.auto.create", "true")
     conf.set("es.nodes", "192.168.12.34:9200")
     conf.set("es.resource", "spark/docs")          //使用自定义分区时
     conf.set("es.net.http.auth.user", "elastic")
     conf.set("es.net.http.auth.pass", "changeme")
 //    写入ES的数据当做String写入，不需要转为Date
 //    conf.set("es.mapping.date.rich","false")
 //    conf.set("es.read.field.exclude","casedate")
 //    conf.set("es.read.field.exclude","record_time_new")

     val sc = new SparkContext(conf)
     sc.setLogLevel("ERROR")


 //    val numbers = Map("one" -> 1, "two" -> 2, "three" -> 3)
 //    val airports = Map("arrival" -> "Otopeni", "SFO" -> "San Fran")
 //    sc.makeRDD(Seq(numbers, airports)).saveToEs("spark/docs")
 //    EsSpark.saveToEs()
     val sparkCfg = new SparkSettingsManager().load(conf)
     val settings = sparkCfg.save()
//     val config = new PropertiesSettings().load()

     val tablename = "laws_doc:judgment"
     val hconf = HBaseConfiguration.create()
     //设置zooKeeper集群地址，也可以通过将hbase-site.xml导入classpath，但是建议在程序里这样设置
 //    hbase参数的设置与python一样，都是：TableInputFormat.java类中的属性！
 //    hbase.mapreduce.scan.row.start
 //    hbase.mapreduce.scan.row.stop
 //    hbase.mapreduce.scan.column.family
 //    hbase.mapreduce.scan.columns
 //    hbase.mapreduce.scan.timestamp
 //    hbase.mapreduce.scan.timerange.start
 //    hbase.mapreduce.scan.timerange.end
 //    hbase.mapreduce.scan.maxversions
 //    hbase.mapreduce.scan.cacheblocks
 //    hbase.mapreduce.scan.cachedrows
 //    hbase.mapreduce.scan.batchsize
     hconf.set("hbase.zookeeper.quorum","cdh-master,cdh-slave1,cdh-slave2")
     //设置zookeeper连接端口，默认2181
     hconf.set("hbase.zookeeper.property.clientPort", "2181")
     hconf.set(TableInputFormat.INPUT_TABLE, tablename)

 //    hconf.set("hbase.mapreduce.scan.row.start","2000000")
 //    hconf.set("hbase.mapreduce.scan.row.stop","2000002")
//     hconf.set("hbase.mapreduce.scan.row.start","2000000")
//     hconf.set("hbase.mapreduce.scan.row.stop","2100000")
     hconf.set("hbase.mapreduce.scan.row.start","1300000")
     hconf.set("hbase.mapreduce.scan.row.stop","1310000")
 //    hconf.set("","")
 //    hconf.set("","")
 //    hconf.set("","")
 //    hconf.set("","")

     // 如果表不存在则创建表
 //    val admin = new HBaseAdmin(hconf)
 //    if (!admin.isTableAvailable(tablename)) {
 //      val tableDesc = new HTableDescriptor(TableName.valueOf(tablename))
 //      admin.createTable(tableDesc)
 //    }

     //读取数据并转化成rdd
     val hBaseRDD = sc.newAPIHadoopRDD(hconf, classOf[TableInputFormat],
       classOf[org.apache.hadoop.hbase.io.ImmutableBytesWritable],
       classOf[org.apache.hadoop.hbase.client.Result])

 //    val count = hBaseRDD.count()
 //    println(count)
 //    hBaseRDD.map{case (_,v) => v}.saveToEs("spark/docs")

     hBaseRDD.map{case (_,result) =>{
       //获取行键
       val rowkey = Bytes.toString(result.getRow)
       var m = scala.collection.mutable.Map("rowkey" -> rowkey)
       val iter = result.listCells().iterator()
       while (iter.hasNext) {
         val cell = iter.next()
         var v = Bytes.toString(CellUtil.cloneValue(cell))
         if (!("".equals(v))) {
           m += (Bytes.toString(CellUtil.cloneQualifier(cell)) -> v)
         }
       }
       val li = List("title","party_info","trial_process","trial_request","trial_reply","court_find","court_idea","judge_result")
       var all_fileds = ""
       for (i <- li)
         all_fileds += Bytes.toString(result.getValue("d".getBytes,i.getBytes))

       m += ("all" -> all_fileds)
       //      println(m.size.toString + "===================")
       //      println(m.toString() + "============================")

       //通过列族和列名获取列
      val uuid = Bytes.toString(result.getValue("d".getBytes,"uuid".getBytes))
      val casedate = Bytes.toString(result.getValue("d".getBytes,"casedate".getBytes))
      val lawlist = Bytes.toString(result.getValue("d".getBytes,"lawlist".getBytes))
//      result.listCells()
//      result.getMap
//      println("Row key:"+rowkey+"| uuid:"+uuid+" |casedate:"+casedate + " |lawlist: " + lawlist)
//       (rowkey.toInt,m.toMap)
       (rowkey,m.toMap)

     }}.partitionBy(new ESShardPartitioner(settings))
     .saveToEsWithMeta("spark/docs")

//       .foreachPartition{ iter =>
//         try {
//           val newSettings = new PropertiesSettings().load(settings)

//           val writer = EsSpark.createEsRDDWriter[Map[String,String]](settings, resource)
       //创建EsRDDWriter
//        val newSettings = new PropertiesSettings().load(settings)


//        val s = ESWriter.write()
//           val writer = EsRDDCreator.createWriter(newSettings.save())
//           writer.write(TaskContext.get(), iter.map(f => f._2))


//     }catch {

//         }
      sc.stop()
 //    admin.close()


   }

 }
