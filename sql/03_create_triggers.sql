-- =============================================
-- 高校教材管理系统 - 触发器创建脚本
-- =============================================

USE textbook_management;

-- =============================================
-- 触发器1：教材入库时自动更新库存
-- =============================================
DELIMITER $$

CREATE TRIGGER trg_stock_in_after_insert
AFTER INSERT ON stock_in
FOR EACH ROW
BEGIN
    -- 声明变量，保存计算结果
    DECLARE v_new_arrived INT; -- 新的“已到货数量”
    DECLARE v_order_quantity INT;
    
    -- 先获取订单信息，计算新的已到货数量
    SELECT arrived_quantity + NEW.actual_quantity, order_quantity
    INTO v_new_arrived, v_order_quantity
    FROM purchase_order 
    WHERE order_id = NEW.order_id;
    
    -- 更新库存表
    IF EXISTS (SELECT 1 FROM inventory WHERE textbook_id = NEW.textbook_id) THEN
        UPDATE inventory 
        SET 
            current_quantity = current_quantity + NEW.actual_quantity,
            total_in_quantity = total_in_quantity + NEW.actual_quantity,
            last_in_date = NEW.stock_in_date,
            updated_at = CURRENT_TIMESTAMP
        WHERE textbook_id = NEW.textbook_id;
    ELSE
        INSERT INTO inventory (textbook_id, current_quantity, total_in_quantity, last_in_date)
        VALUES (NEW.textbook_id, NEW.actual_quantity, NEW.actual_quantity, NEW.stock_in_date);
    END IF;
    
    -- 更新订单表（使用预先计算好的变量，避免MySQL在同一UPDATE中的值覆盖问题）
    UPDATE purchase_order 
    SET 
        arrived_quantity = v_new_arrived,
        order_status = CASE 
            WHEN v_new_arrived >= v_order_quantity THEN '已到货'
            ELSE '部分到货'
        END,
        updated_at = CURRENT_TIMESTAMP
    WHERE order_id = NEW.order_id;
END$$

DELIMITER ;

-- =============================================
-- 触发器2：删除入库记录时回退库存（可选，用于数据修正）
-- =============================================
DELIMITER $$

CREATE TRIGGER trg_stock_in_before_delete
BEFORE DELETE ON stock_in
FOR EACH ROW
BEGIN
    -- 检查库存是否充足回退
    IF EXISTS (
        SELECT 1 FROM inventory 
        WHERE textbook_id = OLD.textbook_id 
        AND current_quantity >= OLD.actual_quantity
    ) THEN
        -- 回退库存数量
        UPDATE inventory 
        SET 
            current_quantity = current_quantity - OLD.actual_quantity,
            total_in_quantity = total_in_quantity - OLD.actual_quantity,
            updated_at = CURRENT_TIMESTAMP
        WHERE textbook_id = OLD.textbook_id;
        
        -- 回退订单到货数量
        UPDATE purchase_order 
        SET 
            arrived_quantity = GREATEST(0, arrived_quantity - OLD.actual_quantity),
            order_status = CASE 
                WHEN GREATEST(0, arrived_quantity - OLD.actual_quantity) = 0 THEN '已订购'
                WHEN GREATEST(0, arrived_quantity - OLD.actual_quantity) < order_quantity THEN '部分到货'
                ELSE order_status
            END,
            updated_at = CURRENT_TIMESTAMP
        WHERE order_id = OLD.order_id;
    ELSE
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = '库存数量不足，无法删除入库记录';
    END IF;
END$$

DELIMITER ;

-- =============================================
-- 触发器3：教材信息初始化库存记录
-- =============================================
DELIMITER $$

CREATE TRIGGER trg_textbook_after_insert
AFTER INSERT ON textbook
FOR EACH ROW
BEGIN
    -- 为新添加的教材自动创建库存记录
    INSERT INTO inventory (textbook_id, current_quantity, total_in_quantity, total_out_quantity)
    VALUES (NEW.textbook_id, 0, 0, 0);
END$$

DELIMITER ;

-- =============================================
-- 触发器4：检查订单状态（防止已完成的订单被修改）
-- =============================================
DELIMITER $$

CREATE TRIGGER trg_purchase_order_before_update
BEFORE UPDATE ON purchase_order
FOR EACH ROW
BEGIN
    -- 如果订单状态为"已取消"，不允许修改状态
    IF OLD.order_status = '已取消' AND NEW.order_status != '已取消' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = '已取消的订单不能修改状态';
    END IF;
    
    -- 如果订单状态为"已发放"，不允许修改状态
    IF OLD.order_status = '已发放' AND NEW.order_status != '已发放' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = '已发放的订单不能修改状态';
    END IF;
END$$

DELIMITER ;

