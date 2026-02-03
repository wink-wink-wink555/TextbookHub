"""
订购API
"""
from flask import request
from flask_jwt_extended import jwt_required, get_jwt
from app.api.v1 import api_v1
from app.services.purchase_service import PurchaseService
from app.schemas.purchase_order_schema import PurchaseOrderSchema, PurchaseOrderUpdateSchema
from app.utils.response import success_response, error_response, paginated_response
from app.utils.helpers import get_pagination_params
from app.utils.decorators import teacher_required, warehouse_required
from marshmallow import ValidationError


purchase_service = PurchaseService()


@api_v1.route('/purchase-orders', methods=['GET'])
@jwt_required()
def get_purchase_orders():
    """
    获取订单列表
    - 管理员和仓库管理员：查看所有订单
    - 教师：查看order_person是自己或普通用户的订单
    - 普通用户：只能查看order_person是自己的订单
    """
    try:
        current_user = get_jwt()
        role = current_user.get('role')
        # 注意：JWT的sub存储的是user_id，username在additional_claims中
        username = current_user.get('username')
        
        page, per_page = get_pagination_params()
        status = request.args.get('status')
        keyword = request.args.get('keyword')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # 数据权限过滤
        order_person = None
        allowed_roles = None
        if role == '普通用户':
            # 普通用户只能查看order_person是自己的订单
            order_person = username
        elif role == '教师':
            # 教师可以查看order_person是自己或普通用户的订单
            # 这里需要特殊处理，传递allowed_roles参数
            allowed_roles = ['教师', '普通用户']
        # 管理员和仓库管理员不设限制，可以看到所有订单
        
        items, total = purchase_service.get_order_list(
            page=page,
            per_page=per_page,
            status=status,
            start_date=start_date,
            end_date=end_date,
            keyword=keyword,
            order_person=order_person,
            current_username=username if role == '教师' else None,
            allowed_roles=allowed_roles
        )
        
        return paginated_response(items, total, page, per_page)
    except Exception as e:
        return error_response(message=str(e))


@api_v1.route('/purchase-orders/<int:order_id>', methods=['GET'])
@jwt_required()
def get_purchase_order(order_id):
    """
    获取订单详情
    - 管理员和仓库管理员：查看任何订单
    - 教师：只能查看order_person是自己或普通用户的订单
    - 普通用户：只能查看order_person是自己的订单
    """
    try:
        current_user = get_jwt()
        role = current_user.get('role')
        # 注意：JWT的sub存储的是user_id，username在additional_claims中
        username = current_user.get('username')
        
        result = purchase_service.get_order_detail(order_id)
        
        # 数据权限检查
        if role not in ['管理员', '仓库管理员']:
            order_person = result.get('order_person')
            
            if role == '普通用户':
                # 普通用户只能查看order_person是自己的订单
                if order_person != username:
                    return error_response(message='您只能查看订购人是自己的订单', code=403)
            elif role == '教师':
                # 教师只能查看order_person是自己或普通用户的订单
                # 需要检查订购人的角色
                from app.dao.user_dao import UserDAO
                user_dao = UserDAO()
                target_user = user_dao.find_by_username(order_person)
                
                if order_person != username and (not target_user or target_user.role != '普通用户'):
                    return error_response(message='教师只能查看订购人是自己或普通用户的订单', code=403)
        
        return success_response(data=result)
    except Exception as e:
        return error_response(message=str(e))


@api_v1.route('/purchase-orders', methods=['POST'])
@jwt_required()
def create_purchase_order():
    """创建订单（所有登录用户）"""
    try:
        current_user = get_jwt()
        role = current_user.get('role')
        # 注意：JWT的sub存储的是user_id，username在additional_claims中
        username = current_user.get('username')
        
        schema = PurchaseOrderSchema()
        data = schema.load(request.get_json())
        
        # 权限检查：确保用户只能为有权限的人创建订单
        order_person = data.get('order_person')
        
        # 验证订购人是否合法
        from app.dao.user_dao import UserDAO
        user_dao = UserDAO()
        target_user = user_dao.find_by_username(order_person)
        
        if not target_user:
            return error_response(message='订购人不存在', code=400)
        
        # 根据角色进行权限检查
        if role == '普通用户':
            # 普通用户只能为自己创建订单
            if order_person != username:
                return error_response(message='普通用户只能为自己创建订单', code=403)
        elif role == '教师':
            # 教师只能为自己或普通用户创建订单
            if order_person != username and target_user.role != '普通用户':
                return error_response(message='教师只能为自己或普通用户创建订单', code=403)
        # 管理员和仓库管理员可以为任何人创建订单，无需额外检查
        
        result = purchase_service.create_order(data)
        return success_response(data=result, message='创建成功', code=201)
    except ValidationError as e:
        return error_response(message='数据验证失败', errors=e.messages)
    except Exception as e:
        return error_response(message=str(e))


@api_v1.route('/purchase-orders/<int:order_id>', methods=['PUT'])
@jwt_required()
def update_purchase_order(order_id):
    """
    更新订单
    - 管理员和仓库管理员：可以修改任何订单
    - 教师/普通用户：只能修改order_person是自己的待审核订单
    """
    try:
        current_user = get_jwt()
        role = current_user.get('role')
        # 注意：JWT的sub存储的是user_id，username在additional_claims中
        username = current_user.get('username')
        
        # 先获取原订单
        original = purchase_service.get_order_detail(order_id)
        
        # 数据权限检查
        if role not in ['管理员', '仓库管理员']:
            # 教师和普通用户只能修改order_person是自己的订单
            if original.get('order_person') != username:
                return error_response(message='您只能修改订购人是自己的订单', code=403)
            if original.get('order_status') != '待审核':
                return error_response(message='只能修改待审核状态的订单', code=403)
        
        schema = PurchaseOrderUpdateSchema()
        data = schema.load(request.get_json())
        
        result = purchase_service.update_order(order_id, data)
        return success_response(data=result, message='更新成功')
    except ValidationError as e:
        return error_response(message='数据验证失败', errors=e.messages)
    except Exception as e:
        return error_response(message=str(e))


@api_v1.route('/purchase-orders/<int:order_id>/approve', methods=['POST'])
@jwt_required()
@warehouse_required
def approve_purchase_order(order_id):
    """审核订单（仅管理员和仓库管理员）"""
    try:
        current_user = get_jwt()
        approver = current_user.get('real_name') or current_user.get('username')
        
        result = purchase_service.approve_order(order_id, approver)
        return success_response(data=result, message='审核成功')
    except Exception as e:
        return error_response(message=str(e))


@api_v1.route('/purchase-orders/<int:order_id>/deliver', methods=['POST'])
@jwt_required()
@warehouse_required
def deliver_purchase_order(order_id):
    """
    发放订单（仅管理员和仓库管理员）
    - 订单必须是"已到货"状态
    - 发放后：库存扣减已到货数量，订单状态变为"已发放"
    """
    try:
        from flask_jwt_extended import get_jwt
        from app.dao.purchase_order_dao import PurchaseOrderDAO
        from app.extensions import db
        
        current_user = get_jwt()
        username = current_user.get('username')
        
        # 获取订单信息
        purchase_dao = PurchaseOrderDAO()
        order = purchase_dao.get_by_id(order_id)
        
        if not order:
            return error_response(message='订单不存在', code=404)
        
        if order.order_status != '已到货':
            return error_response(message='只有"已到货"状态的订单才能发放', code=400)
        
        if order.arrived_quantity <= 0:
            return error_response(message='订单没有可发放的数量', code=400)
        
        # 检查库存是否充足
        from app.models.inventory import Inventory
        inventory = Inventory.query.filter_by(textbook_id=order.textbook_id).first()
        
        if not inventory or inventory.current_quantity < order.arrived_quantity:
            return error_response(message='库存不足，无法发放', code=400)
        
        # 扣减库存
        inventory.current_quantity -= order.arrived_quantity
        inventory.total_out_quantity += order.arrived_quantity
        from datetime import date
        inventory.last_out_date = date.today()
        
        # 更新订单状态为"已发放"
        order.order_status = '已发放'
        order.remarks = f'{order.remarks or ""}\n[{date.today()}] 由 {username} 发放，数量：{order.arrived_quantity}'.strip()
        
        db.session.commit()
        
        return success_response(message=f'发放成功，已从库存扣减 {order.arrived_quantity} 本')
    except Exception as e:
        from app.extensions import db
        db.session.rollback()
        return error_response(message=str(e))


@api_v1.route('/purchase-orders/<int:order_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_purchase_order(order_id):
    """
    取消订单
    - 管理员和仓库管理员：可以取消任何订单
    - 教师：只能取消order_person是自己或普通用户的待审核订单
    - 普通用户：只能取消order_person是自己的待审核订单
    """
    try:
        current_user = get_jwt()
        role = current_user.get('role')
        # 注意：JWT的sub存储的是user_id，username在additional_claims中
        username = current_user.get('username')
        
        # 获取原订单
        original = purchase_service.get_order_detail(order_id)
        order_person = original.get('order_person')
        
        # 数据权限检查
        if role not in ['管理员', '仓库管理员']:
            if role == '普通用户':
                # 普通用户只能取消order_person是自己的订单
                if order_person != username:
                    return error_response(message='您只能取消订购人是自己的订单', code=403)
            elif role == '教师':
                # 教师只能取消order_person是自己或普通用户的订单
                if order_person != username:
                    from app.dao.user_dao import UserDAO
                    user_dao = UserDAO()
                    target_user = user_dao.find_by_username(order_person)
                    if not target_user or target_user.role != '普通用户':
                        return error_response(message='教师只能取消订购人是自己或普通用户的订单', code=403)
            
            # 检查订单状态
            if original.get('order_status') != '待审核':
                return error_response(message='只能取消待审核状态的订单', code=403)
        
        reason = request.get_json().get('reason') if request.get_json() else None
        result = purchase_service.cancel_order(order_id, reason)
        return success_response(data=result, message='取消成功')
    except Exception as e:
        return error_response(message=str(e))

