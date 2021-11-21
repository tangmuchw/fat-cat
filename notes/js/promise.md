[toc]

# Promise: 该对象用于表示一个异步操作的最终状态（完成或失败），以及该异步操作的结果值。

## 状态：

- pending: 初始状态，既不是成功，也不是失败状态
- fulfilled: 操作成功
- rejected: 操作失败 ###回顾 Promise 的用法：

```JavaScript
  var promise = new Promise((resolve, reject) => {
    if (success) {
      resolve(data);
    } else {
      reject(error);
    }
  });
  promise.then((data) => {
    // TODO: handle success
  }, (error) => {
    // TODO: handle error
  });
```

### Simple Try

```JavaScript
  function Promise(executor){
    let self = this,
      self.status = 'pending',
      self.data = undefined,
      self.error = undefined;

    function resolve(val) {
      if (self.status === 'pending' ) {
        self.data = val;
        self.status = 'fulfilled';
        return;
      }
    }

    function reject(err) {
      if (self.status === 'pending') {
        self.error = err;
        self.status = 'rejected'
        return
      }
    }

  try {
    executor(resolve, reject);
  } catch (e) {
    reject(e)
  }

  Promise.prototype.then = function(onFulfilled, onRejected) {
    let self = this;
    let status = self.status;
    switch(status) {
      case 'fulfilled':
        onFulfilled(self.data);
        return;
      case 'rejected':
        onRejected(self.error);
        return;
      default:
        throw new Error('Unexpected state');
        return;
    }
  }
```

### Test

```Javascript
   var testPromise = new Promise(function(resolve, reject) {
     resolve('Successful operation')
   });
   testPromise.then(function(data){
     console.log(data); // output: Successful operation
   })
```

### Advanced Try

```JavaScript
  const PENDING = 'pending';
  const FULFILLED = 'fulfilled';
  const REJECTED = 'rejected';

  function Promise(executor) {
    let that = this;
    // define status
    that.status = PENDING;
    that.data = undefined;
    that.error = undefined;
    that.onFulfilledCallbacks = [];
    that.onRejectedCallbacks = [];

    function resolve(val) {
      if (val instanceof Promise) return val.then(resolve, reject);

      setTimeout(() => {
        if (that.status === PENDING) {
          that.status = FULFILLED;
          that.data = val;
          that.onFulfilledCallbacks.forEach(cd => cb(that.data))
        }
      })
    }

    function reject(error) {
      setTimeout(() => {
        if (that.status === PENDING) {
          that.status = REJECTED;
          that.error = error;
          that.onRejectedCallbacks.forEach(cd => cb(that.error))
        }
      })
    }

    try {
      executor(resolve, reject);
    } catch(e) {
      reject(e);
    }
  }

  function resolvePromise(newPromise, x, resolve, reject) {
    // Prevent x from being returned as someone else's promise
    if (newPromise === x) return reject(new TypeError('Circular reference'));

    let called;
    if (x !== null && (typeof x === 'object' || typeof x === 'function')) {
      try {
        let then = x.then;
        if(typeof then === 'function') {
          then.call(x. function(data){
            if (called) return;
            called = true;
            // Param data may still be a promise, after parsing until the return is a normal data
            resolvePromise(newPromise, data, resolve, reject);
          }, function(err) {
            if (called) return;
            called = true;
            reject(err);
          })
        }
      } catch(e) {}
    } else {
      resolve(x);
    }
  }

  Promise.prototype.then = function (onFulfilled, onRejected) {
    let that = this,
      newPromise;

    const handleFulfilled = typeof onFulfilled === 'function' ? onFulfilled : data => data;
    const handleRejected = typeof onRejected === 'function' ? onRejected : error => { throw error };

    const status = that.status;
    switch(status){
      case FULFILLED:
        return newPromise = new Promise((resolve, reject) => setTimeout(()=> {
          try {
            let fulfilledCallback = handleFulfilled(that.data);
            resolvePromise(newPromise, fulFilledCallback, resolve, reject);
          } catch (e) {
            reject(e);
          }
        }));
      case REJECTED:
       return newPromise = new Promise((resolve, reject) => setTimeout(()=> {
          try {
            let rejectedCallback = handleRejected(that.error);
            resolvePromise(newPromise, rejectedCallback, resolve, reject);
          } catch (e) {
            reject(e);
          }
        }));
    case PENDING:
      return newPromise = new Promise((resolve, reject) =>
      setTimeout(()=> {
        that.onFulfilledCallbacks.push((data) => {
          try {
              let fulfilledCallback = handleFulfilled(data);
              resolvePromise(newPromise, fulfilledCallback, resolve, reject);
            } catch (e) {
              reject(e);
            }
          });
        that.onRejectedCallbacks.push((error) => {
          try {
              let rejectedCallback = handleRejected(error);
              resolvePromise(newPromise, rejectedCallback, resolve, reject);
            } catch (e) {
              reject(e);
            }
          });
        }));
    }
  }

  Promise.prototype.catch = function(callback) {
    return this.then(null, callback);
  }

  Promise.prototype.finally = function(onFinally){
    return this.then(
      res => Promise.resolve(onFinally()).then(() => res),
       err => Promise.reject(onFinally()).then(() => { throw err
       })
    )
  }

  Promise.all = function(promises) {
    // TODO: handle TypeError('Promises not iterable')
    return new Promise((resolve, reject) => {
      let results = [],
        account = 1;

      function processData(index, ret) {
        results[index] = ret;
        if(++account == promises.length) resolve(results);
      }

      for(let key = 0; key < promises.length; key++) {
        promises[key].then((ret) => processData(key, ret), reject)
      }
    });
  }

  Promise.race = function(promises) {
    return new Promise((resolve, reject) => {

      for(let key = 0; key < promises.length; key++) {
         // 这里使用 Promise.resolve 包了一下，以防传递了 non-promise
        Promise.resolve(promises[key]).then(res => resolve(res), err => reject(err))
      }
    });
  }

  // Generate a successful promise
  Promise.resolve = function(val) {
    return new Promise(function(resolve, reject) {
      resolve(val);
    })
  }

   // Generate a failed promise
  Promise.reject = function(err) {
    return new Promise(function(resolve, reject) {
      reject(err);
    })
  }
```
