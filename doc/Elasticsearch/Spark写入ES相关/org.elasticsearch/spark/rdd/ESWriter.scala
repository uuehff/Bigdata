package org.elasticsearch.spark.rdd

import org.apache.spark.TaskContext

/**
 * Created by dell on 2017/9/21.
 *
 * (val serializedSettings: String,
                                              val runtimeMetadata: Boolean = false)
 */
object ESWriter {
//  taskContext: TaskContext, data: Iterator[String]
  def write(serializedSettings: String,runtimeMetadata: Boolean = false,taskContext: TaskContext, data: Iterator[(String,scala.collection.Map[String,String])])= {
//        print("ESWriter====================================================")
        new EsRDDWriter(serializedSettings,true).write(taskContext,data)

  }

}
