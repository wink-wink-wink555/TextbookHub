-- =============================================
-- 高校教材管理系统 - 数据表创建脚本
-- =============================================

USE textbook_management;

-- =============================================
-- 1. 出版社表 (publisher)
-- =============================================
CREATE TABLE IF NOT EXISTS publisher (
    publisher_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '出版社ID',
    publisher_name VARCHAR(100) NOT NULL UNIQUE COMMENT '出版社名称',
    contact_person VARCHAR(50) COMMENT '联系人',
    contact_phone VARCHAR(20) COMMENT '联系电话',
    address VARCHAR(200) COMMENT '地址',
    email VARCHAR(100) COMMENT '邮箱',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    status TINYINT DEFAULT 1 COMMENT '状态：1-正常，0-停用'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='出版社信息表';

-- =============================================
-- 2. 教材类型表 (textbook_type)
-- =============================================
CREATE TABLE IF NOT EXISTS textbook_type (
    type_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '类型ID',
    type_name VARCHAR(50) NOT NULL UNIQUE COMMENT '类型名称',
    type_code VARCHAR(20) NOT NULL UNIQUE COMMENT '类型编码',
    description TEXT COMMENT '类型描述',
    parent_id INT DEFAULT NULL COMMENT '父类型ID（用于分级分类）',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    status TINYINT DEFAULT 1 COMMENT '状态：1-正常，0-停用',
    FOREIGN KEY (parent_id) REFERENCES textbook_type(type_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='教材类型表';

-- =============================================
-- 3. 教材表 (textbook)
-- =============================================
CREATE TABLE IF NOT EXISTS textbook (
    textbook_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '教材ID',
    isbn VARCHAR(20) NOT NULL UNIQUE COMMENT '国际标准书号',
    textbook_name VARCHAR(200) NOT NULL COMMENT '教材名称',
    author VARCHAR(100) COMMENT '作者',
    publisher_id INT NOT NULL COMMENT '出版社ID',
    type_id INT NOT NULL COMMENT '教材类型ID',
    edition VARCHAR(20) COMMENT '版次',
    publication_date DATE COMMENT '出版日期',
    price DECIMAL(10, 2) NOT NULL COMMENT '单价',
    description TEXT COMMENT '教材描述',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    status TINYINT DEFAULT 1 COMMENT '状态：1-正常，0-停用',
    CONSTRAINT chk_isbn CHECK (isbn REGEXP '^ISBN[0-9]{10}$'),
    FOREIGN KEY (publisher_id) REFERENCES publisher(publisher_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (type_id) REFERENCES textbook_type(type_id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='教材信息表';

-- =============================================
-- 4. 订购表 (purchase_order)
-- =============================================
CREATE TABLE IF NOT EXISTS purchase_order (
    order_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '订单ID',
    order_no VARCHAR(50) NOT NULL UNIQUE COMMENT '订单编号',
    textbook_id INT NOT NULL COMMENT '教材ID',
    order_quantity INT NOT NULL COMMENT '订购数量',
    order_date DATE NOT NULL COMMENT '订购日期',
    expected_date DATE COMMENT '预计到货日期',
    order_person VARCHAR(50) COMMENT '订购人',
    order_status ENUM('待审核', '已审核', '已订购', '部分到货', '已到货', '已发放', '已取消') DEFAULT '待审核' COMMENT '订单状态',
    arrived_quantity INT DEFAULT 0 COMMENT '已到货数量',
    remarks TEXT COMMENT '备注',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    CONSTRAINT chk_order_quantity CHECK (order_quantity > 0),
    CONSTRAINT chk_arrived_quantity CHECK (arrived_quantity >= 0 AND arrived_quantity <= order_quantity),
    FOREIGN KEY (textbook_id) REFERENCES textbook(textbook_id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='教材订购表';

-- =============================================
-- 5. 入库表 (stock_in)
-- =============================================
CREATE TABLE IF NOT EXISTS stock_in (
    stock_in_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '入库ID',
    stock_in_no VARCHAR(50) NOT NULL UNIQUE COMMENT '入库单号',
    order_id INT NOT NULL COMMENT '订单ID',
    textbook_id INT NOT NULL COMMENT '教材ID',
    stock_in_quantity INT NOT NULL COMMENT '入库数量',
    stock_in_date DATE NOT NULL COMMENT '入库日期',
    warehouse_person VARCHAR(50) COMMENT '仓库管理员',
    quality_status ENUM('合格', '部分合格', '不合格') DEFAULT '合格' COMMENT '质量状态',
    actual_quantity INT NOT NULL COMMENT '实际入库数量',
    remarks TEXT COMMENT '备注',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    CONSTRAINT chk_stock_in_quantity CHECK (stock_in_quantity > 0),
    CONSTRAINT chk_actual_quantity CHECK (actual_quantity >= 0 AND actual_quantity <= stock_in_quantity),
    FOREIGN KEY (order_id) REFERENCES purchase_order(order_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (textbook_id) REFERENCES textbook(textbook_id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='教材入库表';

-- =============================================
-- 6. 库存表 (inventory)
-- =============================================
CREATE TABLE IF NOT EXISTS inventory (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '库存ID',
    textbook_id INT NOT NULL UNIQUE COMMENT '教材ID',
    current_quantity INT DEFAULT 0 COMMENT '当前库存数量',
    total_in_quantity INT DEFAULT 0 COMMENT '累计入库数量',
    total_out_quantity INT DEFAULT 0 COMMENT '累计出库数量',
    min_quantity INT DEFAULT 10 COMMENT '最低库存预警值',
    max_quantity INT DEFAULT 1000 COMMENT '最高库存预警值',
    last_in_date DATE COMMENT '最后入库日期',
    last_out_date DATE COMMENT '最后出库日期',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    CONSTRAINT chk_current_quantity CHECK (current_quantity >= 0),
    FOREIGN KEY (textbook_id) REFERENCES textbook(textbook_id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='教材库存表';

-- =============================================
-- 7. 用户表 (user) - 用于系统登录和权限管理
-- =============================================
CREATE TABLE IF NOT EXISTS user (
    user_id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    password VARCHAR(255) NOT NULL COMMENT '密码（加密存储）',
    real_name VARCHAR(50) COMMENT '真实姓名',
    role ENUM('管理员', '仓库管理员', '教师', '普通用户') DEFAULT '普通用户' COMMENT '用户角色',
    department VARCHAR(100) COMMENT '所属部门',
    email VARCHAR(100) COMMENT '邮箱',
    phone VARCHAR(20) COMMENT '电话',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    last_login TIMESTAMP NULL COMMENT '最后登录时间',
    status TINYINT DEFAULT 1 COMMENT '状态：1-正常，0-停用'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统用户表';

-- =============================================
-- 创建索引以提高查询性能
-- =============================================

-- 教材表索引
CREATE INDEX idx_textbook_name ON textbook(textbook_name);
CREATE INDEX idx_textbook_publisher ON textbook(publisher_id);
CREATE INDEX idx_textbook_type ON textbook(type_id);

-- 订购表索引
CREATE INDEX idx_order_date ON purchase_order(order_date);
CREATE INDEX idx_order_status ON purchase_order(order_status);
CREATE INDEX idx_order_textbook ON purchase_order(textbook_id);

-- 入库表索引
CREATE INDEX idx_stock_in_date ON stock_in(stock_in_date);
CREATE INDEX idx_stock_in_order ON stock_in(order_id);
CREATE INDEX idx_stock_in_textbook ON stock_in(textbook_id);

-- 库存表索引
CREATE INDEX idx_inventory_quantity ON inventory(current_quantity);

