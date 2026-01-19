
---

# MySQL 数据库运维手册（SOP）

## 📘 目录

1. [概述](#概述)
2. [慢 SQL（Slow Query）处理流程](#慢-sqlslow-query处理流程)
3. [空间告警处理流程](#空间告警处理流程)
4. [资源告警处理流程（CPU/内存/IO）](#资源告警处理流程cpumemio)
5. [附录：常用诊断 SQL](#附录常用诊断-sql)

---

# 概述

本手册用于指导数据库运维工程师在生产环境中快速处理 MySQL 常见运维告警，包括：

* 慢 SQL 导致的服务延迟/超时
* 存储空间不足，影响写入
* CPU、内存、IO 等资源占用异常
* 提供标准化、可审计的排查步骤

---

# 慢 SQL（Slow Query）处理流程

## 🔍 1. 告警定义

常见慢 SQL 告警来源：

* APM/Tracing 慢事务报警
* RDS 慢日志检测（如 MySQL slow_log）
* MySQL 监控系统 QPS/执行时延异常

阈值示例：

* 执行时间 > 1s
* Rows_examined > 10k
* QPS/RT 持续异常增长

---

## 🧭 2. 处理步骤

### **步骤 1：确认影响范围**

* 是否影响业务（超时、响应变慢）
* 是否影响数据库（CPU/IO 是否飙高）
* 单 SQL 还是批量 SQL?

记录影响范围。

---

### **步骤 2：获取慢 SQL 详细信息**

常见方式：

#### 📌 方法 A：RDS 或 APM 采集（推荐）

通常可直接看到：

* SQL 内容
* 执行时间
* 执行计划
* 绑定参数

#### 📌 方法 B：数据库手动查询

若启用了慢日志表：

```sql
SELECT * FROM mysql.slow_log ORDER BY start_time DESC LIMIT 10;
```

---

### **步骤 3：分析 SQL 执行计划**

```sql
EXPLAIN <your SQL>;
```

重点关注：

* type 是否为 `ALL`（全表扫描）
* key 是否为空
* rows 是否非常大
* extra 是否包含“Using temporary / Using filesort”

---

### **步骤 4：优化 SQL 或索引**

常见优化方向：

| 问题     | 解决方案                |
| ------ | ------------------- |
| 未命中索引  | 增加索引 / 调整字段顺序       |
| 全表扫描   | 增加 where 条件 或重构 SQL |
| 排序/分组慢 | 索引优化 / 增加合适的索引      |
| Join 慢 | 确认 join 字段一致性并加索引   |
| 返回字段过多 | 使用更少字段（避免 SELECT *） |

---

### **步骤 5：在低峰期验证 SQL 性能**

* 执行 explain analyze（MySQL 8.0）
* 对新索引进行评估
* 必要时进行 SQL 回归测试

---

### **步骤 6：上线优化方案并记录变更**

变更内容包括：

* 增加/删除索引
* 重写 SQL
* schema 变更
* 参数调整（如优化器 hints）

---

---

# 空间告警处理流程

## 📌 1. 告警定义

当数据库存储空间使用超过阈值时触发，例如：

* 磁盘使用率 > 80%
* 表空间增长异常
* Binlog 占满磁盘

---

## 🧭 2. 处理步骤

### **步骤 1：确认空间不足原因**

常见原因：

* 业务数据短期暴增
* binlog 未清理
* undo/redo 过大
* 大事务未提交
* 临时表撑爆

检查磁盘使用：

```sql
SELECT table_schema, SUM(data_length + index_length)/1024/1024 AS mb
FROM information_schema.tables GROUP BY table_schema;
```

---

### **步骤 2：清理空间（安全优先）**

#### ✔ 清理 binlog（谨慎）

```sql
SHOW BINARY LOGS;
PURGE BINARY LOGS TO 'mysql-bin.010200';
```

#### ✔ 清理历史数据（归档）

常见做法：

* 移动老数据到 archive 表
* 批量删除（分批删除，避免大事务）
* 业务方确认可删除的日志数据

示例（分批删除）：

```sql
DELETE FROM logs WHERE created < DATE_SUB(NOW(), INTERVAL 30 DAY) LIMIT 5000;
```

---

### **步骤 3：处理 temp/undo 涨高**

#### 临时表大量占用磁盘

检查：

```sql
SHOW GLOBAL STATUS LIKE 'Created_tmp%';
```

解决：

* 优化排序、分组 SQL
* 增加 tmpdir 存储空间

#### undo 过大

* 可能有长事务
  查看：

```sql
SHOW ENGINE INNODB STATUS;
```

终止问题事务（确保业务确认）：

```sql
KILL <thread_id>;
```

---

### **步骤 4：表空间收缩**

InnoDB 表可通过重建释放空间：

```sql
ALTER TABLE mytable ENGINE=InnoDB;
```

或

```sql
OPTIMIZE TABLE mytable;
```

---

---

# 资源告警处理流程（CPU/MEM/IO）

## 🔥 1. 告警定义

常见资源告警：

| 指标                          | 典型阈值          |
| --------------------------- | ------------- |
| CPU 使用率                     | > 80% 持续 5 分钟 |
| 内存占用                        | > 90%         |
| IOPS                        | > 85%         |
| InnoDB Buffer Pool Hit Rate | < 95%         |

---

## 🧭 2. 排查步骤

### **步骤 1：查看 MySQL 当前耗资源连接**

```sql
SHOW PROCESSLIST;
```

记录：

* 正在执行的 SQL
* 锁等待情况
* 大事务

---

### **步骤 2：排查 CPU 升高原因**

```sql
SELECT *
FROM performance_schema.events_statements_summary_by_digest
ORDER BY SUM_TIMER_WAIT DESC LIMIT 10;
```

重点关注：

* 大量慢 SQL / 全表扫描
* 频繁 join / filesort / temp table

解决方式：

* SQL 优化
* 增加索引
* 增加只读实例分担请求

---

### **步骤 3：排查 IO 升高原因**

```sql
SHOW GLOBAL STATUS LIKE 'Innodb_data_reads';
SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool_reads';
```

若 buffer pool hit rate < 95%，需：

* 增大 innodb_buffer_pool_size
* 热数据量 > 内存 → 考虑分库分表/升级实例规格

---

### **步骤 4：排查内存不足原因**

* 大量连接：

```sql
SHOW GLOBAL STATUS LIKE 'Threads_connected';
```

* 大查询导致 buffer 使用激增
* join buffer / sort buffer 设置过大

调整建议：

* 降低 join_buffer_size
* 降低 sort_buffer_size
* 减少 max_connections 或引入连接池

---

### **步骤 5：必要时扩容**

若优化后资源仍不足，则：

* 升级实例规格
* 增加只读实例承载只读查询
* 分库/分表

---

---

# 附录：常用诊断 SQL

## 🔧 查看慢 SQL Top 10

```sql
SELECT * FROM performance_schema.events_statements_summary_by_digest
ORDER BY AVG_TIMER_WAIT DESC LIMIT 10;
```

## 🔧 查看锁等待

```sql
SHOW ENGINE INNODB STATUS;
```

## 🔧 查看表大小

```sql
SELECT table_schema, table_name,
       data_length/1024/1024 AS data_mb,
       index_length/1024/1024 AS index_mb
FROM information_schema.tables
ORDER BY data_mb DESC LIMIT 20;
```

## 🔧 大事务检查

```sql
SELECT * FROM information_schema.innodb_trx;
```

---

# 📚 结语

本 MySQL 运维手册可用于：

* 数据库日常巡检
* 生产环境告警处理
* 提升 DBA 标准化与可审计性


