mongodb

**1.进入mongodb**

```
* 安装位置： /var/lib/mongodb..
				* 配置文件： /etc/mongodb.conf
				* 命令集：  /usr/bin
				
* 进入mongodb交互界面
  名称 ： mongodb shell
  命令 ： mongo
  退出 ： quit()    ctrl-c
```

**2.数据库的操作**

```
创建库
use 库名
删除库
db.dropDatabase()
查看所有库
show dbs

# 数据库的备份和恢复
mongodump -h [host] -d [db] -o [path]
e.g. 将本机 stu 数据库备份在 当前目录下
mongodump -h 127.0.0.1 -d stu -o  .
恢复命令：
mongorestore -h [host:port] -d [db]  [bak]
e.g. 将stu备份 恢复到本机student数据库中
mongorestore -h 127.0.0.1:27017 -d student stu

# 创建集合
db.createCollection(name, options)
参数说明：

name: 要创建的集合名称
options: 可选参数, 指定有关内存大小及索引的选项
options 可以是如下参数：

字段	类型	描述
capped	布尔	（可选）如果为 true，则创建固定集合。固定集合是指有着固定大小的集合，当达到最大值时，它会自动覆盖最早的文档。
当该值为 true 时，必须指定 size 参数。
autoIndexId	布尔	（可选）如为 true，自动在 _id 字段创建索引。默认为 false。
size	数值	（可选）为固定集合指定一个最大值（以字节计）。
如果 capped 为 true，也需要指定该字段。
max	数值	（可选）指定固定集合中包含文档的最大数量。

# 查看所有集合
show collections

# 集合的重命名
db.集合名.renameCollection(newname)

# 删除集合
db.collection.drop()


# 插入文档
db.集合名.insertOne(doc)
db.集合名.insertMany(doc)

doc代表[{},{},{}....]

db.集合名.save()
如果_id重复,会替换掉原有的文档


# 删除文档
remove() 方法的基本语法格式如下所示：

db.collection.remove(
   <query>,
   <justOne>
)
如果你的 MongoDB 是 2.6 版本以后的，语法格式如下：

db.collection.remove(
   <query>,
   {
     justOne: <boolean>,
     writeConcern: <document>
   }
)
参数说明：

query :（可选）删除的文档的条件。
justOne : （可选）如果设为 true 或 1，则只删除一个文档，如果不设置该参数，或使用默认值 false，则删除所有匹配条件的文档。
writeConcern :（可选）抛出异常的级别。


# 查找
db.集合名.find(query,field)
query代表查找条件
field代表查找的域

e.g.  查找所有年龄18的文档，只查找name，age域
    db.class0.find({age:18},{_id:0,name:1,age:1})
    
query操作符的使用
1】 $eq  等于  = 	
e.g.  年龄等于17 
db.class0.find({age:{$eq:17}},{_id:0})		
【2】 $lt  小于  < 		
e.g. 字符串可以比较大小
db.class0.find({name:{$lt:'Tom'}},{_id:0})
【3】 $gt  大于  >
e.g. 查找一个区间范围
db.class0.find({age:{$gt:17,$lt:20}},{_id:0})
【4】 $lte  小于等于  <=
【5】 $gte  大于等于  >=
【6】 $ne   不等于    !=
【7】 $in   包含
e.g. 查找年龄在数组范围的
db.class0.find({age:{$in:[17,19,21]}},{_id:0})
【8】 $nin  不包含
e.g. 查找年龄不在数组范围的
db.class0.find({age:{$nin:[17,19,21]}},{_id:0})


逻辑操作符
【1】 $and   逻辑与	 
e.g.  查找年龄小于19 并且性别为w的
db.class0.find({$and:[{age:{$lt:19}},{sex:{$ne:'w'}}]},{_id:0})
* query中的多个条件本身也表示并且关系
【2】 $or  逻辑或	 
e.g.  查找年龄大于18或者性别为w
db.class0.find({$or:[{age:{$gt:18}},{sex:'w'}]},{_id:0})
【3】 $not  逻辑非	
e.g. 查找年龄不大于18的
db.class0.find({age:{$not:{$gt:18}}},{_id:0})
【4】 $nor 既不也不(多个条件均为假则结果为真)
e.g.  年龄不大于18 性别不为 m
db.class0.find({$nor:[{age:{$gt:18}},{sex:'m'}]},{_id:0})
【5】 混合条件语句 
年龄大于等于19或者小于18  并且 性别为 w
db.class0.find({$and:[{$or:[{age:{$gte:19}},{age:{$lt:18}}]},{sex:'w'}]},{_id:0}
（年龄大于等于17的男生） 或者  (姓名叫 Abby 或者Emma)
db.class0.find({$or:[{age:{$gte:17},sex:'m'},{name:{$in:['Abby','Emma']}}]},{_id:0})


数组操作符	 
【1】 查找数组中包含元素
e.g.  查找score数组中元素包含大于90的文档
db.class2.find({score:{$gt:90}},{_id:0})
【2】 $all  查找数组中同时包含多项
e.g. 查找数组中同时包含87,89的文档
db.class2.find({score:{$all:[87,89]}},{_id:0})
【3】 $size 根据数组的元素个数查找
e.g.  查找数组中包含3个元素的文档
db.class2.find({score:{$size:3}},{_id:0})
【4】 $slice 用于field参数，表示查找数组哪些项
e.g.  查找数组中的前两项
db.class2.find({},{_id:0,score:{$slice:2}})
e.g.  跳过数组第一项，查看后面两项
db.class2.find({},{_id:0,score:{$slice:[1,2]}})
【5】 通过数组索引进行查找
e.g.  查找数组第二项大于80的文档
db.class2.find({'score.1':{$gt:80}},{_id:0})
* 通过score.1表示第二项，需要加引号表达
其他操作符
【1】 $exists  判断一个域是否存在
e.g.  查找有sex域的文档
db.class0.find({sex:{$exists:true}},{_id:0})
【2】 $mod   根据除数余数筛选
e.g. 查找age 除以 2 余数为1的文档
db.class0.find({age:{$mod:[2,1]}},{_id:0})
【3】 $type  根据数据类型筛选
e.g.  查找 age域值为 字符串类型的
db.class2.find({age:{$type:2}},{_id:0})
* 数据类型与数字对应查看type表


二. 数据操作函数

	1. db.collection.distinct(field)
	   功能: 获取集合中某个域的值范围
		 参数： 域名
		 返回值： 取值的范围 数组
     
		 e.g. 查找class0 age域有哪些值
		 db.class0.distinct('age')
	
	2. pretty() 
		 功能: 将find结果格式化显示
	
	3. limit(n)
		 功能: 显示查询结果的前n条
		 
		 e.g.  显示查询结果前3条
		  db.class0.find({},{_id:0}).limit(3)
	
	4. skip(n)
		 功能 ： 跳过前n条显示后面的文档

    e.g. 跳过前5个文档，显示后面内容
		db.class0.find({},{_id:0}).skip(5)

  5. count()
	   功能: 统计查询结果数量
		
		 e.g.  统计年龄大于18的文档个数
		 db.class0.find({age:{$gt:18}},{_id:0}).count()

	6. sort({field:1/-1})
		 功能: 对查找结果排序
		 参数: field 表示排序的域，1升序  -1降序
     
		 e.g.  年龄为数字的域按照降序排序
		 db.class0.find({age:{$type:1}},{_id:0}).sort({age:-1})

		 e.g.  复合排序（第一排序项相同的时候按照第二项排序）
		 db.class0.find({age:{$type:1}},{_id:0}).sort({age:1,name:1})

  7. 函数连续调用
	   
		 如果上一个函数返回的仍是一个文档集合则可以继续调用下一个操作函数
		 
		 e.g.  查找年龄最大的三位同学
		 db.class0.find({age:{$type:1}},{_id:0}).sort({age:-1}).limit(3)
  
	8.  通过序列号直接获取文档集合中某一个

     e.g.  获取文档集合第二项
		 db.class0.find({},{_id:0}).sort({age:1})[1]
		 
		 
		 
 2. 修改函数
 updateOne(query,update,upsert)
 功能: 修改第一个符合条件文档
 参数: query  筛选条件  同 find 
 update 要修改的数据，需要同修改操作符一				 起使用
 upsert 如果query没有筛选到文档是否插入				 新的文档
 update  键值对文档，表达将数据修改为什么样子

e.g.  将tom年龄修改为16
db.class0.updateOne({name:'Tom'},{$set:{age:16}})

upsert  如果设置为true，此时query没有筛选到文档会根据前两个参数插入新的文档

e.g.  如果没有Levi则插入新的文档
db.class0.updateOne({name:'Levi'},{$set:{age:21}},{upsert:true})


updateMany(query,update,upsert):
功能: 修改所有符合条件的文档
参数： 同  updateOne

e.g.  修改age域为字符串的年龄改为18
db.class0.updateMany({age:{$type:2}},{$set:{age:18}})


update(query,update,upsert,multi)
功能: 修改文档
参数：query  update 用法同 updateOne
upsert  upsert=true 表示查找不到文档则插入新的文档
multi   默认只修改一个文档 ，multi=true
表示修改所有符合条件文档

e.g. 修改jack年龄16，如果不存在则插入，如果存在多个则全部修改
db.class0.update({name:'Jack'},{$set:{age:16}},true,true)

findOneAndUpdate(query,update)
功能: 查找到一个文档并修改
参数: query 查找条件
update  修改数据
返回值 ： 修改前的文档

e.g.  查找到Emma 并修改其年龄为19
db.class0.findOneAndUpdate({name:'Emma'},{$set:{age:19}})


findOneAndReplace(query,doc)
功能: 查找一个文档并替换之
参数：query  查找条件
doc  新的文档
返回： 返回原文档

e.g.  查找lily文档并替换之
db.class0.findOneAndReplace({name:'Lily'},{name:'Jame',age:17,sex:'m'})


3. 修改操作符（修改器）

【1】 $set: 修改一个域的值或者增加一个域

e.g. 修改Levi sex域为'm'，如果没有这个域会自动增添
db.class0.updateOne({sex:{$exists:false}},{$set:{sex:'m'}})

* 一个修改器可以同时修改多项

【2】 $unset: 删除一个域

e.g. 删除lucy的sex域
db.class0.updateOne({name:'Lucy'},{$unset:{sex:''}})

【3】 $rename : 给域重命名

e.g.  给sex域 重命名为gender
db.class0.updateMany({},{$rename:{sex:'gender'}})

【4】 $setOnInsert : 如果使用update*执行了插入文档操作，则作为插入的内容

e.g.  如果执行了插入文档则setOnInsert内容也会插入
db.class0.updateOne({name:'Daivl'},{$set:{age:18},$setOnInsert:{gender:'m'}},{upsert:true})

* update参数可以使用多个修改器
```

## [MongoDB学习笔记-数据格式及数据类型](https://www.cnblogs.com/Khadron/p/MongoDB_Note_1.html)

#### **JSON**

​    JSON是一种简单的数据表示方式，它易于理解、易于解析、易于记忆。但从另一方面来说，因为只有null、布尔、数字、字符串、数组和对象这几种数据类型，所以JSON有一定局限性。例如，JSON没有日期类型，JSON只有一种数字类型，无法区分浮点数和整数，更别说区分32为和64位数字了。再者，JSON无法表示其他一些通用类型，如正则表达式或函数。

#### **BSON**

BSON（Binary Serialized Document Format）是一种类JSON的二进制形式的存储格式，简称Binary JSON。它和JSON一样，支持内嵌的文档对象和数组对象，但是BSON有JSON没有的一些数据类型，如Date和BinData类型。它支持下面数据类型。每个数据类型对应一个数字，在MongoDB中可以使用$type操作符查看相应的文档的BSON类型

| 类型                   | 对应数字 | 别名                  | 说明 |
| ---------------------- | -------- | --------------------- | ---- |
| Double1                | 1        | double                |      |
| String                 | 2        | string                |      |
| Object                 | 3        | object                |      |
| Array                  | 4        | array                 |      |
| Binary data            | 5        | binData               |      |
| Undefined              | 6        | undefined             | 弃用 |
| ObjectId               | 7        | objectId              |      |
| Boolean                | 8        | “bool”                |      |
| Date                   | 9        | “date”                |      |
| Null                   | 10       | “null”                |      |
| Regular Expression     | 11       | “regex”               |      |
| DBPointer              | 12       | “dbPointer”           |      |
| JavaScript             | 13       | “javascript”          |      |
| Symbol                 | 14       | “symbol”              |      |
| JavaScript(with scope) | 15       | “javascriptWithScope” |      |
| 32-bit integer         | 16       | “int”                 |      |
| Timestamp              | 17       | “timestamp”           |      |
| 64-bit integer         | 18       | “long”                |      |
| Min key                | -1       | “minKey”              |      |
| Max key                | 127      | “maxKey”              |      |

#### **基本数据类型**

null：用于表示空值或者不存在的字段，{“x”:null}

布尔型：布尔类型有两个值true和false，{“x”:true}

数值：shell默认使用64为浮点型数值。{“x”：3.14}或{“x”：3}。对于整型值，可以使用NumberInt（4字节符号整数）或NumberLong（8字节符号整数），{“x”:NumberInt(“3”)}{“x”:NumberLong(“3”)}

字符串：UTF-8字符串都可以表示为字符串类型的数据，{“x”：“呵呵”}

日期：日期被存储为自新纪元依赖经过的毫秒数，不存储时区，{“x”:new Date()}

正则表达式：查询时，使用正则表达式作为限定条件，语法与JavaScript的正则表达式相同，{“x”:/[abc]/}

数组：数据列表或数据集可以表示为数组，{“x”： [“a“，“b”,”c”]}

内嵌文档：文档可以嵌套其他文档，被嵌套的文档作为值来处理，{“x”:{“y”:3 }}

对象Id：对象id是一个12字节的字符串，是文档的唯一标识，{“x”: objectId() }

二进制数据：二进制数据是一个任意字节的字符串。它不能直接在shell中使用。如果要将非utf-字符保存到数据库中，二进制数据是唯一的方式。

代码：查询和文档中可以包括任何JavaScript代码，{“x”:function(){/*…*/}}

**BSON 与 MongoDB 的关系**

​    BSON是用于存储MongoDB【文档】的一种文档格式。驱动程序在使用【文档】进行插入、查询或其他操作时。会先将【文档】编码成BSON格式，然后发送给服务器。同样地，服务器将文档返回客户端时，也是已BSON格式进行的。驱动程序先对此BSON进行解码然后再传送给客户端。因此，BSON与MongoDB的关系为：MongoDB利用BSON格式存储数据和传输数据



```
一. 修改器的使用(续)

  1.  $inc :  加法修改器
   
	  e.g.  所有人年龄加1
		 db.class1.updateMany({},{$inc:{age:1}})

  2. $mul  :  乘法修改器

	  e.g. 所有人年龄乘以0.5
	  db.class1.updateMany({},{$mul:{age:0.5}})

	 * $inc  $mul 操作数可以是整数 小数 正数 负数	 
	
	3. $max :  修改某个域的值，如果小于指定值则改为指定值，大于则不变

	  e.g.  如果age域小于30改为30，大于30则不变
		db.class1.updateMany({sex:'w'},{$max:{age:30}})

  4. $min :修改某个域的值，如果大于指定值则改为指定值，小于则不变
	  
		e.g.  将age大于30的文档，如果age大于40改为40
		db.class1.updateMany({age:{$gt:30}},{$min:{age:40}})

  数组修改器
	 
	  1. $push  向数组中添加一项
		
		e.g.  给小红score数组增加一个元素10
		db.class2.updateOne({name:'小红'},{$push:{score:10}})

		2. $pushAll  向数组中添加多项
		3.6版本没有了该功能

		Looking at mongodb official documentation $pushAll had been deprecated since v2.4.

		In latest mongodb version (3.6) $pushAll does not exist anymore.
		
		e.g.  给小明score数组中增加多个元素
		db.class2.updateOne({name:'小明'},{$pushAll:{score:[10,5]}})

		3. $pull : 从数组中删除某个值

		e.g. 删除小刚score数组中的90
		db.class2.updateOne({name:'小刚'},{$pull:{score:90}})

		4. $pullAll : 同时删除数组中多个值
    
		e.g.  删除小明score数组多个值
		db.class2.updateOne({name:'小明'},{$pullAll:{score:[69,5]}})

		5. $pop ： 弹出数组中一项
		
		e.g.  弹出数组中最后一项 （1表示最后一项，-1表示第一项）
		db.class2.updateOne({name:'小红'},{$pop:{score:1}})

		6. $addToSet : 向数组中添加一项，但是不能和已有的数值重复
		
		e.g.  向score增加80，但是不能和已有的重复
		db.class2.updateOne({name:'小刚'},{$addToSet:{score:80}})

		7. $each : 对多个值逐一操作
		
		e.g.  对90  10 都执行push操作
		db.class2.updateOne({name:'小红'},{$push:{score:{$each:[90,10]}}})

		8. $position : 指定数据插入位置 配合$each
		
		e.g.  将90 插入到 索引1位置
		db.class2.updateOne({name:'小刚'},{$push:{score:{$each:[90],$position:1}}})

    9. $sort :  给数组排序  配合$each使用
		
		e.g. 将小红score数组按照降序排序 （-1降序，1升序）
		db.class2.updateOne({name:'小红'},{$push:{score:{$each:[],$sort:-1}}})
```

```
练习 ： 使用grade

  1. 将小红年龄修改为8岁，兴趣爱好改为跳舞画画
	   updateOne({name:'小红'},{$set:{age:8,hobby:['dance','draw']}})

	2. 小明多了一个兴趣爱好 唱歌
		 updateOne({name:'小明'},{$push:{hobby:'sing'}})


	3. 小王兴趣爱好多个吹牛，打篮球
		updateOne({name:'小王'},{$push:{hobby:['吹牛','basketball']}})

	4. 小李兴趣增加跑步,唱歌，但是确保不和以前的重复
		updateOne({name:'小李'},{$addToSet:{hobby:{$each:['running','sing']}}})

	5. 班级所有同学年龄增加1
		updataMany({},{$inc:{age:1}})

	6. 删除小明的sex属性
		updateOne({name:'小明'},{$unset:{sex:''}})

	7. 小李第一个兴趣爱好不要了
		updateOne({name:'小明'},{$pop:{hobby:-1}})

	8. 小刚不喜欢计算机和画画了
	  updateOne({name:'小明'},{$pullAll:{hobby:['draw','computer']}})
		 

二. 删除操作
  1. 格式对比
	 mysql ： delete  from  table  where ... 
	 mongo ： db.collection.deleteOne(query)
  2. 删除函数
	 db.collection.deleteOne(query)
	 功能: 删除第一个符合条件文档
	 参数: 筛选条件
	 e.g.  删除第一个不存在 gender域的文档
	  db.class0.deleteOne({gender:{$exists:false}})
   db.collection.deleteMany(query)
	 功能: 删除所有符合条件文档
	 参数: 筛选条件
	 e.g.  删除所有小于18岁的文档
	 db.class0.deleteMany({age:{$lt:18}})
     *  删除一个集合中所有文档
	      db.class1.deleteMany({})
	 db.collection.remove(query,justOne)
	 功能: 删除文档
	 参数: query  筛选条件
	 			 justOne=>false 删除所有符合条件文档(默认)
         justOne=>true  只删除一个符合条件文档	
		e.g.  删除第一个性别为m的文档
    db.class0.remove({gender:'m'},true)
    db.collection.findOneAndDelete(query)
		功能: 查找一个文档并删除之
		参数: 查找条件
		返回: 查找到的文档
		e.g. 查找Levi并删除
		db.class0.findOneAndDelete({name:'Levi'})
练习 ： 使用grade
 1. 删除所有年龄小于8岁或大于12岁的同学
	 deleteMany({$or:[{age:{$gt:12}},{age:{$lt:8}}]})
 2. 删除兴趣爱好中没画画或跳舞的同学
	 deleteMany({hobby:{$nin:['draw','dance']}})
```



数据类型和内部文档操作

```
三. 一些数据类型

  1. 时间类型

	  【1】 获取当前时间
		    
				* new  Date()  自动生成当前时间
				
				e.g. 
				db.class1.insertOne({book:'Python入门',date:new Date()})

				* Date()  获取计算机当前时间生成字符串
				
				e.g.
				db.class1.insertOne({book:'Python精通',date:Date()})

    【2】 时间函数

		    ISODate()
				功能 ： 将制定时间转换为标准时间存入
				参数： 默认同  new  Date() 获取当前时间
							 或者字符串制定时间
							 "2019-01-01  08:08:08"
							 "20190101  08:08:08"
							 "20190101"
				
				e.g.  传入制定时间
				db.class1.insertOne({book:'Python疯狂',date:ISODate("2019-01-01 08:08:08")})

	  【3】 时间戳
		    
				valueOf()
				功能: 将标准时间转化为时间戳

        e.g. 将标准时间转换为时间戳
				db.class1.insertOne({book:'Python涅槃',date:ISODate().valueOf()})

  2. Null 类型

	  【1】 值 ： null

		【2】 含义 ： 
		     
				 * 表示某个域的值为空
				 
				 e.g.  price域的值为空
				 db.class1.insertOne({book:'Python Web',price:null})

				 * 查找时表示某个域没有
					
				 e.g. 查找到price域为null或者没有该域的
				 db.class1.find({price:null},{_id:0})

  3. 内部文档（Object类型）

	  【1】 定义: 文档中某个域的值为内部文档，则该值为object类型数据

		【2】 使用方法：当使用内部文档某个域的值时，需要采用个"外部域.内部域"的方法,此时该格式需要用引号表示为字符串

		e.g.  找到出版社为中国文学的
		db.class3.find({"intro.publication":'中国文学出版社'},{_id:0})

练习： grade

   1. 将小红爱好的第二项变为 唱歌
	 		
			updateOne({name:'小红'},{$set:{'hobby.1':'sing'}})

	 2. 给小王增加一个域 
	    备注:{民族:'回族',习俗:'注意饮食禁忌'}

			updateOne({name:'小王'},{$set:{备注:{民族:'回族',习俗:'注意饮食禁忌'}}})
	 
	 3. 修改小王的备注域，增加一项 
	    宗教 : '伊斯兰'

			updateOne({name:'小王'},{$set:{'备注.宗教':'伊斯兰'}})
```



#### **索引操作**

```
1. 什么是索引：索引是建立文档所在位置的查找清单，使用索引可以方便快速查找，减少遍历次数，提高查找效率
2. 索引约束： * 数据量很小时不需要创建索引

- 创建索引会增加磁盘的使用空间
- 对数据库操作大多时写操作而不是读操作时不宜创建索引

3. 创建索引
   【1】 db.collection.createIndex(index,option)
   功能: 创建索引
   参数：索引域和索引选项
   e.g. 为name域创建索引
   db.class0.createIndex({name:1}) 

- _id域会由系统自动生成索引
- 1 表示正向索引，-1表示逆向索引					
  【2】 db.collection.getIndexes()
  功能： 查看集合中索引
  【3】 通过第二个参数定义索引名
  e.g.  创建索引名字为ageIndex
  db.class0.createIndex({age:-1},{name:'ageIndex'})
  【4】 其他索引创建方法   
  ensureIndex()
  功能: 创建索引
  参数： 同 createIndex()
  createIndexes([{},{}..])
  功能: 创建多个索引
  参数: 数组中写多个键值对 

4. 删除索引 		
   【1】 db.collection.dropIndex(index or name)
   功能: 删除一个索引
   参数: 索引名称或者键值对				
   e.g.  通过名称或者键值对删除
   db.class0.dropIndex('name_-1')
   db.class0.dropIndex({age:-1})
   【2】 db.collection.dropIndexes()
   功能 ： 删除所有索引			

- _id索引不会被删除

5. 其他类型索引   
   【1】 复合索引: 根据多个域创建一个索引
   db.class0.createIndex({name:1,age:-1})			
   【2】object/数组索引 ： 如果对object域或者数组域创建索引则针对object或者数组中某一个元素的查询也是索引查询
   e.g. 如果对intro创建了索引，则该查找也是索引查找
   db.class3.find({'intro.author':'曹雪芹'})
   【3】 唯一索引 ： 要求创建索引的域不能有重复值
   e.g. 对name域创建唯一索引
   db.class0.createIndex({name:1},{unique:true})
   【4】 稀疏索引 ： 如果创建稀疏索引则对没有索引域的文档会忽略
   e.g. 对age 创建稀疏索引
   db.class0.createIndex({age:1},{sparse:true,name:'Age'})
```

#### **聚合操作**

```sql
1. 什么是聚合 ： 对文档进行数据整理统计，得到统计结果

   2. 集合函数 

      db.collection.aggregate(aggr)
       功能: 执行聚合操作
       参数: 聚合条件，配合聚合操作符使用

   3. 聚合操作符

     【1】 $group  分组聚合  需要配合统计操作符
   	    

   - 统计求和 ： $sum
     	
     e.g. 按性别分组统计每组人数
      db.class.aggregate({$group:{_id:'$gender',num:{$sum:1}}})

     - 求平均数 ： $avg 

     e.g.  按性别分组求平均年龄
     db.class.aggregate({$group:{_id:'$gender',num:{$avg:'$age'}}})

     - 求最大最小值 : $max / $min

     e.g. 按性别分组求每组的最大值
     db.class.aggregate({$group:{_id:'$gender',num:{$max:'$age'}}})

     - $first/$last   求第一项值和最后一项值

   【3】 $match  数据筛选

   - match 值的写法同find函数中query写法

     e.g. 筛选年龄大于18的文档
     db.class0.aggregate({$match:{age:{$gt:18}}})

    【4】 $limit  显示集合中前几条文档

   ​		e.g. 显示前3个文档内容
   ​    db.class0.aggregate([{$limit:3}])

     【5】$skip  跳过前几个文档显示后面的内容

   ​     e.g. 跳过前3个文档显示后面内容
   ​     db.class0.aggregate([{$skip:3},{$project:{_id:0}}])

     【6】 $sort  对集合文档排序

   ​     e.g. 对文档按年龄排序
   ​     db.class0.aggregate([{$sort:{age:1}},{$project:{_id:0}}])

2. 聚合管道 

​     定义： 指将第一个聚合的结果交给第二个聚合操作继续执行，直到所有聚合完成。

​     形式： aggregate([{聚合1},{聚合2}...])

​     e.g. 查找年龄大于18的文档，不显示_id
​     db.class0.aggregate([{$match:{age:{$gt:18}}},{$project:{_id:0}}])
```

