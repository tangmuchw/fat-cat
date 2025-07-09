# database v1.0.0

## 用户表 users

<style>
table { width: 100%;text-align: center; }
th:nth-child(1) { width: 120px }
th:nth-child(2) { width: 120px; }
th:nth-child(3) { width: 200px }
</style>

> 记录当前登录的用户信息
> 权限：所有用户可读、创建者可读写

| 字段名    | 类型   | 说明                                |
| --------- | ------ | ----------------------------------- |
| nickName  | string | 用户昵称                            |
| avatarUrl | string | 用户头像地址                        |
| openid    | string | 微信小程序用户标识 id               |
| bearid    | string | 熊熊卡小程序用户 id                 |
| updatedAt | Date   | 更新时间，日期类型存储              |
| createAt  | Date   | 创建时间，日期类型存储              |
| expiredAt | Date   | 过期时间，日期类型存储，默认为 7 天 |

## 送卡记录表 sent_card_records

> 权限：所有用户可读、创建者可读写

| 字段名                    | 类型   | 说明                                                                                                       |
| ------------------------- | ------ | ---------------------------------------------------------------------------------------------------------- |
| sentId                    | string | 送卡记录 id，唯一标识                                                                                      |
| senderOpenid              | string | 送卡人的用户 ID 或唯一标识，统一使用 openid                                                                |
| status                    | string | 送卡的状态：已创建 created，已发卡 sent，已收卡 received，已过期 expired，已撤回 canceled，已拒绝 rejected |
| recipientOpenid           | string | 收卡人的用户 ID 或唯一标识，统一使用 openid                                                                |
| cardId                    | string | 卡的 id                                                                                                    |
| cardNumber                | string | 卡的编号，用于唯一标识每张卡                                                                               |
| checkedNotifySignedStatus | number | 是否勾选了通知签收状态, 0 未勾选，1 勾选                                                                   |
| createAt                  | Date   | 创建时间，日期类型存储                                                                                     |
| updatedAt                 | Date   | 更新时间，日期类型存储                                                                                     |
| sentAt                    | Date   | 送卡时间，日期类型存储                                                                                     |
| expiredAt                 | Date   | 过期时间，日期类型存储                                                                                     |
| finalAt                   | Date   | 终态时间，日期类型存储，当 状态 为 已撤回，已拒绝，已签收 时，记录当前操作时间                             |

<!-- | canceledAt                | Date   | 撤回时间，日期类型存储                                                                                     |
| rejectedAt                | Date   | 拒绝签收时间，日期类型存储                                                                                 |
| receivedAt                | Date   | 签收时间，日期类型存储                                                                                     | -->

## 卡面表 cards v1.0.4

> 权限：所有用户可读、创建者可读写

| 字段名       | 类型   | 说明                                                                                                                           |
| ------------ | ------ | ------------------------------------------------------------------------------------------------------------------------------ |
| id           | string | 卡的 id，唯一标识                                                                                                              |
| status       | string | 卡的状态, 下线 offline, 上线 online, coming 待上线                                                                             |
| categoryCode | string | 卡分类，如 职场突围                                                                                                            |
| categoryName | string | 卡分类名称，                                                                                                                   |
| categoryDesc | string | 卡分类描述，                                                                                                                   |
| typeCode     | string | 卡类型，例如：感谢卡 thanks, 道歉卡 sorry, 鼓励卡 encourage, 拒绝卡 reject, 夸夸卡 praise, 自嘲卡 selfMockery, 纪念卡 souvenir |
| typeName     | string | 卡类型名称                                                                                                                     |
| themeCode    | string | 主题编码，用与标识卡不同风格的卡，感谢卡类型 0001                                                                              |
| themeName    | string | 主题名称名称                                                                                                                   |
| themeDesc    | string | 主题说明称                                                                                                                     |
| honoree      | string | 致敬对象，如 致：亲爱的同事                                                                                                    |
| content      | string | 正文内容                                                                                                                       |
| title        | string | 正文标题，如：亲爱的同事                                                                                                       |
| cover        | string | 卡封面图片                                                                                                                     |
| createAt     | Date   | 创建时间，日期类型存储                                                                                                         |
| updatedAt    | Date   | 更新时间，日期类型存储                                                                                                         |

<!-- | salePrice    | string | 卡售价，暂时先定义，当前没有支付                                                                                               | -->
<!-- | isHot        | number | 是否热门推荐，0 否，1 是                                                                                                       | -->
<!-- | copywriting  | string | 公关文案，用于做一些承诺，如"永久有效 \| 编号唯一"                                                                             | -->

## 意见反馈表 feedbacks

> 权限：仅创建者可读写

| 字段名    | 类型   | 说明                                              |
| --------- | ------ | ------------------------------------------------- |
| openid    | string | 用户 ID                                           |
| fromWhere | string | 来自哪里, msg-board 留言板, preview-card 预览卡片 |
| content   | string | 反馈内容                                          |
| extraInfo | Object | 额外信息, preview-card 时, 存有 cardId            |
| createAt  | Date   | 创建时间                                          |

## 修改记录表 edit_logs

> 权限：所有用户不可读写

| 字段名   | 类型   | 说明                             |
| -------- | ------ | -------------------------------- |
| openid   | string | 用户 ID                          |
| editedAt | Date   | 修改时间                         |
| editType | string | 修改类型， user_profile 用户信息 |

## 配置表 configs

> 表里 只有 一个文档，存下所有系统相关配置信息
> 权限：所有用户可读

| 字段名        | 类型   | 说明                                                       |
| ------------- | ------ | ---------------------------------------------------------- |
| scrollingText | object | 跑马灯文字，在首页展示，{ show: boolean, content: string } |

honorific
