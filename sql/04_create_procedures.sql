-- =============================================
-- 高校教材管理系统 - 存储过程创建脚本
-- =============================================

USE textbook_management;

-- =============================================
-- 存储过程1：统计各类教材的订购、到货和发放数量
-- =============================================
DELIMITER $$

CREATE PROCEDURE sp_statistics_by_type()
BEGIN
    SELECT 
        tt.type_id AS '类型ID',
        tt.type_name AS '教材类型',
        tt.type_code AS '类型编码',
        COUNT(DISTINCT t.textbook_id) AS '教材种类数',
        COALESCE(SUM(po.order_quantity), 0) AS '订购总数量',
        COALESCE(SUM(po.arrived_quantity), 0) AS '到货总数量',
        -- 只有当订单状态是 '已发放' 时，才把 arrived_quantity 算进去；否则算 0
        COALESCE(SUM(CASE WHEN po.order_status = '已发放' THEN po.arrived_quantity ELSE 0 END), 0) AS '发放总数量',
        COALESCE(SUM(i.current_quantity), 0) AS '当前库存总量'
    FROM 
        textbook_type tt
        LEFT JOIN textbook t ON tt.type_id = t.type_id AND t.status = 1
        LEFT JOIN purchase_order po ON t.textbook_id = po.textbook_id
        LEFT JOIN inventory i ON t.textbook_id = i.textbook_id
    WHERE 
        tt.status = 1
    GROUP BY 
        tt.type_id, tt.type_name, tt.type_code
    ORDER BY 
        tt.type_code;
END$$

DELIMITER ;

-- =============================================
-- 存储过程2：根据教材ID统计订购、到货和发放情况
-- =============================================
DELIMITER $$

CREATE PROCEDURE sp_statistics_by_textbook(IN p_textbook_id INT)
BEGIN
    SELECT 
        t.textbook_id AS '教材ID',
        t.isbn AS 'ISBN',
        t.textbook_name AS '教材名称',
        t.author AS '作者',
        p.publisher_name AS '出版社',
        tt.type_name AS '教材类型',
        COALESCE(SUM(po.order_quantity), 0) AS '订购总数量',
        COALESCE(SUM(po.arrived_quantity), 0) AS '到货总数量',
        COALESCE(SUM(CASE WHEN po.order_status = '已发放' THEN po.arrived_quantity ELSE 0 END), 0) AS '发放总数量',
        COALESCE(i.current_quantity, 0) AS '当前库存数量'
    FROM 
        textbook t
        LEFT JOIN publisher p ON t.publisher_id = p.publisher_id
        LEFT JOIN textbook_type tt ON t.type_id = tt.type_id
        LEFT JOIN purchase_order po ON t.textbook_id = po.textbook_id
        LEFT JOIN inventory i ON t.textbook_id = i.textbook_id
    WHERE 
        t.textbook_id = p_textbook_id
    GROUP BY 
        t.textbook_id, t.isbn, t.textbook_name, t.author, 
        p.publisher_name, tt.type_name, i.current_quantity;
END$$

DELIMITER ;


-- =============================================
-- 存储过程3：按出版社统计教材情况
-- =============================================
DELIMITER $$

CREATE PROCEDURE sp_statistics_by_publisher()
BEGIN
    SELECT 
        p.publisher_id AS '出版社ID',
        p.publisher_name AS '出版社名称',
        COUNT(DISTINCT t.textbook_id) AS '教材种类数',
        COALESCE(SUM(po.order_quantity), 0) AS '订购总数量',
        COALESCE(SUM(po.arrived_quantity), 0) AS '到货总数量',
        COALESCE(SUM(CASE WHEN po.order_status = '已发放' THEN po.arrived_quantity ELSE 0 END), 0) AS '发放总数量',
        COALESCE(SUM(i.current_quantity), 0) AS '当前库存总量'
    FROM 
        publisher p
        LEFT JOIN textbook t ON p.publisher_id = t.publisher_id AND t.status = 1
        LEFT JOIN purchase_order po ON t.textbook_id = po.textbook_id
        LEFT JOIN inventory i ON t.textbook_id = i.textbook_id
    WHERE 
        p.status = 1
    GROUP BY 
        p.publisher_id, p.publisher_name
    ORDER BY 
        p.publisher_name;
END$$

DELIMITER ;

-- =============================================
-- 存储过程4：生成订单编号
-- =============================================
DELIMITER $$

CREATE PROCEDURE sp_generate_order_no(OUT p_order_no VARCHAR(50))
BEGIN
    DECLARE v_date VARCHAR(8);
    DECLARE v_seq INT;
    
    -- 获取当前日期（YYYYMMDD格式）
    SET v_date = DATE_FORMAT(NOW(), '%Y%m%d');
    
    -- 获取今天的订单序号
    -- SUBSTRING(str, start)：从字符串第 start 位开始截取到末尾；
    -- CAST('0001' AS UNSIGNED)：把字符串 '0001' 转成整数 1
    -- 如果今天还没有任何订单，MAX(...) 返回 NULL，COALESCE(NULL, 0) → 返回 0
    SELECT COALESCE(MAX(CAST(SUBSTRING(order_no, 11) AS UNSIGNED)), 0) + 1
    INTO v_seq
    FROM purchase_order
    WHERE order_no LIKE CONCAT('PO', v_date, '%'); -- 拼接
    
    -- 生成订单编号：PO + YYYYMMDD + 4位序号
    SET p_order_no = CONCAT('PO', v_date, LPAD(v_seq, 4, '0'));
END$$

DELIMITER ;

-- =============================================
-- 存储过程5：生成入库单号
-- =============================================
DELIMITER $$

CREATE PROCEDURE sp_generate_stock_in_no(OUT p_stock_in_no VARCHAR(50))
BEGIN
    DECLARE v_date VARCHAR(8);
    DECLARE v_seq INT;
    
    SET v_date = DATE_FORMAT(NOW(), '%Y%m%d');
    
    SELECT COALESCE(MAX(CAST(SUBSTRING(stock_in_no, 11) AS UNSIGNED)), 0) + 1
    INTO v_seq
    FROM stock_in
    WHERE stock_in_no LIKE CONCAT('SI', v_date, '%');
    
    SET p_stock_in_no = CONCAT('SI', v_date, LPAD(v_seq, 4, '0'));
END$$

DELIMITER ;

