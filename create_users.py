"""
创建测试用户脚本
"""
import requests

BASE_URL = "http://localhost:5000/api/v1"

users = [
    {
        "username": "admin",
        "password": "admin123",
        "real_name": "系统管理员",
        "role": "管理员",
        "department": "教务处",
        "email": "admin@university.edu.cn",
        "phone": "13800000000"
    },
    {
        "username": "warehouse01",
        "password": "warehouse123",
        "real_name": "张管理",
        "role": "仓库管理员",
        "department": "图书馆",
        "email": "warehouse@university.edu.cn",
        "phone": "13800000001"
    },
    {
        "username": "teacher01",
        "password": "teacher123",
        "real_name": "李老师",
        "role": "教师",
        "department": "计算机学院",
        "email": "teacher01@university.edu.cn",
        "phone": "13800000002"
    }
]

print("=" * 50)
print("创建测试用户")
print("=" * 50)

for user in users:
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=user)
        result = response.json()
        if result['code'] in [200, 201]:
            print(f"✅ 成功创建用户: {user['username']} ({user['real_name']})")
        else:
            print(f"❌ 创建失败: {user['username']} - {result.get('message', '未知错误')}")
    except Exception as e:
        print(f"❌ 错误: {user['username']} - {str(e)}")

print("\n" + "=" * 50)
print("完成！现在可以使用以下账号登录：")
print("=" * 50)
print("用户名: admin, 密码: admin123")
print("用户名: warehouse01, 密码: warehouse123")
print("用户名: teacher01, 密码: teacher123")

