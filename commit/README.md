# commit lint

> 详见： https://github.com/conventional-changelog/commitlint

-   build
-   ci
-   chore: 比较杂的内容相关
-   docs: 文档/文献相关
-   feat
-   fix
-   perf: 性能相关
-   refactor: 重构相关
-   revert: 重提相关
-   style
-   test

## 解决 git 命令删除远程分支后，本地 git branch -a 仍能看到已删除的分支问题

-   git remote show origin 查看远程库，看到远程分支和本地分支的对应关系；
-   git remote prune origin 删除远程没有，本地有的分支；
