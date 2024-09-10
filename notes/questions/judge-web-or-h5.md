# 同一个链接，PC 打开的是 web 应用，手机打开的是 h5 应用

```Javascript
document.addEventListener('DOMContentLoaded', () => {
  const userAgent = navigator.userAgent || navigator.vendor || window.opera;

  // 检测移动设备
  const isMobile = /android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini/i.test(userAgent.toLowerCase());

  const href = isMobile ? 'https://h5' : 'https://web'
  window.location.href = href;
});

```
