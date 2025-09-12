const ERROR_CODES = {
// 4xx 客户端错误
'VALIDATION_ERROR': 400, // 数据验证失败
'UNAUTHORIZED': 401, // 未授权
'FORBIDDEN': 403, // 禁止访问
'NOT_FOUND': 404, // 资源不存在
'METHOD_NOT_ALLOWED': 405, // 方法不允许
'CONFLICT': 409, // 资源冲突

// 5xx 服务器错误
'INTERNAL_ERROR': 500, // 内部服务器错误
'SERVICE_UNAVAILABLE': 503 // 服务不可用
}
