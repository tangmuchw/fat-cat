#instanceof: 用于测试构造函数的 prototype 属性是否出现在对象的原型链中的任何位置。
<br />

###Test

```Javascript
  function instanceOf(child, parent) {
    let proto = child.__proto__;
    let prototype = parent.prototype;
    while(true) {
      if(proto === null) return false;
      if(proto === prototype) return true;
      proto = proto.__proto__;
    }
  }
```
