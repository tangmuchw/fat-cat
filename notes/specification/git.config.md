# 本作者推荐在使用觉得好用的 git config 配置

> 通过命令 git config --global --edit 进行下面的配置

```Markdown
alias.st=status
alias.sh=stash
alias.sh-l=sh list
alias.sh-ay=sh apply
alias.chp=cherry-pick
alias.ct=commit -m
alias.ctmd=commit --amend
alias.br=branch
alias.rtu=remote update
alias.pl=pull
alias.mg=merge
alias.ctn=commit -n -m
alias.ph=push
alias.rbrt=rebase rt/master
alias.rb=rebase
alias.rbc=rebase --continue
alias.sh-l=sh list
alias.co=checkout
alias.lo=log --oneline --pretty=format:'%Cred%h%Creset: %C(yellow)%d%C(White)%s%C(bold magenta)<%an>%C(green)(%cr)'
alias.lg=log --stat --relative-date --decorate --pretty=format:'%Cred%h%Creset-%C(yellow)%d%C(White)%s%C(bold magenta)<%an>%C(green)(%cr)'
alias.rtp=remote prune origin
alias.tn=tag -n --sort=-taggerdate
core.ignorecase=false
push.autosetupremote=true
```
