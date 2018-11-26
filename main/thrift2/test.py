import sys  

sys.path.append('./thrift/packages')
sys.path.append('./thrift')

from thrift import Thrift  
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.packages.hbase import THBaseService
from thrift.packages.hbase.ttypes import *

transport = TSocket.TSocket('10.255.1.35', 9090)
transport = TTransport.TBufferedTransport(transport)
protocol = TBinaryProtocol.TBinaryProtocol(transport)
client = THBaseService.Client(protocol)

transport.open()
tableName = 'topic_static_test'
rowKey = '4114392867856261'
get = TGet()
get.row = rowKey
result = client.get(tableName, get)
#print result
print result.row

created = ''
modified = ''

for columnValue in result.columnValues:
	if 'created' == columnValue.qualifier: 
		created = columnValue.value
	elif 'modified' == columnValue.qualifier: 
		modified = columnValue.value
	else:
		continue
	
print 'created is ', created
print 'modified is ', modified

#coulumnValue1 = TColumnValue('cf','created_time',created)
#coulumnValue2 = TColumnValue('cf','modified_time',modified)
#
#coulumnValues = [coulumnValue1,coulumnValue2]
#print 'coulumnValues is ', coulumnValues
#
#tPut = TPut(rowKey,coulumnValues)
#print 'tPut is ', tPut
#
#result = client.put(tableName, tPut)
#print 'Put result is ', result

#coulumnValue1 = TColumnValue('cf','modified')
#coulumnValues = [coulumnValue1]
#tdelete = TDelete(rowKey,coulumnValues)

#print 'tdelete is ',tdelete

#result = client.deleteSingle(tableName,tdelete)

#print 'delete result is ',result

transport.close()