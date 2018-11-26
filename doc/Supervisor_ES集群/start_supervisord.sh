#!/bin/bash
echo "master begin start!"
sudo /bin/supervisord -c /etc/supervisor/supervisord.conf
echo "slave1 begin start!"
ssh cdh-slave1 -p 2222 "sudo /bin/supervisord -c /etc/supervisor/supervisord.conf "
echo "slave2 begin start!"
ssh cdh-slave2 -p 2222 "sudo /bin/supervisord -c /etc/supervisor/supervisord.conf "
echo "slave3 begin start!"
ssh cdh-slave3 -p 2222 "sudo /bin/supervisord -c /etc/supervisor/supervisord.conf "
