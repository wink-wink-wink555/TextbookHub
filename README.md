# 📚 TextbookHub - 高校教材管理系统

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask Version](https://img.shields.io/badge/flask-3.0.0-green.svg)
![MySQL Version](https://img.shields.io/badge/mysql-5.7+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)

**一个功能完善的高校教材管理系统 | 数据库原理课程设计项目**

[功能特性](#-功能特性) • [技术栈](#-技术栈) • [快速开始](#-快速开始) • [系统架构](#-系统架构) • [API文档](#-api文档)

</div>

---

## 📋 项目简介

TextbookHub 是一个基于 Flask + MySQL 开发的高校教材管理系统，专为数据库原理课程设计打造。系统实现了教材的全生命周期管理，包括订购、入库、库存管理、发放和统计分析等核心功能。

### ✨ 项目亮点

- ✅ **完整的数据库设计**：包含触发器、存储过程、视图、索引等高级特性
- ✅ **RESTful API 架构**：前后端分离，接口规范
- ✅ **JWT 身份认证**：安全的用户认证和授权机制
- ✅ **自动化库存管理**：通过数据库触发器实现库存自动更新
- ✅ **统计分析功能**：多维度数据统计和可视化
- ✅ **规范的代码结构**：采用工厂模式、蓝图、DAO模式等最佳实践

---

## 🎯 功能特性

### 核心业务功能

| 模块 | 功能描述 |
|------|---------|
| 📖 **教材管理** | 教材信息的增删改查、ISBN格式校验、分类管理 |
| 🏢 **出版社管理** | 出版社信息维护、联系人管理 |
| 📦 **订购管理** | 订单创建、状态追踪、自动生成订单编号 |
| 📥 **入库管理** | 入库登记、质量检验、自动更新库存 |
| 📊 **库存管理** | 实时库存查询、库存预警、库存盘点 |
| 📝 **领用管理** | 领用申请、审批流程、自动扣减库存 |
| 📈 **统计分析** | 多维度统计（按类型、出版社、时间段等） |
| 👤 **用户管理** | 用户认证、角色权限、密码加密 |

### 数据库高级特性

- **触发器 (Triggers)**
  - 入库自动更新库存和订单状态
  - 领用发放自动扣减库存
  - 数据删除保护机制

- **存储过程 (Stored Procedures)**
  - `sp_statistics_by_type()` - 按类型统计
  - `sp_statistics_by_publisher()` - 按出版社统计
  - `sp_statistics_by_textbook()` - 按教材统计
  - `sp_generate_order_no()` - 自动生成订单编号
  - `sp_generate_stock_in_no()` - 自动生成入库单号

- **视图 (Views)**
  - `v_textbook_detail` - 教材详情综合视图
  - `v_inventory_warning` - 库存预警视图

- **约束与索引**
  - ISBN格式正则校验：`^ISBN[0-9]{10}$`
  - 外键级联约束
  - 复合索引优化查询性能

---

## 🛠 技术栈

### 后端技术

| 技术 | 版本 | 说明 |
|------|------|------|
| Python | 3.8+ | 编程语言 |
| Flask | 3.0.0 | Web 框架 |
| SQLAlchemy | 2.0.23 | ORM 框架 |
| Flask-JWT-Extended | 4.6.0 | JWT 认证 |
| PyMySQL | 1.1.0 | MySQL 驱动 |
| Marshmallow | 3.20.1 | 数据序列化 |
| Bcrypt | 4.1.2 | 密码加密 |

### 数据库

- **MySQL 5.7+** - 关系型数据库
- 支持触发器、存储过程、视图等高级特性
- utf8mb4 字符集，完整支持中文和特殊字符

### 前端技术

- HTML5 + CSS3
- JavaScript (ES6+)
- Bootstrap 5 (UI框架)
- Chart.js (数据可视化)

---

## 🚀 快速开始

### 环境要求

- Python 3.8 或更高版本
- MySQL 5.7 或更高版本
- pip (Python 包管理器)

### 1. 克隆项目

```bash
git clone https://github.com/wink-wink-wink555/TextbookHub.git
cd TextbookHub
```

### 2. 创建虚拟环境

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

创建 `.env` 文件（参考 `.env.example`）：

```env
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=textbook_management

# Flask配置
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
FLASK_ENV=development

# JWT过期时间（秒）
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=2592000
```

### 5. 初始化数据库

**按顺序执行 SQL 脚本**（使用 MySQL Workbench 或命令行）：

```bash
# 1. 创建数据库
mysql -u root -p < sql/01_create_database.sql

# 2. 创建表结构
mysql -u root -p < sql/02_create_tables.sql

# 3. 创建触发器
mysql -u root -p < sql/03_create_triggers.sql

# 4. 创建存储过程
mysql -u root -p < sql/04_create_procedures.sql

# 5. 插入示例数据
mysql -u root -p < sql/05_insert_sample_data.sql

# 6. 创建视图
mysql -u root -p < sql/07_create_views.sql
```

详细说明请查看 [sql/README.md](sql/README.md)

### 6. 创建系统用户

```bash
python create_users.py
```

默认用户账号：
- **管理员**: `admin` / `admin123`
- **普通用户**: `user` / `user123`

### 7. 启动应用

```bash
python main.py
```

应用将在 `http://localhost:5000` 启动

### 8. 访问系统

- **前端页面**: http://localhost:5000
- **API文档**: http://localhost:5000/api/health
- **登录页面**: http://localhost:5000 (自动跳转)

---

## 📂 项目结构

```
TextbookHub/
├── app/                        # 应用主目录
│   ├── __init__.py            # 应用工厂
│   ├── extensions.py          # Flask扩展初始化
│   ├── api/                   # API蓝图
│   │   └── v1/               # API v1版本
│   │       ├── auth.py       # 认证接口
│   │       ├── textbook.py   # 教材接口
│   │       ├── publisher.py  # 出版社接口
│   │       ├── purchase_order.py  # 订购接口
│   │       ├── stock_in.py   # 入库接口
│   │       └── statistics.py # 统计接口
│   ├── dao/                   # 数据访问层
│   │   ├── base_dao.py       # 基础DAO
│   │   ├── textbook_dao.py   # 教材DAO
│   │   └── ...               # 其他DAO
│   ├── models/                # 数据模型
│   │   ├── base.py           # 基础模型
│   │   ├── textbook.py       # 教材模型
│   │   └── ...               # 其他模型
│   ├── schemas/               # 序列化模式
│   │   ├── textbook_schema.py
│   │   └── ...
│   ├── services/              # 业务逻辑层
│   │   ├── auth_service.py   # 认证服务
│   │   ├── textbook_service.py
│   │   └── ...
│   ├── utils/                 # 工具类
│   │   ├── decorators.py     # 装饰器
│   │   ├── exceptions.py     # 自定义异常
│   │   ├── response.py       # 响应封装
│   │   └── validators.py     # 数据校验
│   ├── middleware/            # 中间件
│   │   └── error_handler.py  # 错误处理
│   ├── static/                # 静态文件
│   │   ├── css/
│   │   └── js/
│   └── templates/             # HTML模板
│       ├── login.html
│       ├── dashboard.html
│       └── ...
├── sql/                       # SQL脚本
│   ├── README.md             # SQL脚本说明
│   ├── 01_create_database.sql
│   ├── 02_create_tables.sql
│   ├── 03_create_triggers.sql
│   ├── 04_create_procedures.sql
│   ├── 05_insert_sample_data.sql
│   ├── 06_test_queries.sql
│   └── 07_create_views.sql
├── config.py                  # 配置文件
├── main.py                    # 应用入口
├── create_users.py            # 用户创建脚本
├── requirements.txt           # Python依赖
├── .env.example              # 环境变量示例
├── .gitignore                # Git忽略规则
└── README.md                 # 项目说明
```

---

## 🔌 API 文档

### 基础URL

```
http://localhost:5000/api/v1
```

### 认证接口

#### 用户登录

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

**响应示例**：

```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user": {
      "user_id": 1,
      "username": "admin",
      "role": "admin"
    }
  }
}
```

### 教材接口

#### 获取教材列表

```http
GET /api/v1/textbooks?page=1&page_size=20
Authorization: Bearer {access_token}
```

#### 创建教材

```http
POST /api/v1/textbooks
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "isbn": "ISBN1234567890",
  "textbook_name": "数据库系统概论",
  "author": "王珊",
  "publisher_id": 1,
  "type_id": 1,
  "price": 45.00,
  "edition": "第5版"
}
```

#### 更新教材

```http
PUT /api/v1/textbooks/{id}
Authorization: Bearer {access_token}
Content-Type: application/json
```

#### 删除教材

```http
DELETE /api/v1/textbooks/{id}
Authorization: Bearer {access_token}
```

### 统计接口

#### 按类型统计

```http
GET /api/v1/statistics/by-type
Authorization: Bearer {access_token}
```

#### 按出版社统计

```http
GET /api/v1/statistics/by-publisher
Authorization: Bearer {access_token}
```

#### 库存预警

```http
GET /api/v1/statistics/inventory-warning
Authorization: Bearer {access_token}
```

更多接口详情请参考源码中的 `app/api/v1/` 目录。

---

## 🗄 数据库设计

### ER图概览

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│  Publisher  │◄────────┤   Textbook   │────────►│ TextbookType│
│  (出版社)    │         │   (教材)      │         │  (教材类型)  │
└─────────────┘         └──────┬───────┘         └─────────────┘
                              │
                    ┌─────────┼─────────┐
                    │         │         │
                    ▼         ▼         ▼
            ┌───────────┐ ┌──────────┐ ┌───────────┐
            │PurchaseOrder│ │StockIn  │ │Inventory  │
            │  (订购)     │ │ (入库)   │ │ (库存)    │
            └───────────┘ └──────────┘ └───────────┘
```

### 核心数据表

| 表名 | 说明 | 主要字段 |
|------|------|---------|
| `publisher` | 出版社 | publisher_id, publisher_name, contact |
| `textbook_type` | 教材类型 | type_id, type_name, type_code |
| `textbook` | 教材 | textbook_id, isbn, textbook_name, price |
| `purchase_order` | 订购单 | order_id, order_no, textbook_id, quantity |
| `stock_in` | 入库单 | stock_in_id, order_id, actual_quantity |
| `inventory` | 库存 | inventory_id, textbook_id, current_quantity |
| `requisition` | 领用单 | requisition_id, textbook_id, quantity |
| `user` | 用户 | user_id, username, password_hash, role |

详细的数据库设计文档请查看 [sql/README.md](sql/README.md)

---

## 🧪 测试

### 运行测试脚本

```bash
# 测试数据库功能
mysql -u root -p < sql/06_test_queries.sql
```

### 功能测试清单

- [x] 用户登录认证
- [x] 教材CRUD操作
- [x] 订购单创建和状态追踪
- [x] 入库自动更新库存（触发器）
- [x] 领用发放自动扣减库存（触发器）
- [x] 多维度统计分析（存储过程）
- [x] 库存预警功能
- [x] ISBN格式校验
- [x] 数据完整性约束

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

### 代码规范

- Python 代码遵循 PEP 8 规范
- SQL 脚本使用大写关键字
- 注释使用中文，代码使用英文
- 提交信息格式：`type: description`

---

## 📜 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 👨‍💻 作者

**wink-wink-wink555**

- GitHub: [wink-wink-wink555](https://github.com/wink-wink-wink555)
- Email: yfsun.jeff@gmail.com

---

## 🙏 致谢

- 感谢数据库原理课程提供的实践机会
- 感谢 Flask 和 SQLAlchemy 社区的优秀文档
- 感谢所有贡献者的支持

---

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 [Issue](https://github.com/wink-wink-wink555/TextbookHub/issues)
- 发送邮件至：yfsun.jeff@gmail.com

---

<div align="center">

**⭐ 如果这个项目对您有帮助，请给一个 Star！⭐**

Made with ❤️ by wink-wink-wink555 for Database Course Design

</div>


