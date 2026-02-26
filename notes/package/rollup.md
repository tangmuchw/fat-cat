# Rollup 源码深度分析

我来详细分析 Rollup 的核心源码实现。我们将从架构设计到具体实现逐步深入。

## 一、源码结构概览

### 1. **核心目录结构**

```
rollup/
├── src/
│   ├── rollup/           # 公共 API 入口
│   ├── ast/              # AST 处理相关
│   ├── Bundle/           # Bundle 生成逻辑
│   ├── Chunk/            # 代码块处理
│   ├── Module/           # 模块表示和解析
│   ├── ExternalModule/   # 外部模块处理
│   ├── utils/            # 工具函数
│   ├── finalisers/       # 输出格式生成器
│   └── watch/            # 监听模式
├── dist/                 # 打包输出
├── node_modules/
└── test/                 # 测试用例
```

### 2. **核心文件解析**

```javascript
// 主要入口文件
src / rollup / index.ts; // 主入口
src / rollup / rollup.ts; // rollup() 函数实现
src / rollup / PluginDriver.ts; // 插件驱动
src / Graph.ts; // 模块图（核心）
```

## 二、核心类架构

### 1. **Graph 类（核心）**

```typescript
// src/Graph.ts - 模块依赖图管理
class Graph {
    // 核心属性
    moduleById: Map<string, Module>; // 模块映射
    entryModules: Module[]; // 入口模块
    modules: Module[]; // 所有模块
    needsTreeshakingPass: boolean; // 是否需要 Tree-shaking

    // 构建过程
    async build(): Promise<void> {
        // 1. 加载入口模块
        await this.loadEntryModules();

        // 2. 构建模块图
        await this.buildModuleGraph();

        // 3. 标记 Tree-shaking
        this.includeStatements();

        // 4. 排序模块
        this.sortModules();

        // 5. 生成代码块
        await this.generateBundle();
    }
}
```

### 2. **Module 类**

```typescript
// src/Module.ts - 模块表示
class Module {
    id: string; // 模块ID
    originalCode: string; // 原始代码
    ast: ProgramNode; // AST 树
    dependencies: Module[]; // 依赖模块
    importBindings: Map<string, ImportBinding>; // 导入绑定
    exportBindings: Map<string, ExportBinding>; // 导出绑定
    renderedExports: string[]; // 渲染后的导出
    isExecuted: boolean; // 是否已执行
    scope: Scope; // 作用域

    // 解析模块
    async parse(): Promise<void> {
        // 使用 Acorn 解析 AST
        this.ast = acorn.parse(this.originalCode, {
            sourceType: "module",
            ecmaVersion: "latest",
            locations: true,
        });

        // 分析导入导出
        this.analyseImportsExports();

        // 构建作用域
        this.analyseScopes();
    }

    // Tree-shaking 标记
    markExportsUsed(usedExports: Set<string>): void {
        for (const [name, binding] of this.exportBindings) {
            binding.isUsed = usedExports.has(name);
        }
    }
}
```

## 三、Tree-shaking 实现

### 1. **Tree-shaking 核心算法**

```typescript
// src/ast/analyse.ts - 静态分析
function analyseModuleForTreeShaking(module: Module): void {
    // 第一步：收集所有导出
    const allExports = collectExports(module);

    // 第二步：从入口开始跟踪使用
    const usedExports = new Set<string>();
    const moduleQueue: Module[] = [module];
    const visitedModules = new Set<Module>();

    while (moduleQueue.length > 0) {
        const currentModule = moduleQueue.shift()!;
        if (visitedModules.has(currentModule)) continue;
        visitedModules.add(currentModule);

        // 分析当前模块的导入
        for (const importBinding of currentModule.importBindings.values()) {
            const importedModule = importBinding.module;
            const importedName = importBinding.importedName;

            if (importedModule && importedName) {
                // 标记该导出为已使用
                const exportBinding =
                    importedModule.exportBindings.get(importedName);
                if (exportBinding) {
                    exportBinding.isUsed = true;
                    usedExports.add(importedName);
                }

                // 继续分析导入的模块
                if (!visitedModules.has(importedModule)) {
                    moduleQueue.push(importedModule);
                }
            }
        }
    }

    // 第三步：递归标记依赖的导出
    function markDependentExports(exportBinding: ExportBinding): void {
        if (exportBinding.isUsed) return;
        exportBinding.isUsed = true;

        // 如果这个导出依赖于其他导出（重新导出）
        if (exportBinding.reExports) {
            for (const reExport of exportBinding.reExports) {
                markDependentExports(reExport);
            }
        }
    }
}
```

### 2. **作用域分析**

```typescript
// src/ast/scopes.ts - 作用域分析
class Scope {
    parent: Scope | null;
    variables: Map<string, Variable>;
    children: Scope[] = [];

    addDeclaration(
        name: string,
        identifier: Node,
        kind: "var" | "let" | "const" | "function"
    ): Variable {
        const variable = new Variable(name, identifier, kind);
        this.variables.set(name, variable);
        return variable;
    }

    findVariable(name: string): Variable | null {
        // 在当前作用域查找
        if (this.variables.has(name)) {
            return this.variables.get(name)!;
        }

        // 向父作用域查找
        if (this.parent) {
            return this.parent.findVariable(name);
        }

        return null;
    }
}
```

## 四、模块解析过程

### 1. **模块加载器**

```typescript
// src/ModuleLoader.ts
class ModuleLoader {
    constructor(private graph: Graph, private pluginDriver: PluginDriver) {}

    async loadModule(id: string, importer?: string): Promise<Module> {
        // 1. 解析模块ID
        const resolvedId = await this.resolveId(id, importer);

        // 2. 加载模块源码
        const code = await this.loadSource(resolvedId);

        // 3. 创建模块实例
        const module = new Module(resolvedId, code, this.graph);

        // 4. 解析AST
        await module.parse();

        // 5. 处理导入
        await this.processImports(module);

        return module;
    }

    private async resolveId(id: string, importer?: string): Promise<string> {
        // 调用插件的 resolveId 钩子
        const result = await this.pluginDriver.hookFirst("resolveId", [
            id,
            importer,
        ]);

        if (typeof result === "string") {
            return result;
        } else if (result && typeof result === "object") {
            return result.id;
        }

        // 默认解析逻辑
        return defaultResolve(id, importer);
    }
}
```

### 2. **AST 转换管道**

```typescript
// src/ast/transform.ts
class TransformPipeline {
    async transformModule(module: Module): Promise<void> {
        const { id, ast, originalCode } = module;

        // 应用插件的 transform 钩子
        let currentCode = originalCode;
        let currentAst = ast;

        const transformResult = await this.pluginDriver.hookReduceArg0(
            "transform",
            [currentCode, id],
            (previousCode, transformed) => {
                if (transformed == null) return previousCode;

                if (typeof transformed === "string") {
                    // 如果插件返回字符串，重新解析AST
                    currentCode = transformed;
                    currentAst = this.parseCode(transformed, id);
                } else if (transformed.ast) {
                    // 如果插件返回AST，直接使用
                    currentAst = transformed.ast;
                }

                return currentCode;
            },
            currentCode
        );

        module.ast = currentAst;
        module.code = transformResult;
    }
}
```

## 五、代码生成过程

### 1. **代码生成器**

```typescript
// src/Chunk.ts - 代码块生成
class Chunk {
    constructor(
        private modules: Module[],
        private options: NormalizedOutputOptions
    ) {}

    render(): MagicString {
        const magicString = new MagicString.Bundle();

        // 1. 按拓扑排序模块
        const sortedModules = this.topologicallySortModules();

        // 2. 渲染每个模块
        for (const module of sortedModules) {
            const rendered = this.renderModule(module);
            magicString.addSource({
                content: rendered,
                separator: "\n\n",
            });
        }

        // 3. 添加包装代码
        if (this.options.format !== "es") {
            magicString.prepend(this.renderWrapperHeader());
            magicString.append(this.renderWrapperFooter());
        }

        return magicString;
    }

    private renderModule(module: Module): string {
        const magicString = new MagicString(module.originalCode);

        // 1. 移除未使用的代码
        this.removeUnusedStatements(magicString, module);

        // 2. 重命名变量避免冲突
        this.renameIdentifiers(magicString, module);

        // 3. 作用域提升优化
        this.hoistStatements(magicString, module);

        return magicString.toString();
    }
}
```

### 2. **作用域提升实现**

```typescript
// src/optimize/hoist.ts
function hoistModule(module: Module, magicString: MagicString): void {
    const statementsToHoist: Statement[] = [];

    // 收集可以提升的语句
    walk(module.ast, {
        enter(node) {
            if (isTopLevelDeclaration(node)) {
                // 检查是否可以被安全提升
                if (canSafelyHoist(node, module.scope)) {
                    statementsToHoist.push(node);
                }
            }
        },
    });

    // 提升语句到模块顶部
    for (const statement of statementsToHoist) {
        const code = magicString.slice(statement.start, statement.end);
        magicString.remove(statement.start, statement.end);
        magicString.prependLeft(module.ast.start, code + "\n");
    }
}
```

## 六、插件系统实现

### 1. **插件驱动核心**

```typescript
// src/rollup/PluginDriver.ts
class PluginDriver {
    private plugins: readonly Plugin[];

    async hookFirst<T extends keyof PluginHooks>(
        hookName: T,
        args: Parameters<PluginHooks[T]>
    ): Promise<any> {
        for (const plugin of this.plugins) {
            const hook = plugin[hookName];
            if (hook) {
                const result = await (hook as Function).apply(plugin, args);
                if (result != null) {
                    return result;
                }
            }
        }
        return null;
    }

    async hookParallel<T extends keyof PluginHooks>(
        hookName: T,
        args: Parameters<PluginHooks[T]>
    ): Promise<void> {
        const promises: Promise<any>[] = [];

        for (const plugin of this.plugins) {
            const hook = plugin[hookName];
            if (hook) {
                promises.push(
                    Promise.resolve().then(() =>
                        (hook as Function).apply(plugin, args)
                    )
                );
            }
        }

        await Promise.all(promises);
    }
}
```

### 2. **钩子执行流程**

```typescript
// src/rollup/build.ts
async function build(options: InputOptions): Promise<OutputBundle> {
    const pluginDriver = new PluginDriver(options.plugins || []);

    // 1. options 钩子
    const resolvedOptions = await pluginDriver.hookFirst("options", [options]);

    // 2. buildStart 钩子
    await pluginDriver.hookParallel("buildStart", [resolvedOptions]);

    // 3. 模块解析钩子链
    const resolveId = async (id: string, importer?: string) => {
        const resolved = await pluginDriver.hookFirst("resolveId", [
            id,
            importer,
        ]);
        return resolved || defaultResolve(id, importer);
    };

    // 4. 模块加载钩子
    const load = async (id: string) => {
        const result = await pluginDriver.hookFirst("load", [id]);
        return result || fs.readFileSync(id, "utf-8");
    };

    // 5. transform 钩子链
    // ... 省略

    // 6. generateBundle 钩子
    await pluginDriver.hookParallel("generateBundle", [outputOptions, bundle]);

    // 7. writeBundle 钩子
    await pluginDriver.hookParallel("writeBundle", [outputOptions, bundle]);
}
```

## 七、Watch 模式实现

### 1. **文件监听器**

```typescript
// src/watch/watch.ts
class Watcher {
    private fileWatchers = new Map<string, fs.FSWatcher>();
    private dependencies = new Map<string, Set<string>>();

    async watch(): Promise<void> {
        // 1. 初始构建
        await this.build();

        // 2. 设置文件监听
        for (const file of this.getWatchedFiles()) {
            this.watchFile(file);
        }

        // 3. 处理变更事件
        this.setupChangeHandling();
    }

    private watchFile(file: string): void {
        const watcher = chokidar.watch(file, {
            persistent: true,
            ignoreInitial: true,
        });

        watcher.on("change", (filePath) => {
            this.handleFileChange(filePath);
        });

        this.fileWatchers.set(file, watcher);
    }

    private async handleFileChange(changedFile: string): Promise<void> {
        // 1. 找出受影响的模块
        const affectedModules = this.getAffectedModules(changedFile);

        // 2. 清除缓存
        this.invalidateCaches(affectedModules);

        // 3. 增量重建
        await this.incrementalBuild(affectedModules);

        // 4. 触发重新构建钩子
        await this.pluginDriver.hookParallel("watchChange", [changedFile]);
    }
}
```

## 八、代码生成优化

### 1. **MagicString 的使用**

```typescript
// Rollup 使用 MagicString 进行高效的字符串操作
import MagicString from "magic-string";

class ModuleRenderer {
    renderExports(module: Module): string {
        const magicString = new MagicString(module.originalCode);

        // 高效的字符串操作
        module.exportBindings.forEach((binding, name) => {
            if (!binding.isUsed) {
                // 删除未使用的导出
                magicString.remove(binding.start, binding.end);
            } else {
                // 重命名导出的变量
                if (binding.hasDifferentLocalName) {
                    magicString.overwrite(
                        binding.start,
                        binding.end,
                        binding.renderedName
                    );
                }
            }
        });

        return magicString.toString();
    }
}
```

### 2. **缓存机制**

```typescript
// src/utils/cache.ts
class ModuleCache {
    private cache = new Map<string, CachedModule>();
    private astCache = new WeakMap<Node, any>();

    get(id: string): CachedModule | undefined {
        const cached = this.cache.get(id);
        if (cached && !this.isStale(cached)) {
            return cached;
        }
        this.cache.delete(id);
        return undefined;
    }

    set(id: string, module: CachedModule): void {
        this.cache.set(id, {
            ...module,
            timestamp: Date.now(),
            dependencies: module.dependencies.slice(),
        });
    }

    private isStale(cached: CachedModule): boolean {
        // 检查依赖文件是否变更
        for (const dep of cached.dependencies) {
            const stats = fs.statSync(dep);
            if (stats.mtimeMs > cached.timestamp) {
                return true;
            }
        }
        return false;
    }
}
```

## 九、性能优化技巧

### 1. **懒解析**

```typescript
// src/Module.ts - 懒加载 AST
class LazyModule extends Module {
    private _ast: ProgramNode | null = null;

    get ast(): ProgramNode {
        if (!this._ast) {
            this._ast = this.parseAST();
        }
        return this._ast;
    }

    private parseAST(): ProgramNode {
        // 按需解析 AST
        return acorn.parse(this.originalCode, {
            sourceType: "module",
            ecmaVersion: "latest",
        });
    }
}
```

### 2. **增量编译**

```typescript
// src/Graph.ts - 增量更新
class IncrementalGraph extends Graph {
    private modifiedModules = new Set<Module>();

    async incrementalUpdate(changedFiles: string[]): Promise<void> {
        // 1. 找出受影响的模块
        const affectedModules = this.findAffectedModules(changedFiles);

        // 2. 只更新这些模块
        for (const module of affectedModules) {
            await this.updateModule(module);
        }

        // 3. 重新分析依赖
        this.reanalyseDependencies(affectedModules);

        // 4. 重新生成受影响的部分
        await this.regenerateAffectedChunks(affectedModules);
    }
}
```

## 十、错误处理和调试

### 1. **错误收集**

```typescript
// src/utils/error.ts
class RollupError extends Error {
    code: string;
    frame?: string;
    pos?: number;
    loc?: {
        file: string;
        line: number;
        column: number;
    };

    constructor(message: string, props: Partial<RollupError> = {}) {
        super(message);

        // 添加错误位置信息
        if (props.loc) {
            this.frame = this.generateCodeFrame(
                props.loc.file,
                props.loc.line,
                props.loc.column
            );
        }
    }

    private generateCodeFrame(
        file: string,
        line: number,
        column: number
    ): string {
        const lines = fs.readFileSync(file, "utf-8").split("\n");
        const start = Math.max(0, line - 3);
        const end = Math.min(lines.length, line + 3);

        return lines
            .slice(start, end)
            .map((content, index) => {
                const currentLine = start + index + 1;
                const prefix = currentLine === line ? ">" : " ";
                return `${prefix} ${currentLine}: ${content}`;
            })
            .join("\n");
    }
}
```

## 十一、总结设计模式

Rollup 源码中运用的关键设计模式：

1. **构建器模式（Builder）**：Graph 类按步骤构建模块图
2. **观察者模式（Observer）**：Watch 模式监听文件变化
3. **策略模式（Strategy）**：不同输出格式使用不同的 Finaliser
4. **责任链模式（Chain of Responsibility）**：插件钩子的执行
5. **访问者模式（Visitor）**：AST 遍历和转换
6. **备忘录模式（Memento）**：模块缓存机制

## 十二、核心性能优化点

1. **基于 AST 的静态分析**：避免执行代码
2. **增量构建**：只重新编译变更的部分
3. **智能缓存**：AST、解析结果、依赖关系
4. **并行处理**：插件钩子的并行执行
5. **懒加载**：按需解析 AST
6. **高效字符串操作**：使用 MagicString

Rollup 的源码设计体现了函数式编程思想，通过不可变数据结构和纯函数处理，确保构建过程的可预测性和可靠性。它的模块化设计使得各个部分职责清晰，易于维护和扩展。
