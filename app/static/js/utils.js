// 工具函数

// 显示提示消息
function showMessage(message, type = 'success') {
    // 图标映射
    const iconMap = {
        'success': 'fa-check-circle',
        'error': 'fa-times-circle',
        'warning': 'fa-exclamation-circle',
        'info': 'fa-info-circle'
    };
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.innerHTML = `<i class="fas ${iconMap[type] || iconMap.info}"></i><span>${message}</span>`;
    alertDiv.style.position = 'fixed';
    alertDiv.style.top = '20px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '9999';
    alertDiv.style.minWidth = '300px';
    alertDiv.style.maxWidth = '400px';
    
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.style.opacity = '0';
        alertDiv.style.transform = 'translateX(20px)';
        alertDiv.style.transition = 'all 0.3s ease';
        setTimeout(() => alertDiv.remove(), 300);
    }, 3000);
}

// 显示加载状态
function showLoading(element) {
    const originalText = element.textContent;
    element.disabled = true;
    element.innerHTML = '<span class="loading"></span> 加载中...';
    return originalText;
}

// 隐藏加载状态
function hideLoading(element, originalText) {
    element.disabled = false;
    element.textContent = originalText;
}

// 格式化日期
function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-CN');
}

// 格式化金额
function formatMoney(amount) {
    return `¥${parseFloat(amount).toFixed(2)}`;
}

// 获取状态徽章样式
function getStatusBadgeClass(status) {
    const statusMap = {
        '待审核': 'badge-warning',
        '已审核': 'badge-info',
        '已订购': 'badge-info',
        '部分到货': 'badge-warning',
        '已到货': 'badge-success',
        '已取消': 'badge-danger',
        '待审批': 'badge-warning',
        '已审批': 'badge-info',
        '已发放': 'badge-success',
        '已拒绝': 'badge-danger',
        '正常': 'badge-success',
        '库存不足': 'badge-danger',
        '库存过多': 'badge-warning'
    };
    return statusMap[status] || 'badge-info';
}

// 创建状态徽章HTML
function createStatusBadge(status) {
    const badgeClass = getStatusBadgeClass(status);
    
    // 状态图标映射
    const iconMap = {
        '待审核': 'fa-clock',
        '已审核': 'fa-check',
        '已订购': 'fa-shopping-cart',
        '部分到货': 'fa-truck',
        '已到货': 'fa-box',
        '已取消': 'fa-times',
        '待审批': 'fa-hourglass-half',
        '已审批': 'fa-check-double',
        '已发放': 'fa-paper-plane',
        '已拒绝': 'fa-ban',
        '正常': 'fa-check-circle',
        '库存不足': 'fa-exclamation-triangle',
        '库存过多': 'fa-boxes'
    };
    
    const icon = iconMap[status] || 'fa-circle';
    return `<span class="badge ${badgeClass}"><i class="fas ${icon}"></i> ${status}</span>`;
}

// 确认对话框
function confirmAction(message) {
    return confirm(message);
}

// 模态框控制
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('show');
    }
}

function hideModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('show');
    }
}

// 表单验证
function validateForm(formData, rules) {
    const errors = [];
    
    for (const [field, rule] of Object.entries(rules)) {
        const value = formData[field];
        
        if (rule.required && !value) {
            errors.push(`${rule.label}不能为空`);
        }
        
        if (rule.pattern && value && !rule.pattern.test(value)) {
            errors.push(`${rule.label}格式不正确`);
        }
        
        if (rule.min && value && parseFloat(value) < rule.min) {
            errors.push(`${rule.label}不能小于${rule.min}`);
        }
    }
    
    return errors;
}

// ISBN格式验证
function validateISBN(isbn) {
    const pattern = /^ISBN\d{10}$/;
    return pattern.test(isbn);
}

// 分页组件生成
function createPagination(currentPage, totalPages, onPageChange) {
    const container = document.createElement('div');
    container.className = 'pagination';
    
    // 上一页
    const prevBtn = document.createElement('button');
    prevBtn.textContent = '上一页';
    prevBtn.disabled = currentPage === 1;
    prevBtn.onclick = () => onPageChange(currentPage - 1);
    container.appendChild(prevBtn);
    
    // 页码
    const maxButtons = 5;
    let startPage = Math.max(1, currentPage - Math.floor(maxButtons / 2));
    let endPage = Math.min(totalPages, startPage + maxButtons - 1);
    
    if (endPage - startPage < maxButtons - 1) {
        startPage = Math.max(1, endPage - maxButtons + 1);
    }
    
    for (let i = startPage; i <= endPage; i++) {
        const pageBtn = document.createElement('button');
        pageBtn.textContent = i;
        pageBtn.className = i === currentPage ? 'active' : '';
        pageBtn.onclick = () => onPageChange(i);
        container.appendChild(pageBtn);
    }
    
    // 下一页
    const nextBtn = document.createElement('button');
    nextBtn.textContent = '下一页';
    nextBtn.disabled = currentPage === totalPages;
    nextBtn.onclick = () => onPageChange(currentPage + 1);
    container.appendChild(nextBtn);
    
    return container;
}

// 保存用户信息
function saveUserInfo(user) {
    localStorage.setItem('user', JSON.stringify(user));
}

// 获取用户信息
function getUserInfo() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}

// 检查登录状态
function checkLogin() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/';
        return false;
    }
    return true;
}

// 退出登录
function logout() {
    if (confirmAction('确定要退出登录吗？')) {
        api.clearToken();
        localStorage.removeItem('user');
        window.location.href = '/';
    }
}

// 处理错误
function handleError(error, defaultMessage = '操作失败') {
    console.error('Error:', error);
    const message = error.message || defaultMessage;
    showMessage(message, 'error');
}

// 防抖函数
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 导出数据为CSV
function exportToCSV(data, filename) {
    if (!data || data.length === 0) {
        showMessage('没有数据可导出', 'warning');
        return;
    }
    
    const headers = Object.keys(data[0]);
    const csv = [
        headers.join(','),
        ...data.map(row => headers.map(field => row[field]).join(','))
    ].join('\n');
    
    const blob = new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `${filename}_${new Date().getTime()}.csv`;
    link.click();
}

// ======================
// 权限检查相关函数
// ======================

/**
 * 检查当前用户是否有指定角色
 * @param {string|array} roles - 角色名称或角色数组，如 '管理员' 或 ['管理员', '仓库管理员']
 * @returns {boolean}
 */
function hasRole(roles) {
    const user = getUserInfo();
    if (!user || !user.role) return false;
    
    if (typeof roles === 'string') {
        return user.role === roles;
    }
    
    if (Array.isArray(roles)) {
        return roles.includes(user.role);
    }
    
    return false;
}

/**
 * 检查是否为管理员
 */
function isAdmin() {
    return hasRole('管理员');
}

/**
 * 检查是否为管理员或仓库管理员
 */
function isAdminOrWarehouse() {
    return hasRole(['管理员', '仓库管理员']);
}

/**
 * 检查是否为教师及以上角色（管理员、仓库管理员、教师）
 */
function isTeacherOrAbove() {
    return hasRole(['管理员', '仓库管理员', '教师']);
}

/**
 * 检查是否可以查看订单（所有登录用户都可以）
 */
function canViewOrders() {
    const user = getUserInfo();
    return user && user.role; // 只要登录就可以查看订单
}

/**
 * 检查是否可以创建订单（教师、普通用户可以为自己或学生创建）
 */
function canCreateOrder() {
    return hasRole(['管理员', '仓库管理员', '教师', '普通用户']);
}

/**
 * 检查是否可以查看基础统计（所有登录用户）
 */
function canViewStatistics() {
    const user = getUserInfo();
    return user && user.role; // 所有登录用户都可以查看统计
}

/**
 * 检查是否可以管理基础数据（教材、出版社、教材类型）
 * 只有管理员可以
 */
function canManageBasicData() {
    return isAdmin();
}

/**
 * 根据权限隐藏元素
 * @param {string} selector - CSS选择器
 * @param {function} checkFunc - 权限检查函数，返回true表示有权限
 */
function hideIfNoPermission(selector, checkFunc) {
    const element = document.querySelector(selector);
    if (element && !checkFunc()) {
        element.style.display = 'none';
    }
}

/**
 * 根据权限禁用元素
 * @param {string} selector - CSS选择器
 * @param {function} checkFunc - 权限检查函数，返回true表示有权限
 * @param {string} tooltipText - 鼠标悬停提示文字
 */
function disableIfNoPermission(selector, checkFunc, tooltipText = '您没有此操作的权限') {
    const element = document.querySelector(selector);
    if (element && !checkFunc()) {
        element.disabled = true;
        element.style.opacity = '0.5';
        element.style.cursor = 'not-allowed';
        element.title = tooltipText;
        
        // 阻止点击事件
        element.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            showMessage(tooltipText, 'warning');
            return false;
        }, true);
    }
}

/**
 * 根据权限控制多个按钮
 * @param {object} config - 配置对象，格式：{ selector: checkFunc }
 */
function applyPermissions(config) {
    for (const [selector, checkFunc] of Object.entries(config)) {
        hideIfNoPermission(selector, checkFunc);
    }
}

/**
 * 在需要权限的操作前检查并提示
 * @param {function} checkFunc - 权限检查函数
 * @param {function} callback - 有权限时执行的回调
 * @param {string} message - 无权限时的提示信息
 */
function checkPermissionBeforeAction(checkFunc, callback, message = '您没有此操作的权限') {
    if (checkFunc()) {
        callback();
    } else {
        showMessage(message, 'warning');
    }
}

