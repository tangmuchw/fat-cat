# Commit Message 规范

## 如何优雅的开发（针对同一 feature，非通用流程，此模块主要目的是讲解怎么将多个 commit 合成一个）

> 项目开发 owner 会把项目分支划分为 master，dev，test 和 preprod，这 4 个基础分支，只有 owner 可以直接进行代码操作，其他开发者，需以 mr 的方式来合到对应的分支上，更新代码

-   master：主分支，始终与生产环境保持一致
-   dev：开发分支，用于功能开发
-   test：测试分支，多提供于测试人员测试使用
-   preprod：预发布分支，多用于 owner 打 tag 使用
-   功能分支合并的流程：chw/xxx => fe/xxx => test => preprod => master 或者 chw/xxx => fe/xxx => preprod => master，具体合到哪个 测试分支 由 owner 决定，绝不允许反向 merge，即 preprod => test，理论是不允许的。 最后由 owner 手动同步这 4 个基础分支

> 项目开发 owner 会根据功能需求基于 dev 新建功能分支 fe 和 bugfix 分支 fix，这个两种类型的分支可以直接进行代码操作的权限可由 owner 根据实际情况决定

-   fe/xxx: 功能分支
-   fix/xxx: bugfix 分支

## 开始开发（单人开发）

本地分支可以 checkout 到 fe/xxx 直接开发
更新远程代码，可以按照 「多人协作开发之更新本地代码」 的方式更新，也可以直接使用 git pull 更新代码
然后按照流程去创建 mr 即可，创建 mr 的时候，有可能出现 dev 分支有新的更新，fe/xxx 落后了，即需要按照 「多人协作开发之更新本地代码」的方式更新，但注意的是此时的 rebase 的远程分支为 dev 了

## 开始开发（多人协作开发）

本地新建自己的功能分支，举个栗子：chw/xxx，命名规则：{名字拼音缩写}/xxx
一顿操作后，要提交代码了
本地提交 commit，commit message 请按「如何提交规范的 commit message」的规范书写

-   更新本地代码 chw/xxx 分支
-   检查远程分支 fe/xxx 是否有更新，运行命令：git remote update (推荐)或者 git fetch
-   若 fe/xxx 有更新 - 运行命令：git rebase origin/fe/xxx - 若有冲突，解决冲突后，运行以下命令：
    -   git add .
    -   git rebase --continue
    -   若还有冲突，重复以上步骤，即 解决冲突，git add . ，git rebase --continue，直到没有冲突
    -   若没有冲突，检查一下 git log，确认一下本次修改，commit 是否正确否 运行命令: git log --oneline
    -   Congratulation！你更新本地代码成功
    -   若 fe/xxx 没有更新，直接 push 本地分支到远程上
        -   第一次 push：git push --set-upstream origin chw/xxx
            远程已有本地同名分支：git push
        -   一顿操作后，功能都开发完成了，要提 mr 了，需要自己整合一下 commit，保证 commit 的个数不要太多，暂时界定不超过 5 个（以项目开发 owner 实际界定为准）
        -   **git rebase -i HEAD~{num}**: 将多个 commit 合成一个 commit
            整理完 commit 后，然后就可以提 mr 了， 按「如何提交规范的 commit message」的规范写明 mr 的标题

## 如何提交规范的 commit message

> 基于 commitlint 所定的规则统一 commit message

### 通用 commit message 表达式：

> type(optional scopes): [optional pingCodeId] subject // tips: 注意空格

-   type：表明本次 commit 的操作属性，其取值可参考下表 「Type 使用场景」
-   optional scopes：可选的，表明影响的范围；多个影响范围时，使用 “,” 分割
-   optional pingCodeId：可选的，pingCode 对应的 task/bug/story 的 ID ，多个 pingCodeId 时，使用 “,” 分割（\*pingCodeId 的是否填写，唯一的标准是：明确 owner 打 tag 的时候，需要写进发行说明里，则必须填有 pingCodeId，否则可以不填写）
-   subject：表明具体的改动说明，也可以在 subject 里标明影响范围

### 部分场景举个栗子：

场景说明 Commit Message 英文举例 Commit Message 中文举例 备注

-   项目：某个购物网站
-   需求： 在 xxx 页面新增商品列表
    -   feat(xxx): add product list
    -   feat(xxx): 新增商品列表

## Type 使用场景

| type     | 使用解释                                                                           |
| -------- | ---------------------------------------------------------------------------------- |
| feat     | 增加新功能                                                                         |
| fix      | 修复 bug                                                                           |
| chore    | 其他修改，比如增加依赖库、工具 或者 一些业务逻辑的调整等                           |
| merge    | 多用于版本跨度较大时，手动触发 git merge，解决冲突后的提交，必要时需要注明影响范围 |
| style    | 代码格式修改，注意不是 css 样式的修改                                              |
| docs     | 文档修改                                                                           |
| ci       | 持续集成修改                                                                       |
| build    | 编译相关的修改，例如发布版本、对项目构建或者依赖的改动                             |
| perf     | 优化相关，比如提升性能、体验等                                                     |
| refactor | 代码重构                                                                           |
| revert   | 撤销某次提交，回滚到某个版本                                                       |
| test     | 测试用例                                                                           |

## commitlint.config.js 通用配置

```JavasScript
module.exports = {
    extends: ['@commitlint/config-conventional'],
    rules: {
    'type-enum': [
        2,
        'always',
        [
            'feat',
            'fix',
            'chore',
            'merge',
            'style',
            'docs',
            'ci',
            'build',
            'perf',
            'refactor',
            'revert',
            'test',
        ],
        ],
            'header-max-length': [2, 'always', 150],
        },
}
```
