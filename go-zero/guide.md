## model 层

新建一个 <code>xxx.sql</code> 文件

```
CREATE TABLE user (
    id bigint AUTO_INCREMENT,
    name varchar(255) NULL COMMENT 'The username',
    password varchar(255) NOT NULL DEFAULT '' COMMENT 'The user password',
    mobile varchar(255) NOT NULL DEFAULT '' COMMENT 'The mobile phone number',
    gender char(10) NOT NULL DEFAULT 'male' COMMENT 'gender,male|female|unknown',
    nickname varchar(255) NULL DEFAULT '' COMMENT 'The nickname',
    type tinyint(1) NULL DEFAULT 0 COMMENT 'The user type, 0:normal,1:vip, for test golang keyword',
    create_at timestamp NULL,
    update_at timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE mobile_index (mobile),
    UNIQUE name_index (name),
    PRIMARY KEY (id)
) ENGINE = InnoDB COLLATE utf8mb4_general_ci COMMENT 'user table';
```

执行 goctl
goctl model mysql ddl --src user.sql --dir .

```
# 列出当前目录下的文件
$ ls
user.sql         usermodel.go     usermodel_gen.go vars.go
# 查看目录树
$ tree
.
├── user.sql
├── usermodel.go
├── usermodel_gen.go
└── vars.go

0 directories, 4 files
```
