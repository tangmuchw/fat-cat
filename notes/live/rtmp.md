# RTMP 协议

> RTMP: Real Time Messaging Protocol（实时消息传输协议）

- 是流媒体协议
- RTMP 协议是 Adobe 的私有协议，未完全公开
- RTMP 协议一般传输的是 flv，f4v 格式流
- RTMP 一般在 TCP 1 个通道上传输命令和数据

# 步骤

- url 通过 blob 转化， 回填到 video 标签 src 下
- redirectStream （Content-Type: application/x-mpegURL;charset=ISO-8859-1）.m3u8 转到 http2 获取对应的 ts 格式流媒体
