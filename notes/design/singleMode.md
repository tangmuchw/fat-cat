# 单例模式

```JavaScript
var LazySingle = (function(){
    // 单例实力引用
    var _instance = null

    // 单例
    function Single(){
        // 对应使用 new Single()
        // this.publicMethod = function(){}
        // this.publicProperty = '1.0'

       return {
            publicMethod: function(){},
            publicProperty: '1.0'
        }
    }

    // 获取单例对象接口
    return  function() {
        if(!_instance) {
            // _instance = new Single()
            _instance = Single()
        }

        return _instance
    }
})()

console.log(LazySingle().publicProperty) // 1.0

```
