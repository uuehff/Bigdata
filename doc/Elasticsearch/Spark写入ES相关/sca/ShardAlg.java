package sca;

/**
 * Created by dell on 2017/9/19.
 */
public class ShardAlg {
   public static int shard(String id, int shardNum) {

//        int hash = Murmur3HashFunction.hash(id);
        int hash = id.hashCode();
        return mod(hash, shardNum);
    }

    public static int mod(int v, int m) {
        int r = v % m;
        if (r < 0) {
            r += m;
        }
        return r;
    }

}
