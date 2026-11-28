# JSON-LD
> 由 DeepSeek 整理生成
JSON-LD（**JavaScript Object Notation for Linked Data**）是一种基于 JSON 的**结构化数据格式**，用于将网页内容以机器可读的方式表达出来，帮助搜索引擎、AI 爬虫等工具准确理解页面信息。它由 W3C 标准化，是 Schema.org 结构化数据的**首选推荐格式**，也是当前业界事实上的主流方案。

---

### 🧠 核心概念：`@context` 与 `@type`

JSON-LD 的灵魂在于**上下文（context）** 和**类型（type）**，二者共同规定了“用什么词汇表来描述什么事物”。

- **`@context`**：声明所使用的词汇表，通常指向 `https://schema.org`。一旦声明，后续所有键名都自动从该词汇表中解释。
- **`@type`**：指定当前描述实体的类型，如 `Person`、`Organization`、`Article`、`FAQPage` 等。`@type` 是保留键，其值必须是完整的类型 URI 或 URI 片段。

一个最基本的骨架如下，通常放在 HTML 的 `<head>` 或 `<body>` 末尾的 `<script>` 标签中：

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "John Doe",
  "jobTitle": "Graduate research assistant"
}
</script>
```

---

### ⚡ 为什么选择 JSON-LD？

在 Schema.org 支持的三种嵌入语法（Microdata、RDFa、JSON-LD）中，JSON-LD 成为主流选择，原因在于：

1. **与 HTML 结构彻底解耦**：JSON-LD 是独立的 `<script>` 块，不需要侵入正文 DOM，CMS 改造成本最低。
2. **可维护性强**：数据变更只需修改 JSON 内容，无需改动页面模板。
3. **官方与生态一致推荐**：Google 官方推荐，主流搜索引擎和 AI 爬虫的解析器也普遍优先支持。

---

### 🧱 常用 Schema 类型与写法

不同页面类型对应不同的 Schema。以下是最常用的几种及其典型字段与示例。

#### 🏢 Organization（品牌实体身份）

用于声明品牌/机构的实体身份，是 AI 进行实体消歧的关键锚点。核心字段包括 `name`、`url`、`logo`、`sameAs`（全网官方账号链接列表）等。

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "品牌名",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "sameAs": [
    "https://www.zhihu.com/org/你的机构号",
    "https://baike.baidu.com/item/你的词条"
  ]
}
</script>
```

`sameAs` 字段尤其重要，它是告诉爬虫“这些不同平台上的账号指向同一个实体”的**实体对齐信号**。

#### ❓ FAQPage（问答对）

FAQPage 是结构化数据中**投入产出比最高**的类型之一，因为用户向 AI 提出的问题与 FAQ 中的问题天然同构，检索命中率和抽取准确率都很高。核心结构是 `mainEntity` 数组，每项包含一个 `Question` 及其 `acceptedAnswer`。

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "支持私有化部署吗？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "支持。可提供本地部署与专属云两种方案。"
      }
    }
  ]
}
</script>
```

**实战要点**：`Question.name` 应使用**用户的真实问法**（如“怎么收费”优于“商业模式咨询”）；`Answer.text` 的**第一句必须直接给出结论**，因为 AI 抽取时最常用首句。

#### 📄 Article（文章页）

博客、新闻等内容页的基础标记，核心字段包括 `headline`、`author`、`datePublished`、`dateModified`、`publisher`。

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "文章标题",
  "author": { "@type": "Person", "name": "作者名" },
  "datePublished": "2026-10-08",
  "dateModified": "2026-10-08",
  "publisher": { "@type": "Organization", "name": "站点名称" }
}
</script>
```

`dateModified` 对于检索型 AI 判断内容时效性很有价值，内容实质更新后应同步更新该字段。

#### 🛒 Product / Service（商品或服务）

实物用 `Product`，服务用 `Service`。核心思路是将“能做什么、怎么收费、什么限制”写成显式字段，避免 AI 从文案中猜测。

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "服务名称",
  "serviceType": "品类定位",
  "provider": { "@type": "Organization", "name": "品牌名" },
  "offers": {
    "@type": "Offer",
    "priceSpecification": {
      "@type": "PriceSpecification",
      "description": "免费检测档；正式服务按需报价"
    }
  }
}
</script>
```

若不便公开精确价格，可用 `PriceSpecification.description` 写明**价格结构**（有哪些档、按什么计价），这比缺失定价信息好得多，能给 AI 一个官方口径可引。

#### 🧭 BreadcrumbList（面包屑导航）

用于声明页面的层级路径，使搜索结果中可能显示“首页 > 分类 > 当前页”的导航信息。核心是 `itemListElement` 数组，每项包含 `position`、`name` 和 `item`（URL）。

---

### 🔗 进阶：`@graph` 与 `@id` 组织多实体

当一个页面需要声明**多个平行实体**（如 Organization、WebSite、WebPage）时，用 `@graph` 将它们放在同一个 `script` 块中，并通过稳定的 `@id` 互相引用，是 Schema.org 官方认可的多实体标记方案。

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://example.com/#org",
      "name": "品牌名"
    },
    {
      "@type": "WebSite",
      "@id": "https://example.com/#website",
      "name": "站点名",
      "publisher": { "@id": "https://example.com/#org" }
    }
  ]
}
```

`@id` 只是一个标识符，不要求对应的 URL 真实可访问；约定俗成的做法是使用自己域名下的片段（如 `#org`）作为稳定标识。这种“分开定义、`@id` 关联”的方式，比强行嵌套更符合语义规范，也更利于搜索引擎解析。

---

### ✅ 验证工具

配置完成后，建议进行三步验证：

1. **语法校验**：使用 **Google Rich Results Test**（`search.google.com/test/rich-results`）或 **Schema.org Validator**（`validator.schema.org`），贴入 URL 或代码检查解析结果。
2. **抓取模拟**：用 `curl` 带上 AI 爬虫的 User-Agent 请求页面，确认 JSON-LD 出现在 **HTML 源码**中（而非 JS 动态注入），例如：
   ```bash
   curl -s -A "GPTBot" https://example.com/faq | grep -o 'application/ld+json'
   ```
3. **效果观察**：查看服务器日志中 AI 爬虫对标记页面的抓取频次，或将页面 URL 交给支持联网的 AI，对比其抽取结果与标记内容是否一致。

---

### ⚠️ 常见坑与避坑指南

- **标记与可见内容不一致**：JSON-LD 中标了什么，页面上就必须有对应的可见内容。标了 `aggregateRating` 却看不到评分，会被判定为结构化数据作弊，严重的会导致处罚。
- **由前端 JS 动态注入**：不执行 JavaScript 的爬虫无法获取 JSON-LD 内容。应通过 SSR 输出，或直接写死在模板中。
- **嵌套实体断链**：例如 FAQPage 中引用了 Organization 的 `@id`，但 Organization 的 `url` 写错域名，导致实体对齐失败，标记效果大打折扣。
- **堆砌无关 Schema**：每页只标记与当前内容直接相关的类型，一篇文章同时塞入 Product、Recipe、JobPosting 等多种类型，反而显得不自然，可能适得其反。

---

总结来说，JSON-LD 的本质是**把“希望机器如何理解你的页面”从模糊的文本中抽出来，变成一份显式的、结构化的声明**。无论是传统 SEO 中的富媒体摘要，还是生成式搜索中 AI 对事实的准确抽取，JSON-LD 都是当前最直接、成本最低的技术杠杆。
