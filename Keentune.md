# 关于Keentune
KeenTune是阿里云全自研的智能化性能调优工具，目前已经在龙蜥社区进行开源。请访问：
* [KeenTune官网](http://keentune.io/home/)
* [龙蜥社区KeenTune SIG](https://openanolis.cn/sig/keentune)
* [Keentune代码仓库](https://gitee.com/anolis/keentuned)

# 使用方式
## Step 1
在Alibaba Cloud Linux 3.2104版本可以使用yum安装keentuned和keentune-target组件：
```
yum install keentuned
yum install -y keentune-target
```
安装完成后，请检查keentune版本为1.3.3：
```
keentune version
keentune version 1.3.3
```
安装keentune-target的依赖包tornado：
```
pip3 install tornado
```
之后，可以启动keentune：
```
systemctl start keentuned
systemctl start keentune-target
```
检查两个组件的状态都为active即表示keentune组件安装成功。

## Step 2 查看可用的专家调优知识库
使用keentune profile list可以查看按照场景划分提供的可用的专家调优知识库：
```
keentune profile list
[available]    cpu_high_load.conf
[available]    io_high_throughput.conf
[available]    net_high_throuput.conf
[available]    net_low_latency.conf
[available]    mysql_yitian.conf
[available]    nginx_yitian.conf
[available]    pgsql_yitian.conf
[available]    redis_yitian.conf
```
如果需要查看某一种调优知识库的具体内容，可以使用keentune profile info命令，以mysql为例：
```
keentune profile info --name mysql_yitian.conf
[net]
XPS = different
# XPS i.e. different, off
RPS = different
# RPS i.e. different, off
smp_affinity = dedicated
# smp_affinity i.e. different, dedicated, off

[kernel_mem]
code_hugepage = 1
# code_hugepage i.e. 0, 1, 2, 3
TLBI = "recommend: TLB range improvement. Please refer to https://gitee.com/anolis/keentuned/blob/dev-1.3.2/docs/profile_features/TLBI%20-%20TLB%20range%E4%BC%98%E5%8C%96.md"

[kernel_io]
atomic_write = "recommend：Close MySQL double write and use 16K atomic write can improve write request performance. Please refer to https://gitee.com/anolis/keentuned/blob/dev-1.3.2/docs/profile_features/16K%E5%8E%9F%E5%AD%90%E5%86%99.md"
ext4_fast_commit = "recommend: fast commit for ext4. Please refer to https://gitee.com/anolis/keentuned/blob/dev-1.3.2/docs/profile_features/EXT4%20Fast%20Commit.md"

[kernel_sec]
E0PD = "recommend: Please use E0PD instead of BHB. Please refer to https://gitee.com/anolis/keentuned/blob/dev-1.3.2/docs/profile_features/E0PD.md"

[mysql_compile]
LSE = "recommend: LSE appplies GCC compile promotion. Please refer to https://gitee.com/anolis/keentuned/blob/dev-1.3.2/docs/profile_features/LSE%E6%8C%87%E4%BB%A4%E9%9B%86%E7%BC%96%E8%AF%91%E4%BC%98%E5%8C%96.md"
LTO = "recommend: Link Time Optimization. Please refer to https://gitee.com/anolis/keentuned/blob/dev-1.3.2/docs/profile_features/LTO.md"
PGO = "recommend：PGO can produce optimal code by using application runtime data. Please refer to: https://gitee.com/anolis/keentuned/blob/dev-1.3.2/docs/profile_features/PGO.md"

[sysctl]
kernel.sched_min_granularity_ns = 3000000
kernel.sched_wakeup_granularity_ns = 4000000

[my_cnf]
__ENV-LIMITATION = "#!CPU_CORE#=8 & #!MEM_TOTAL#=32"
# Configurations for my.cnf only matches 8C32G VM
character_set_server = utf8
collation_server = utf8_general_ci
max_heap_table_size = 67108864
max_allowed_packet = 1073741824
thread_stack = 262144
interactive_timeout = 7200
wait_timeout = 86400
sort_buffer_size = 2097152
read_buffer_size = 1048576
read_rnd_buffer_size = 256K
join_buffer_size = 1048576
net_buffer_length = 16384
thread_cache_size = 100
ft_min_word_len = 4
transaction_isolation = READ-COMMITTED
tmp_table_size = 2097152
core-file = SET_TRUE
skip_name_resolve = SET_TRUE
skip_ssl = SET_TRUE

default_authentication_plugin = mysql_native_password
max_connections = 5000
max_user_connections = 5000
max_prepared_stmt_count = 1728000

binlog_cache_size = 1048576
max_binlog_size = 500M
sync_binlog = 1000
binlog_format = ROW
gtid_mode = ON
enforce-gtid-consistency = 1

innodb_flush_log_at_trx_commit = 2
innodb_buffer_pool_instances = 8
innodb_buffer_pool_size = 12884901888
innodb_file_per_table = 1
innodb_log_buffer_size = 16M
innodb_log_file_size = 2048M
innodb_log_files_in_group = 2
innodb_max_dirty_pages_pct = 75
innodb_flush_method = O_DIRECT
innodb_lock_wait_timeout = 50
innodb_doublewrite = 1
innodb_rollback_on_timeout = OFF
innodb_autoinc_lock_mode = 2
innodb_purge_threads = 1
innodb_lru_scan_depth = 1024
innodb_open_files = 2000

table_open_cache = 2048
table_open_cache_instances = 8

innodb_read_io_threads = 4
innodb_write_io_threads = 4
innodb_io_capacity = 20000
innodb_io_capacity_max = 40000

autocommit = ON
innodb_deadlock_detect = ON
event_scheduler = OFF
performance_schema = OFF

loose_thread_pool_enabled = OFF
loose_thread_pool_size = 4
loose_innodb_rds_flashback_task_enabled = OFF
loose_innodb_undo_retention = 0
```

## Step3. 设置需要的专家调优知识库
使用keentune profile set命令来进行设置。以MySQL为例
```
keentune profile set mysql_yitian.conf
```
可用profile为上文keentune profile list的输出
```
keentune profile list
[available]    cpu_high_load.conf
[available]    io_high_throughput.conf
[available]    net_high_throuput.conf
[available]    net_low_latency.conf
[available]    mysql_yitian.conf
[available]    nginx_yitian.conf
[available]    pgsql_yitian.conf
[available]    redis_yitian.conf
```

