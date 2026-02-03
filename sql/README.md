# 高校教材管理系统 - SQL脚本说明

## 脚本执行顺序

请按照以下顺序在 MySQL Workbench 中执行SQL脚本：

### 1. 01_create_database.sql
- 创建数据库 `textbook_management`
- 设置字符集为 utf8mb4

### 2. 02_create_tables.sql
- 创建所有数据表
- 建立表之间的外键约束
- 创建索引优化查询性能

### 3. 03_create_triggers.sql
- 创建触发器实现自动库存管理
- 入库触发器：自动更新库存和订单状态
- 出库触发器：自动扣减库存
- 数据保护触发器：防止非法操作

### 4. 04_create_procedures.sql
- 创建存储过程实现统计功能
- 各类教材统计
- 按日期范围统计
- 库存预警
- 单号自动生成

### 5. 05_insert_sample_data.sql
- 插入示例数据用于测试
- 包括出版社、教材类型、教材、用户等基础数据
- 包括订购、入库、领用等业务数据

### 6. 06_test_queries.sql
- 测试查询语句
- 验证触发器和存储过程功能
- 复杂查询示例

### 7. 07_create_views.sql
- 创建数据库视图
- `v_textbook_detail`：教材详情视图（整合教材、出版社、类型、库存信息）
- `v_inventory_warning`：库存预警视图（展示库存异常的教材）

## 数据库表结构说明

### 核心表

1. **publisher（出版社表）**
   - 管理出版社信息
   - 包含联系方式等

2. **textbook_type（教材类型表）**
   - 教材分类管理
   - 支持层级分类

3. **textbook（教材表）**
   - 教材基本信息
   - ISBN书号格式约束：必须以ISBN开头，后跟10位数字

4. **purchase_order（订购表）**
   - 教材订购管理
   - 订单状态追踪

5. **stock_in（入库表）**
   - 教材入库管理
   - 质量检验记录

6. **requisition（领用表）**
   - 教材领用管理
   - 审批流程控制

7. **inventory（库存表）**
   - 实时库存数量
   - 库存预警设置

8. **user（用户表）**
   - 系统用户管理
   - 角色权限控制

## 特殊功能实现

### 1. ISBN格式约束
```sql
CONSTRAINT chk_isbn CHECK (isbn REGEXP '^ISBN[0-9]{10}$')
```

### 2. 自动库存管理触发器
- `trg_stock_in_after_insert`: 入库时自动增加库存
- `trg_requisition_after_update`: 发放时自动减少库存
- `trg_stock_in_before_delete`: 删除入库记录时回退库存

### 3. 统计存储过程
- `sp_statistics_by_type()`: 按类型统计
- `sp_statistics_by_textbook(textbook_id)`: 按教材统计
- `sp_statistics_by_date_range(start_date, end_date)`: 按日期范围统计
- `sp_inventory_warning()`: 库存预警查询
- `sp_statistics_by_publisher()`: 按出版社统计

### 4. 数据库视图
- `v_textbook_detail`: 教材详情视图，整合教材、出版社、类型和库存信息
- `v_inventory_warning`: 库存预警视图，展示库存异常（不足或过多）的教材

### 5. 单号生成存储过程
- `sp_generate_order_no()`: 生成订单编号
- `sp_generate_stock_in_no()`: 生成入库单号
- `sp_generate_requisition_no()`: 生成领用单号

## 参照完整性约束

所有外键都设置了适当的约束：
- `ON DELETE RESTRICT`: 有引用时禁止删除
- `ON UPDATE CASCADE`: 主键更新时级联更新
- `ON DELETE SET NULL`: 删除时设置为NULL（用于可选外键）

## 注意事项

1. 执行脚本前请确保MySQL版本 >= 5.7
2. 触发器中使用了 SIGNAL 语句进行错误处理
3. ISBN格式使用正则表达式约束：`^ISBN[0-9]{10}$`
4. 所有时间字段使用 TIMESTAMP 自动更新
5. 字符集统一使用 utf8mb4 支持中文

## 测试方法

执行 `06_test_queries.sql` 中的查询语句，验证：
- ✅ 表结构正确创建
- ✅ 外键约束生效
- ✅ 触发器自动更新库存
- ✅ 存储过程正确统计数据
- ✅ ISBN格式约束生效

## 常见问题

### 1. 触发器执行失败
- 检查MySQL版本是否支持触发器
- 确认表结构完整创建

### 2. ISBN约束不生效
- MySQL 8.0.16+ 支持 CHECK 约束
- 低版本可使用触发器替代

### 3. 字符集问题
- 确保数据库和表都使用 utf8mb4
- 连接时指定字符集

## 数据库架构图

```
publisher (出版社) ─────┐
                       │
textbook_type (类型) ──┼─→ textbook (教材) ─┬─→ inventory (库存)
                       │                    │
                       │                    ├─→ purchase_order (订购) ─→ stock_in (入库)
                       │                    │
                       │                    └─→ requisition (领用)
                       │
user (用户) ───────────┘
```

