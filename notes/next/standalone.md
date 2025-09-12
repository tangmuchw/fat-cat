# standalone 模式

Next.js 的 `standalone` 模式是一种专为生产环境优化的构建输出类型，通过配置 `output: 'standalone'` 在 `next.config.js` 中启用。它主要解决传统部署的依赖冗余、镜像体积过大等问题，适用于容器化、低资源主机或自托管场景。以下是其核心作用及实现细节：

---

### ⚙️ 一、**核心机制：生成最小化运行环境**

1. **独立部署目录**  
   执行 `next build` 后，生成 `.next/standalone` 目录，包含：

    - **精简版 `node_modules`**：仅保留运行必需的依赖（剔除开发依赖、Webpack 等构建工具），大幅减少文件数量。
    - **自包含服务器入口**：自动生成 `server.js` 文件，替代 `next start`，直接通过 `node server.js` 启动应用。
    - **静态资源映射**：需手动复制 `public` 和 `.next/static` 到 `standalone` 目录，否则需通过 CDN 托管。

2. **依赖树优化（Tree Shaking）**  
   通过静态分析移除未使用的代码，确保 `node_modules` 仅包含运行时代码，避免传统部署中全量依赖的冗余。

---

### 🐳 二、**在容器化部署中的核心优势**

1. **显著减小镜像体积**

    - 传统镜像：约 2.6 GB（包含完整 `node_modules` 和源码）。
    - `standalone` 镜像：**100–200 MB**（仅运行必需文件），提升推送与部署效率。
    - **Dockerfile 配置示例**：

        ```dockerfile
        # 多阶段构建：仅复制 standalone 目录
        COPY --from=builder /app/.next/standalone ./
        COPY --from=builder /app/.next/static ./.next/static
        COPY --from=builder /app/public ./public
        CMD ["node", "server.js"]

        ```

2. **解决低配置主机构建问题**  
   在 1GB 内存的服务器上，传统构建常因 Webpack 内存溢出失败。`standalone` 支持在高性能主机构建后，将产物直接移植到低配主机运行。

---

### ⚖️ 三、**适用场景与限制**

1. **最佳适用场景**

    - **自托管/传统服务器**：需灵活控制服务端环境（如自定义中间件、SSR 优化）。
    - **资源敏感环境**：小内存主机、边缘计算节点。
    - **容器化部署**：Kubernetes、Docker Swarm 等。

2. **与 `export` 模式的区别**  
   | **模式** | `standalone` | `export` |
   |----------------|----------------------------------|------------------------------|
   | **输出类型** | 包含服务端逻辑的 Node 应用 | 纯静态 HTML/CSS/JS 文件 |
   | **部署目标** | 需 Node 环境的服务器 | CDN/静态托管（Netlify/Vercel）|
   | **动态能力** | 支持 SSR、API 路由 | 仅静态生成（SSG） |

3. **局限性**
    - **启动命令变更**：必须使用 `node server.js`，而非 `next start`（否则报错）。
    - **需手动复制静态资源**：若未配置 CDN，需手动复制 `public` 和 `.next/static`。
    - **潜在体积增大**：包含 Node.js 运行时，可通过 Tree Shaking 缓解。

---

### 🚀 四、**正确使用方式**

1. **启用配置**

    ```javascript
    // next.config.js
    module.exports = {
        output: "standalone",
    };
    ```

2. **启动命令**

    - 开发环境：`next dev`
    - 生产环境：`node .next/standalone/server.js`  
      （或结合 PM2：`pm2 start .next/standalone/server.js`）

3. **系统服务配置（systemd）**

    ```ini
    [Service]
    ExecStart=/usr/bin/node /path/to/standalone/server.js
    Restart=always

    ```

---

### 💎 总结

`standalone` 模式通过 **构建自包含、最小化的 Node 应用包**，解决了传统部署的资源占用高、环境依赖强等问题。其核心价值在于：

-   ✅ **轻量化**：依赖树优化使镜像体积缩减 90%+。
-   ✅ **移植性**：脱离 `node_modules` 束缚，适配各类服务器。
-   ✅ **部署标准化**：统一入口文件与启动流程，降低运维复杂度。

适合需要平衡性能、资源与部署灵活性的生产场景，尤其推荐用于容器化或自托管架构。对于纯静态站点，可优先考虑 `export` 模式以进一步提升性能。
