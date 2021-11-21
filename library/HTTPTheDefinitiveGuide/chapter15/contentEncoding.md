[toc]

# 内容编码类型

> Content-Encoding 首部就用标准化的代号来说明编码时使用的算法

## 内容编码代号

| Content-Encoding 值 | 描述                                                                     |
| ------------------- | ------------------------------------------------------------------------ |
| gzip                | 表明实体采用 CNU zip 编码                                                |
| compress            | 表明实体采用 Unix 编码                                                   |
| deflate             | 表明实体采用 zlib 编码                                                   |
| identity            | 表明没有对实体进行编码。当没有 Content-Encoding 首部时，就默认为这种情况 |

# Accept-Encoding 首部

> 为了避免服务器使用客户端不支持的编码方式，客户端就把自己支持的内容编码方式列表放在请求的 Accept-Encoding 首部里发出去

## 举例

- Accept-Encoding：\*
- Accept-Encoding： compress;q=0.5, gzip;q=1.0

> 客户端可以给每种编码附带 Q （质量）值参数来说明编码的优先级
