赵旭
zhaoxu@tedu.cn

#### AJAX

#### 1.什么是Ajax

	Asynchronous Javascript And Xml
		异步的       JS         和  Xml (JSON)
	
	同步访问:
		当客户端向服务器发送请求时，服务器在处理的过程中，浏览器只能等待
	异步访问:
		当客户端向服务器发送请求时，服务器在处理的过程中，浏览器无需等待,可以做其他操作
	
	AJAX的优点:
		1.异步 访问
		2.局部 刷新
	
	使用场合:
		1.搜索建议
		2.表单验证
		3.前后端完全分离
			SPA - Single Page Application
#### 2.AJAX核心对象 - 异步对象(XMLHttpRequest)

```
1.什么是XMLHttpRequest
		简称为 xhr
		称为 "异步对象"，代替浏览器向服务器发送异步的请求并接受响应
	2.创建异步对象
		xhr的创建是由js来提供的
		主流的异步对象时XMLHttpRequest类型的，并且主流的浏览器都支持			  (IE7+,Chrome,Firefox,Safari,Opera),但在IE低版本下是不支持XMLHttpRequest
		支持XMLHttpRequest : 
		通过new XMLHttpRequest()创建
	不支持XMLHttpRequest:
		通过new ActiveXObject("Microsoft.XMLHTTP")
	
	var xmlhttp;
	if (window.XMLHttpRequest)
	{
		//  IE7+, Firefox, Chrome, Opera, Safari 浏览器执行代码
		xmlhttp=new XMLHttpRequest();
	}
	else
	{
		// IE6, IE5 浏览器执行代码
		xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	}
	
	判断浏览器支持性:
	if(window.XMLHttpRequest){
		则说明浏览器支持 XMLHttpRequest
	}else{
		则说明浏览器支持 ActiveXObject("")
	}
		
```

​	

		
	
		1.创建一个Django程序 - AjaxDemo01
		2.创建一个网页/模板
		3.在网页/模板中创建一个函数 - createXhr()
		4.在函数中，创建异步对象并返回
			到底支持XMLHttpRequest还是ActiveXObject



#### 01.xhr的成员

```
1.方法 - open()
		作用:创建请求
		语法:xhr.open(method,url,async)
			method:请求方式,取值 'get' 或 'post'
			url:请求地址,取值为 字符串
			async:是否采用异步的方式发送请求
				true:异步
				false:同步
		示例:使用get方式向01-server的服务器端地址发送异步请求
			xhr.open("get","/01-server",true);
	2.属性 - readyState
		作用:请求状态，通过不同的请求状态来表示xhr与服务器的交互情况
			由0-4共5个值来表示5个不同的状态
			0:请求尚未初始化
			1:已经与服务器建立连接
			2:服务器端已经接受请求信息
			3:请求正在处理中
			4:响应已完成
	3.属性 - status
		作用:表示服务器端响应状态码
			200 : 服务器正确处理所有请求并给出响应
			404 : Not Found
			500 : Internal Server Error
			... ...
    示例:
            if(xhr.readyState==4 && xhr.status==200){
                //正确的接收了服务器端所有响应内容
            }
    4.属性 - responseText
        作用:表示服务器端响应回来的数据
        示例:
            if(xhr.readyState==4 && xhr.status==200){
                console.log(xhr.responseText);
            }
    5.事件 - onreadystatechange	
        作用:每当xhr的readyState值发生改变时要触发的操作 - 回调函数
        示例:
            xhr.onreadystatechange = function(){
                if(xhr.readyState==4 && xhr.status==200){
                    接收响应数据做前端业务处理
                }
            }
    6.方法 - send()
        作用:通过xhr向服务器端发送请求
        语法:xhr.send(body)
            body为请求主体
            get请求:body的值为null
                xhr.send(null)
            post请求:body的值为请求体的数据
                xhr.send("请求数据")
```

#### 2.AJAX的操作步骤

​	

```
1.GET请求
		1.创建 xhr 对象
		2.创建请求 -  open()
		3.设置回调函数 - onreadystatechange
			1.判断状态
			2.接收响应
			3.业务处理
		4.发送请求 - send()
```

		练习:
			1.创建应用 - users
			2.创建一个数据库 - ajax
			3.在 users 应用中创建一个实体类 - User
				uname - 用户名，varchar(30)
				upwd -  密码, varchar(30)
				nickname - 昵称,varchar(30)
				将实体类映射回数据库,插入测试数据
			4.创建路由-视图-模板
	
	2.POST请求













