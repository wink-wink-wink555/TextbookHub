-- =============================================
-- 高校教材管理系统 - 视图创建脚本
-- =============================================

USE textbook_management;

-- =============================================
-- 视图1：教材详情视图 (v_textbook_detail)
-- 功能：整合教材基本信息、出版社、类型及库存信息
-- 使用场景：教材列表展示、教材详情查询
-- 【注意】此视图为扩展功能，当前项目中未被调用
-- 可供未来优化使用，或直接在MySQL中查询
-- =============================================
DROP VIEW IF EXISTS v_textbook_detail;

CREATE VIEW v_textbook_detail AS
SELECT 
    t.textbook_id,
    t.isbn,
    t.textbook_name,
    t.author,
    t.edition,
    t.publication_date,
    t.price,
    t.description AS textbook_description,
    t.status AS textbook_status,
    t.created_at AS textbook_created_at,
    t.updated_at AS textbook_updated_at,
    -- 出版社信息
    p.publisher_id,
    p.publisher_name,
    p.contact_person AS publisher_contact,
    p.contact_phone AS publisher_phone,
    -- 教材类型信息
    tt.type_id,
    tt.type_name,
    tt.type_code,
    -- 库存信息
    COALESCE(i.inventory_id, NULL) AS inventory_id,
    COALESCE(i.current_quantity, 0) AS current_quantity,
    COALESCE(i.total_in_quantity, 0) AS total_in_quantity,
    COALESCE(i.total_out_quantity, 0) AS total_out_quantity,
    COALESCE(i.min_quantity, 10) AS min_quantity,
    COALESCE(i.max_quantity, 1000) AS max_quantity,
    i.last_in_date,
    i.last_out_date,
    -- 计算库存价值
    COALESCE(t.price * i.current_quantity, 0) AS inventory_value,
    -- 库存状态判断
    CASE 
        WHEN i.inventory_id IS NULL THEN '无库存记录'
        WHEN i.current_quantity < COALESCE(i.min_quantity, 10) THEN '库存不足'
        WHEN i.current_quantity > COALESCE(i.max_quantity, 1000) THEN '库存过多'
        ELSE '正常'
    END AS stock_status
FROM 
    textbook t
    LEFT JOIN publisher p ON t.publisher_id = p.publisher_id
    LEFT JOIN textbook_type tt ON t.type_id = tt.type_id
    LEFT JOIN inventory i ON t.textbook_id = i.textbook_id
WHERE 
    t.status = 1;

-- =============================================
-- 视图2：库存预警视图 (v_inventory_warning)
-- 功能：展示库存异常（不足或过多）的教材信息
-- 使用场景：库存预警查询、仪表盘预警展示
-- =============================================
DROP VIEW IF EXISTS v_inventory_warning;

CREATE VIEW v_inventory_warning AS
SELECT 
    t.textbook_id,
    t.isbn,
    t.textbook_name,
    t.author,
    t.price,
    p.publisher_id,
    p.publisher_name,
    tt.type_id,
    tt.type_name,
    i.inventory_id,
    i.current_quantity,
    i.min_quantity,
    i.max_quantity,
    i.total_in_quantity,
    i.total_out_quantity,
    i.last_in_date,
    i.last_out_date,
    -- 库存价值
    COALESCE(t.price * i.current_quantity, 0) AS inventory_value,
    -- 库存状态
    CASE 
        WHEN i.current_quantity < i.min_quantity THEN '库存不足'
        WHEN i.current_quantity > i.max_quantity THEN '库存过多'
        ELSE '正常'
    END AS warning_status,
    -- 预警级别（用于排序，数值越小越紧急）
    CASE 
        WHEN i.current_quantity < i.min_quantity THEN 1
        WHEN i.current_quantity > i.max_quantity THEN 2
        ELSE 3
    END AS warning_level,
    -- 缺口/超量数量
    CASE 
        WHEN i.current_quantity < i.min_quantity THEN i.min_quantity - i.current_quantity
        WHEN i.current_quantity > i.max_quantity THEN i.current_quantity - i.max_quantity
        ELSE 0
    END AS gap_quantity
FROM 
    inventory i
    INNER JOIN textbook t ON i.textbook_id = t.textbook_id
    LEFT JOIN publisher p ON t.publisher_id = p.publisher_id
    LEFT JOIN textbook_type tt ON t.type_id = tt.type_id
WHERE 
    t.status = 1
    AND (i.current_quantity < i.min_quantity OR i.current_quantity > i.max_quantity)
ORDER BY 
    warning_level ASC,
    gap_quantity DESC;

-- =============================================
-- 验证视图创建成功
-- =============================================

-- 查看教材详情视图结构
DESCRIBE v_textbook_detail;

-- 查看库存预警视图结构
DESCRIBE v_inventory_warning;

-- 测试查询：教材详情视图
SELECT 
    textbook_id,
    isbn,
    textbook_name,
    publisher_name,
    type_name,
    current_quantity,
    stock_status
FROM v_textbook_detail
LIMIT 5;

-- 测试查询：库存预警视图
SELECT 
    textbook_id,
    isbn,
    textbook_name,
    publisher_name,
    current_quantity,
    min_quantity,
    max_quantity,
    warning_status,
    gap_quantity
FROM v_inventory_warning;

