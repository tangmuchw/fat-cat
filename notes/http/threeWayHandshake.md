[toc]

# 三次握手(three-way handshake):
<br />
### Why?
- IP是位于网络层的无连接的通讯协议，IP协议只负责将IP包发送给目的地，但不确保发送到目的地，所以在**传输层采用有连接的方式，来确保数据的送达**。
- 三次握手之所以是三次，是为了保证 client 和 server 均让对方知道自己的接收能力和发送能力没问题而保证的最小次数。

### How to do？

#### Handshake:

- The first time: client => server, 只能 server 端判断出 client**具备**发送能力。
- The secondary time: server => client, client 就可以判断出 server 端**具备**发送和接收能力，**此时 client 还需让 server 端知道自己接收能力没问题于是有了 the third time**。
- The third time: client => server, 双方均保证自己的接收和发送能力没有问题

notice: **其中，为了保证后续的握手是为了应答上一个握手，每次握手都会带一个标识 seq， 后续的 ACK 都会对这个 seq 进行加 1 来进行确认**

#### Wave

- the fourth wave: 主要是用于关闭链接时，当 server 端收到 FIN 报文时，很可能并不会立即关闭 SOCKET,所以智能先回复 ACK 报文，告诉 client，"你发的 FIN 报文我收到了"，只有等到我 server 端所有的报文都发完了，我才能发送 FIN 报文。

#### Keywords

- seq: 序列号, 占 4 个字节，用来标记数据段的顺序
- ACK: 确认号， 占 4 个字节， 期待收到对方下一个报文段的第一个数据字节的序号， 一般 ACK = seq + 1
- SYN: 链接建立时用于同步序号
- PSH: 提示接收端应用程序立即从 TCP 缓冲区把数据读走
- FIN: 希望断开
