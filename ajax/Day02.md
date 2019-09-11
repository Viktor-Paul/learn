#### 1.使用Ajax发送POST请求

```
1.创建xhr
	2.创建请求 
	  1.将请求方式更改为post
		2.如果有请求参数不能拼在url之后
	3.设置回调函数
	4.设置请求消息头
		xhr.setRequestHeader("Content-Type","application/x-www-form-urlencoded")
	5.发送请求
		xhr.send("name=value&name1=value1");
```

#### 2.JSON

```text
1.介绍JSON
		JSON:JavaScript Object Notation
		     JS         对象   表现方式
		以JS对象的格式来约束前后端交互的字符串数据
	2.JSO - JS对象
		var obj = {
			uname:"wangwc",
			uage:30,
			ugender:"男"
		}
	3.JSON规范
		1.使用JSON表示单个对象
			1.使用 {} 表示一个对象
			2.在{}中使用 key:value 来表示属性(数据)
			3.key必须使用 "" 引起来
			4.value如果是字符串的话，也必须使用""引起来
			5.多对 key:value 之间使用 , 分隔
示例:
			var obj = '{"uname":"wangwc","uage":30}';
        2.使用JSON表示一组对象
            使用 [] 表示一组对象
            示例:
                var users = '[{"uname":"wangwc","uage":30},{"uname":"weimz","uage":40}]';
    4.前端中处理JSON
        var js对象 = JSON.parse(JSON串);

    5.后端中处理JSON
        1.在Python中的处理
            1.允许将 元组，列表，字典 转换成JSON串
            2.元组，列表，字典中可以是字符串也可以是元组，列表和字典

            python中提供了json模块，json模块中提供dumps方法实现JSON串的转换
        2.在Django中的处理
            使用Django中提供的序列化类来完成QuerySet到JSON字符串的转换

            from django.core import serializers
            str = serializers.serialize('json',QuerySet)
            return HttpResponse(str)
```

```json
[
	{
		"model": "users.user", 
		"pk": 1, 
		"fields":
        {
			"uname": "wangwc", 
			"upwd": "wangwc", 
			"nickname": "TeacherWang"
		}
	}, 
	{
		"model": "users.user", 
		"pk": 2, 
		"fields": 
		{
			"uname": "lvze", "upwd": "maria", 			
			"nickname": "\u5415\u6cfd\u739b\u5229\u4e9a"
		}
	}, 
	{
		"model": "users.user", 
		"pk": 3, 
		"fields": 
		{
			"uname": "weimz", "upwd": "123456", 
			"nickname": "\u9b4f\u8001\u5e08"
		}
	}, 
	{
		"model": "users.user",
        "pk": 4, 
        "fields": 
        {
        	"uname": "wangwc", "upwd": "123456", 
        	"nickname": "\u738b\u8001\u5e08"
        }
    }, 
    {
    	"model": "users.user",
        "pk": 5, 
        "fields": 
        {
            "uname": "qtx", "upwd": "qtx", 
            "nickname": "\u7941\u8001\u5e08"
        }
     }
 ]
```







