# **redis_day01回顾**

## **Redis的特点**

```python
1、基于key-value的非关系型数据库
2、基于内存存储，速度很快
3、基于内存存储，经常当作缓存型数据库使用，常用信息存储在redis数据库中
```

## **五大数据类型**

```python
1、字符串类型（string）
2、列表类型（list）
3、哈希类型（hash）
4、集合类型（set）
5、有序集合类型（sorted set）
```

### **字符串类型**

```python
# 设置key相关操作
1、set key value
2、setnx key value # 当键不存在时设置 not exists
3、mset k1 v1 k2 v2 k3 v3
4、set key value ex seconds # 设置过期时间
5、set key value
5、expire key 5
5、pexpire key 5
5、ttl key
5、persist key # 删除过期时间
# 获取key相关操作
6、get key
7、mget k1 k2 k3
8、strlen key 
# 数字相关操作
7、incrby key 步长
8、decrby key 步长
9、incr key
10、decr key
11、incrbyfloat key number
```

### **列表类型**

```python
# 插入元素相关操作
1、LPUSH key value1 value2 
2、RPUSH key value1 value2
3、RPOPLPUSH source destination
4、LINSERT key after|before value newvalue
# 查询相关操作
5、LRANGE key start stop
6、LLEN key
# 删除相关操作
7、LPOP key
8、RPOP key
# timeout参数必须得给，0代表永久阻塞
9、BLPOP key timeout
10、BRPOP key timeout
11、LREM key count value
12、LTRIM key start stop
# 修改指定元素相关操作
13、LSET key index newvalue
```

**思考：**

**Redis列表如何当做共享队列来使用？？？**

```python
# 同学你好，你还记得小米应用商店爬取URL地址的案例吗？
1、生产者消费者模型
2、生产者进程在列表中 LPUSH | RPUSH 数据，消费者进程在列表中 RPOP | LPOP 数据
```

# **redis_day02笔记**



**Python操作字符串类型**

```python
import redis

r = redis.Redis(host='192.168.43.49',port=6379,password='123456',db=0)

r.set('mystring','python')
# b'python'
print(r.get('mystring'))
# False
print(r.setnx('mystring','socket'))
# mset：参数为字典
r.mset({'mystring2':'mysql','mystring3':'mongodb'})
# mget：结果为一个列表
print(r.mget('mystring','mystring2','mystring3'))
# mystring长度：6
print(r.strlen('mystring'))
# 数字类型操作
r.set('number',10)
r.incrby('number',5)
r.decrby('number',5)
r.incr('number')
r.decr('number')
r.incrbyfloat('number',6.66)
r.incrbyfloat('number',-6.66)
# b'10'
print(r.get('number'))
```

## **==位图操作bitmap==**

**定义**

```python
1、位图不是真正的数据类型，它是定义在字符串类型中
2、一个字符串类型的值最多能存储512M字节的内容，位上限：2^32
# 1MB = 1024KB
# 1KB = 1024Byte(字节)
# 1Byte = 8bit(位)
```

**强势点**

```
可以实时的进行统计，极其节省空间。官方在模拟1亿2千8百万用户的模拟环境下，在一台MacBookPro上，典型的统计如“日用户数”的时间消耗小于50ms, 占用16MB内存
```

**常用命令**

```python
# 设置某一位上的值（offset是偏移量，从0开始）
setbit key offset value
# 获取某一位上的值
GETBIT key offset
# 统计键所对应的值中有多少个 1 
BITCOUNT key
```

**应用场景案例**

```python
网站用户的上线次数统计（寻找活跃用户）
用户名为key，上线的天作为offset，上线设置为1

示例: 用户名为 user001 的用户，今年第1天上线，第30天上线

SETBIT user001 0 1 
SETBIT user001 29 1
BITCOUNT user001
```

**代码实现**

```python
02_setbit_count.py
```

## **==Hash散列数据类型==**

- **定义**

![1562834840173](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\1562834840173.png)

```python
1、由field和关联的value组成的键值对
2、field和value是字符串类型
3、一个hash中最多包含2^32-1个键值对
```

- **优点**

```python
1、节约内存空间
2、每创建一个键，它都会为这个键储存一些附加的管理信息（比如这个键的类型，这个键最后一次被访问的时间等）
3、键越多，redis数据库在储存附件管理信息方面耗费内存越多，花在管理数据库键上的CPU也会越多
```

- **缺点（不适合hash情况）**

```
1、使用二进制位操作命令:SETBIT、GETBIT、BITCOUNT等，如果想使用这些操作，只能用字符串键
2、使用过期键功能：键过期功能只能对键进行过期操作，而不能对散列的字段进行过期操作
```

**基本命令操作**

```python
# 1、设置单个字段
HSET key field value
HSETNX key field value
# 2、设置多个字段
HMSET key field value field value
# 3、返回字段field个数
HLEN key
# 4、判断字段是否存在（不存在返回0）
HEXISTS key field
# 5、返回字段值
HGET key field
# 6、返回多个字段值
HMGET key field filed
# 7、返回所有的键值对
HGETALL key
# 8、返回所有字段名
HKEYS key
# 9、返回所有值
HVALS key
# 10、删除指定字段
HDEL key field field field
# 11、在字段对应值上进行整数增量运算
HINCRBY key field increment
# 12、在字段对应值上进行浮点数增量运算
HINCRBYFLOAT key field increment
```

**python基本方法**

```python
# 1、更新一条数据的属性，没有则新建
hset(name, key, value) 
# 2、读取这条数据的指定属性， 返回字符串类型
hget(name, key)
# 3、批量更新数据（没有则新建）属性
HMSET key field value field value 
user_dict = {field1:value1,field2:value2}
hmset(name, user_dict)
# 4、批量读取数据（没有则新建）属性
hmget(name, keys, *args)
# 5、获取这条数据的所有属性和对应的值，返回字典类型
HGETALL key
1)name
2)wang
3)age
4)20
hgetall(name)
# 6、获取这条数据的所有属性名，返回列表类型
hkeys(name)
# 7、删除这条数据的指定属性
hdel(name, *keys)
```

**Python代码hash散列**

```python

```

**应用场景：微博好友关注**

```python
1、用户ID为key，Field为好友ID，Value为关注时间
	   key          field    value
    user:10000    user:606  20190520
	              user:605  20190521
2、用户维度统计
   统计数包括：关注数、粉丝数、喜欢商品数、发帖数
   用户为key，不同维度为field，value为统计数
   比如关注了5人
	HSET user:10000 fans 5
	HINCRBY user:10000 fans 1
```

**应用场景: redis+mysql+hash组合使用**

- 原理

  ```python
  用户想要查询个人信息
  1、到redis缓存中查询个人信息
  2、redis中查询不到，到mysql查询，并缓存到redis
  3、再次查询个人信息
  ```

- 代码实现

  ```python
  
  ```
  
  

**mysql数据库中数据更新信息后同步到redis缓存**

用户修改个人信息时，要将数据同步到redis缓存

```python

```

## **集合数据类型（set）**

- 特点

```python
1、无序、去重
2、元素是字符串类型
3、最多包含2^32-1个元素
```

- 基本命令

```python
# 1、增加一个或者多个元素,自动去重
SADD key member1 member2
# 2、查看集合中所有元素
SMEMBERS key
# 3、删除一个或者多个元素，元素不存在自动忽略
SREM key member1 member2
# 3、随机弹出元素(默认弹出一个)
SPOP key [count]
# 4、元素是否存在
SISMEMBER key member
# 5、随机返回集合中指定个数的元素，默认为1个
SRANDOMMEMBER key [count]
# 6、返回集合中元素的个数，不会遍历整个集合，只是存储在键当中了
SCARD key
# 7、把元素从源集合移动到目标集合
SMOVE source destination member
# 8、差集(number1 1 2 3 number2 1 2 4)
SDIFF key1 key2 
# 9、差集保存到另一个集合中
SDIFFSTORE destination key1 key2
# 10、交集
SINTER key1 key2
SINTERSTORE destination key1 key2
# 11、并集
SUNION key1 key2
SUNIONSTORE destination key1 key2
```

**案例: 新浪微博的共同关注**

```python
需求: 当用户访问另一个用户的时候，会显示出两个用户共同关注过哪些相同的用户
设计: 将每个用户关注的用户放在集合中，求交集即可
实现:

user001 = {'peiqi','qiaozhi','danni'}
user002 = {'peiqi','qiaozhi','lingyang'}

user001和user002的共同关注为:
# SINTERSTORE user_all user001 user002
# SINTER user001 user002
```

**python操作set**

```python
# 1、给name对应的集合中添加元素
r.sadd(name,values)
r.sadd("set_name","tom")
r.sadd("set_name","tom","jim")

# 2、获取name对应的集合的所有成员
r.smembers(name)

# 3、获取name对应的集合中的元素个数
scard(name)
r.scard("set_name")

# 4、检查value是否是name对应的集合内的元素
sismember(name, value)

# 5、随机删除并返回指定集合的一个元素
spop(name)

# 6、删除集合中的某个元素
srem(name, value) 
r.srem("set_name", "tom")

# 7、获取多个name对应集合的交集
sinter(keys, *args)

r.sadd("set_name","a","b")
r.sadd("set_name1","b","c")
r.sadd("set_name2","b","c","d")

print(r.sinter("set_name","set_name1","set_name2"))
#输出:｛b'b'｝

# 8、获取多个name对应的集合的并集
sunion(keys, *args)
r.sunion("set_name","set_name1","set_name2")
```

**python代码实现微博关注**

```python

```



## **==有序集合sortedset==**

- 特点

```
1、有序、去重
2、元素是字符串类型
3、每个元素都关联着一个浮点数分值(score)，并按照分值从小到大的顺序排列集合中的元素（分值可以相同）
4、最多包含2^32-1元素
```

- 示例

  **一个保存了水果价格的有序集合**

| 分值 | 2.0  | 4.0  | 6.0  | 8.0  | 10.0 |
| ---- | ---- | ---- | ---- | ---- | ---- |
| 元素 | 西瓜 | 葡萄 | 芒果 | 香蕉 | 苹果 |

​	**一个保存了员工薪水的有序集合**

| 分值 | 6000 | 8000 | 10000 | 12000 |      |
| ---- | ---- | ---- | ----- | ----- | ---- |
| 元素 | lucy | tom  | jim   | jack  |      |

​	**一个保存了正在阅读某些技术书的人数**

| 分值 | 300      | 400    | 555    | 666        | 777      |
| ---- | -------- | ------ | ------ | ---------- | -------- |
| 元素 | 核心编程 | 阿凡提 | 本拉登 | 阿姆斯特朗 | 比尔盖茨 |

- **增加**

zadd key score member

```python
# 在有序集合中添加一个成员
zadd key score member
# 查看指定区间元素（升序)
zrange key start stop [withscores]
# 查看指定区间元素（降序）
ZREVRANGE key start stop [withscores]
# 查看指定元素的分值
ZSCORE key member
# 返回指定区间元素
# offset : 跳过多少个元素
# count : 返回几个
# 小括号 : 开区间  zrangebyscore salary (6000 (8000
zrangebyscore key min max [withscores] [limit offset count]
limit 2 3 # 显示第 3 4 5 三个元素
# 删除成员
zrem key member
# 增加或者减少分值
zincrby key increment member
# 返回元素排名
zrank key member
# 返回元素逆序排名
zrevrank key member
# 删除指定区间内的元素
zremrangebyscore key min max
# 返回集合中元素个数
zcard key
# 返回指定范围中元素的个数
zcount key min max
zcount fruits 4 7 
zcount fruits (4 7
# 并集
zunionstore destination numkeys key [weights 权重值] [AGGREGATE SUM|MIN|MAX]
# zunionstore zset4 2 zset1 zset2 aggregate max
# 交集：和并集类似，只取相同的元素
ZINTERSTORE destination numkeys key1 key2 WEIGHTS weight AGGREGATE SUM|MIN|MAX
```

**python操作sorted set**

```python

```

**案例1：网易音乐排行榜**

```python
1、每首歌的歌名作为元素（先不考虑重复）
2、每首歌的播放次数作为分值
3、使用ZREVRANGE来获取播放次数最多的歌曲
```

**代码实现**

```python

```

**案例2: 京东商品畅销榜**

```python
# 第1天
ZADD mobile-001 5000 'huawei' 4000 'oppo' 3000 'iphone'
# 第2天
ZADD mobile-002 5200 'huawei' 4300 'oppo' 3230 'iphone'
# 第3天
ZADD mobile-003 5500 'huawei' 4660 'oppo' 3580 'iphone'
问题：如何获取三款手机的销量排名？
ZUNIONSTORE mobile-001:003 mobile-001 mobile-002 mobile-003 # 可否？

```

**python代码实现**

```python

```



















