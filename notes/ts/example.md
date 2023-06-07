```TypeScript
interface GenerateMsgData {
    a: {
        field: string;
    };
    b: {
        field: string;
    };
    c: {
        field: string;
    };
}

const doSomething = <
    K extends keyof T,
    T = GenerateMsgData
  >(type: K, meta: T[K]) => {
      switch(type){
          case 'a': {

            const {} = (meta as unknown)  as GenerateMsgData["a"];
            // do something
            break;
          }
          case 'b':
          case 'c':
          default:
          break;

      }
  }


```
