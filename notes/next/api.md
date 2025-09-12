在 Next.js 项目中定义规范的后端接口，需要结合 RESTful 设计原则、目录结构规范和代码组织。以下是推荐的规范方案：

---

### 一、目录结构规范

```bash
src/
├── pages/
│   ├── api/
│   │   ├── v1/                  # API 版本控制
│   │   │   ├── auth/
│   │   │   │   ├── login.js     # POST /api/v1/auth/login
│   │   │   │   └── register.js
│   │   │   ├── users/
│   │   │   │   ├── [userId].js # 动态路由
│   │   │   │   └── index.js     # GET /api/v1/users
│   │   │   └── products/
│   │   └── middleware.js        # 全局中间件
│   └── ...
├── lib/
│   ├── api/
│   │   ├── handlers/            # 业务逻辑处理
│   │   │   ├── userHandlers.js
│   │   │   └── productHandlers.js
│   │   ├── utils/
│   │   │   ├── httpResponse.js  # 统一响应格式
│   │   │   └── errorHandler.js  # 错误处理
│   │   └── db.js                # 数据库连接
└── ...
```

---

### 二、接口设计规范

#### 1. RESTful 原则

| 方法   | 路径               | 描述         |
| ------ | ------------------ | ------------ |
| GET    | /api/v1/users      | 获取用户列表 |
| POST   | /api/v1/users      | 创建用户     |
| GET    | /api/v1/users/{id} | 获取单个用户 |
| PUT    | /api/v1/users/{id} | 更新用户     |
| DELETE | /api/v1/users/{id} | 删除用户     |

#### 2. 版本控制

-   路径中包含版本号：`/api/v1/...`
-   通过目录实现：`pages/api/v1/`

---

### 三、代码实现规范

#### 1. 统一响应格式 (`lib/api/utils/httpResponse.js`)

```javascript
// 成功响应
export const successResponse = (res, data, status = 200) => {
    res.status(status).json({
        success: true,
        data,
    });
};

// 错误响应
export const errorResponse = (res, message, status = 400) => {
    res.status(status).json({
        success: false,
        error: message,
    });
};
```

#### 2. 错误处理中间件 (`pages/api/middleware.js`)

```javascript
export const errorHandler = (handler) => async (req, res) => {
    try {
        await handler(req, res);
    } catch (err) {
        console.error("API Error:", err);
        errorResponse(res, "Internal Server Error", 500);
    }
};
```

#### 3. 接口示例 (`pages/api/v1/users/[userId].js`)

```javascript
import { errorHandler } from "../middleware";
import { getUserById, updateUser } from "@/lib/api/handlers/userHandlers";
import { successResponse, errorResponse } from "@/lib/api/utils/httpResponse";

// 统一使用错误处理包装
export default errorHandler(async (req, res) => {
    const { userId } = req.query;

    switch (req.method) {
        case "GET":
            const user = await getUserById(userId);
            if (!user) return errorResponse(res, "User not found", 404);
            successResponse(res, user);
            break;

        case "PUT":
            const updatedUser = await updateUser(userId, req.body);
            successResponse(res, updatedUser);
            break;

        default:
            res.setHeader("Allow", ["GET", "PUT"]);
            errorResponse(res, `Method ${req.method} Not Allowed`, 405);
    }
});
```

#### 4. 业务逻辑分离 (`lib/api/handlers/userHandlers.js`)

```javascript
import db from "@/lib/api/db";

// 纯业务逻辑，不处理 HTTP 响应
export const getUserById = async (userId) => {
    return await db.user.findUnique({ where: { id: userId } });
};

export const updateUser = async (userId, data) => {
    return await db.user.update({
        where: { id: userId },
        data,
    });
};
```

---

### 四、安全与最佳实践

1. **请求验证**

    - 使用 Zod 或 Joi 进行参数校验

    ```javascript
    import z from "zod";
    const userSchema = z.object({
        name: z.string().min(2),
        email: z.string().email(),
    });
    ```

2. **身份认证**

    - 使用 NextAuth.js 处理 JWT/OAuth
    - 路由保护中间件：

    ```javascript
    export const authMiddleware = (handler) => (req, res) => {
      const session = await getSession({ req });
      if (!session) return errorResponse(res, 'Unauthorized', 401);
      return handler(req, res);
    };
    ```

3. **CORS 配置**

    ```javascript
    import Cors from "cors";
    const cors = Cors({ methods: ["GET", "POST"] });

    // 在 handler 中使用
    await runMiddleware(req, res, cors);
    ```

4. **速率限制**
    - 使用 `rate-limiter-flexible` 库
    ```javascript
    const limiter = new RateLimiter({
        points: 10, // 10 次请求
        duration: 1, // 每 1 秒
    });
    ```

---

### 五、文档规范

1. 使用 OpenAPI (Swagger) 生成接口文档
2. 在 JSDoc 中添加注释：

```javascript
/**
 * @swagger
 * /api/v1/users/{id}:
 *   get:
 *     summary: 获取用户详情
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 */
```

---

### 六、测试建议

1. 使用 Jest + Supertest 进行接口测试
2. 示例测试代码：

```javascript
import request from "supertest";
import app from "../../server";

test("GET /api/v1/users returns 200", async () => {
    const response = await request(app).get("/api/v1/users");
    expect(response.status).toBe(200);
    expect(response.body.success).toBe(true);
});
```

---

### 总结关键点

1. **分层架构**：路由层 → 控制器层 → 服务层
2. **统一响应**：标准化成功/错误响应格式
3. **错误处理**：全局错误捕获中间件
4. **安全防护**：身份验证、输入校验、速率限制
5. **文档驱动**：Swagger 注释 + 类型定义
6. **版本控制**：路径中包含 `/v1/` 前缀

通过以上规范，可确保 Next.js 后端接口具备：
✅ 清晰的代码结构  
✅ 统一的响应格式  
✅ 完善的错误处理  
✅ 可扩展的版本管理  
✅ 易于维护的文档体系  
✅ 可靠的安全防护机制
