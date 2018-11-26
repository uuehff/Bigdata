package sca

import org.apache.commons.logging.LogFactory
import org.apache.spark.Partitioner
import org.elasticsearch.hadoop.cfg.PropertiesSettings
import org.elasticsearch.hadoop.rest.RestRepository

import scala.util.Random

/**
 * Created by dell on 2017/9/18.
 */
class ESShardPartitioner(settings:String) extends Partitioner {
  protected val log = LogFactory.getLog(this.getClass())

  protected var _numPartitions = -1
  protected var shardToPartitions = 2

  override def numPartitions: Int = {
    val newSettings = new PropertiesSettings().load(settings)
    val repository = new RestRepository(newSettings)
    val targetShards = repository.getWriteTargetPrimaryShards(newSettings.getNodesClientOnly())
    repository.close()

//    _numPartitions = targetShards.size()   //一个partition对应一个主shard
//    _numPartitions

    if(newSettings.getProperty("es.bulk.shard.partitions") !=null ){
      shardToPartitions = newSettings.getProperty("es.bulk.shard.partitions").toInt

//      print("shardToPartitions : ----------" + shardToPartitions)
    }
    _numPartitions = targetShards.size()
    _numPartitions * shardToPartitions

  }

  override def getPartition(key: Any): Int = {
    val shardId = ShardAlg.shard(key.toString(), _numPartitions)
//    shardId
    val paritions = ((shardId * shardToPartitions) until (shardId * shardToPartitions + shardToPartitions)).toList
    val targetPartitionId = Random.shuffle(paritions).head
    targetPartitionId
  }
}


object ESShardPartitioner {

  def shardIdFromPartitionId(partitionId:Int,shardToPartitions:Int):Int={
      if (partitionId < shardToPartitions) return 0
          partitionId / shardToPartitions
  }

}
