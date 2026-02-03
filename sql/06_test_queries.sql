-- =============================================
-- 高校教材管理系统 - 测试查询脚本
-- =============================================

USE textbook_management;

-- =============================================
-- 1. 测试基本查询
-- =============================================

-- 查询所有教材信息
SELECT 
    t.textbook_id,
    t.isbn,
    t.textbook_name,
    t.author,
    p.publisher_name,
    tt.type_name,
    t.price,
    i.current_quantity AS '库存数量'
FROM textbook t
LEFT JOIN publisher p ON t.publisher_id = p.publisher_id
LEFT JOIN textbook_type tt ON t.type_id = tt.type_id
LEFT JOIN inventory i ON t.textbook_id = i.textbook_id
WHERE t.status = 1;

-- 查询当前库存情况
SELECT 
    t.textbook_name,
    t.isbn,
    i.current_quantity AS '当前库存',
    i.total_in_quantity AS '累计入库',
    i.total_out_quantity AS '累计出库',
    i.min_quantity AS '最低预警值'
FROM inventory i
INNER JOIN textbook t ON i.textbook_id = t.textbook_id
ORDER BY i.current_quantity;

-- =============================================
-- 2. 测试存储过程
-- =============================================

-- 调用存储过程：统计各类教材情况
CALL sp_statistics_by_type();

-- 调用存储过程：按出版社统计
CALL sp_statistics_by_publisher();

-- 调用存储过程：库存预警查询
CALL sp_inventory_warning();

-- 调用存储过程：查询指定教材统计信息（教材ID=1）
CALL sp_statistics_by_textbook(1);

-- 调用存储过程：按日期范围统计（2024年1月）
CALL sp_statistics_by_date_range('2024-01-01', '2024-01-31');

-- 调用存储过程：生成订单编号
CALL sp_generate_order_no(@new_order_no);
SELECT @new_order_no AS '新订单编号';

-- 调用存储过程：生成入库单号
CALL sp_generate_stock_in_no(@new_stock_in_no);
SELECT @new_stock_in_no AS '新入库单号';

-- 调用存储过程：生成领用单号
CALL sp_generate_requisition_no(@new_requisition_no);
SELECT @new_requisition_no AS '新领用单号';

-- =============================================
-- 3. 测试复杂查询
-- =============================================

-- 查询订单完成情况
SELECT 
    po.order_no AS '订单编号',
    t.textbook_name AS '教材名称',
    po.order_quantity AS '订购数量',
    po.arrived_quantity AS '已到货数量',
    po.order_quantity - po.arrived_quantity AS '未到货数量',
    po.order_status AS '订单状态',
    po.order_date AS '订购日期'
FROM purchase_order po
INNER JOIN textbook t ON po.textbook_id = t.textbook_id
ORDER BY po.order_date DESC;

-- 查询各部门领用情况
SELECT 
    r.department AS '部门',
    COUNT(*) AS '领用次数',
    SUM(r.requisition_quantity) AS '申请数量',
    SUM(r.actual_quantity) AS '实际发放数量',
    SUM(CASE WHEN r.approval_status = '已发放' THEN 1 ELSE 0 END) AS '已发放次数',
    SUM(CASE WHEN r.approval_status = '待审批' THEN 1 ELSE 0 END) AS '待审批次数'
FROM requisition r
GROUP BY r.department
ORDER BY SUM(r.actual_quantity) DESC;

-- 查询最近7天的入库情况
SELECT 
    si.stock_in_date AS '入库日期',
    COUNT(*) AS '入库单数',
    SUM(si.actual_quantity) AS '入库总数量'
FROM stock_in si
WHERE si.stock_in_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
GROUP BY si.stock_in_date
ORDER BY si.stock_in_date DESC;

-- 查询教材价格统计
SELECT 
    tt.type_name AS '教材类型',
    COUNT(*) AS '教材数量',
    MIN(t.price) AS '最低价',
    MAX(t.price) AS '最高价',
    AVG(t.price) AS '平均价',
    SUM(t.price * i.current_quantity) AS '库存总价值'
FROM textbook t
INNER JOIN textbook_type tt ON t.type_id = tt.type_id
LEFT JOIN inventory i ON t.textbook_id = i.textbook_id
WHERE t.status = 1
GROUP BY tt.type_name
ORDER BY SUM(t.price * i.current_quantity) DESC;

-- 查询热门教材（按领用次数排序）
SELECT 
    t.textbook_name AS '教材名称',
    t.author AS '作者',
    p.publisher_name AS '出版社',
    COUNT(r.requisition_id) AS '领用次数',
    SUM(r.actual_quantity) AS '累计发放数量',
    i.current_quantity AS '当前库存'
FROM textbook t
LEFT JOIN publisher p ON t.publisher_id = p.publisher_id
LEFT JOIN requisition r ON t.textbook_id = r.textbook_id AND r.approval_status = '已发放'
LEFT JOIN inventory i ON t.textbook_id = i.textbook_id
WHERE t.status = 1
GROUP BY t.textbook_id, t.textbook_name, t.author, p.publisher_name, i.current_quantity
HAVING COUNT(r.requisition_id) > 0
ORDER BY SUM(r.actual_quantity) DESC
LIMIT 10;

-- =============================================
-- 4. 测试ISBN格式约束
-- =============================================

-- 以下插入应该失败（ISBN格式不正确）
-- INSERT INTO textbook (isbn, textbook_name, author, publisher_id, type_id, price) 
-- VALUES ('ISBN123', '测试教材', '测试作者', 1, 1, 50.00);

-- 以下插入应该成功（ISBN格式正确）
-- INSERT INTO textbook (isbn, textbook_name, author, publisher_id, type_id, price) 
-- VALUES ('ISBN1234567890', '测试教材', '测试作者', 1, 1, 50.00);

-- =============================================
-- 5. 查看触发器和存储过程
-- =============================================

-- 查看所有触发器
SHOW TRIGGERS;

-- 查看所有存储过程
SHOW PROCEDURE STATUS WHERE Db = 'textbook_management';

-- =============================================
-- 6. 数据完整性测试
-- =============================================

-- 查看外键约束
SELECT 
    TABLE_NAME,
    COLUMN_NAME,
    CONSTRAINT_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'textbook_management'
AND REFERENCED_TABLE_NAME IS NOT NULL;

