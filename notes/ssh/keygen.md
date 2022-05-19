# mac 上生成以及查看 ssh-key

- ssh-keygen -t rsa -f ~/.ssh/id_rsa.xxx -C 'email'

  > <code>id_rsa.xxx</code>是我们指定的文件名，这时~/.ssh 目录下会多出 id_rsa.xxx 和 id_rsa.xxx.pub 两个文件，id_rsa.xxx.pub 里保存的就是我们要使用的 key

- cd ~/.ssh
- touch config
- 配置 config, 如下所示

```JavaScript
Host *.xxx.com
  IdentityFile ~/.ssh/id_rsa.xxx
  user xxx
```
