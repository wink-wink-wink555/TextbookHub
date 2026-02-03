// API 通信模块
const API_BASE_URL = 'http://localhost:5000/api/v1';

class API {
    constructor() {
        this.token = localStorage.getItem('token');
    }

    // 设置Token
    setToken(token) {
        this.token = token;
        localStorage.setItem('token', token);
    }

    // 清除Token
    clearToken() {
        this.token = null;
        localStorage.removeItem('token');
        localStorage.removeItem('user');
    }

    // 获取请求头
    getHeaders(includeAuth = true) {
        const headers = {
            'Content-Type': 'application/json'
        };
        if (includeAuth && this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }
        return headers;
    }

    // 通用请求方法
    async request(url, method = 'GET', data = null, includeAuth = true) {
        const options = {
            method,
            headers: this.getHeaders(includeAuth)
        };

        if (data && (method === 'POST' || method === 'PUT')) {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(`${API_BASE_URL}${url}`, options);
            const result = await response.json();

            if (result.code === 401) {
                // Token过期，跳转到登录页
                this.clearToken();
                window.location.href = '/';
                throw new Error('登录已过期，请重新登录');
            }

            return result;
        } catch (error) {
            console.error('API请求错误:', error);
            throw error;
        }
    }

    // 认证相关
    async login(username, password) {
        return await this.request('/auth/login', 'POST', { username, password }, false);
    }

    async getCurrentUser() {
        return await this.request('/auth/current_user');
    }

    async getUsers() {
        return await this.request('/auth/users');
    }

    // 教材相关
    async getTextbooks(page = 1, perPage = 10, keyword = '', publisherId = '', typeId = '') {
        let url = `/textbooks?page=${page}&per_page=${perPage}`;
        if (keyword) url += `&keyword=${keyword}`;
        if (publisherId) url += `&publisher_id=${publisherId}`;
        if (typeId) url += `&type_id=${typeId}`;
        return await this.request(url);
    }

    async getTextbook(id) {
        return await this.request(`/textbooks/${id}`);
    }

    async createTextbook(data) {
        return await this.request('/textbooks', 'POST', data);
    }

    async updateTextbook(id, data) {
        return await this.request(`/textbooks/${id}`, 'PUT', data);
    }

    async deleteTextbook(id) {
        return await this.request(`/textbooks/${id}`, 'DELETE');
    }

    // 出版社相关
    async getPublishers(page = 1, perPage = 100) {
        return await this.request(`/publishers?page=${page}&per_page=${perPage}`);
    }

    async getPublisher(id) {
        return await this.request(`/publishers/${id}`);
    }

    async createPublisher(data) {
        return await this.request('/publishers', 'POST', data);
    }

    async updatePublisher(id, data) {
        return await this.request(`/publishers/${id}`, 'PUT', data);
    }

    async deletePublisher(id) {
        return await this.request(`/publishers/${id}`, 'DELETE');
    }

    // 教材类型相关
    async getTextbookTypes() {
        return await this.request('/textbook-types');
    }

    async getTextbookTypesTree() {
        return await this.request('/textbook-types/tree');
    }

    // 订单相关
    async getPurchaseOrders(page = 1, perPage = 10, status = '', keyword = '') {
        let url = `/purchase-orders?page=${page}&per_page=${perPage}`;
        if (status) url += `&status=${status}`;
        if (keyword) url += `&keyword=${keyword}`;
        return await this.request(url);
    }

    async getPurchaseOrder(id) {
        return await this.request(`/purchase-orders/${id}`);
    }

    async createPurchaseOrder(data) {
        return await this.request('/purchase-orders', 'POST', data);
    }

    async updatePurchaseOrder(id, data) {
        return await this.request(`/purchase-orders/${id}`, 'PUT', data);
    }

    async approvePurchaseOrder(id, approver) {
        return await this.request(`/purchase-orders/${id}/approve`, 'POST', { approver });
    }

    async cancelPurchaseOrder(id, reason) {
        return await this.request(`/purchase-orders/${id}/cancel`, 'POST', { reason });
    }

    async deliverPurchaseOrder(id) {
        return await this.request(`/purchase-orders/${id}/deliver`, 'POST', {});
    }

    // 统计相关
    async getDashboard() {
        return await this.request('/statistics/dashboard');
    }

    async getStatisticsByType() {
        return await this.request('/statistics/by-type');
    }

    async getStatisticsByPublisher() {
        return await this.request('/statistics/by-publisher');
    }

    async getStatisticsByTextbook(id) {
        return await this.request(`/statistics/by-textbook/${id}`);
    }

    async getStatisticsByDate(startDate, endDate) {
        return await this.request(`/statistics/by-date?start_date=${startDate}&end_date=${endDate}`);
    }

    async getInventoryWarnings() {
        return await this.request('/statistics/inventory-warnings');
    }

    // 入库相关
    async getStockIns(page = 1, perPage = 10, keyword = '') {
        let url = `/stock-ins?page=${page}&per_page=${perPage}`;
        if (keyword) url += `&keyword=${keyword}`;
        return await this.request(url);
    }

    async createStockIn(data) {
        return await this.request('/stock-ins', 'POST', data);
    }

    async deleteStockIn(id) {
        return await this.request(`/stock-ins/${id}`, 'DELETE');
    }

    // 直接入库（不经过订单，自动创建订单并入库）
    async directStockIn(data) {
        return await this.request('/stock-ins/direct', 'POST', data);
    }
}

// 创建全局API实例
const api = new API();

