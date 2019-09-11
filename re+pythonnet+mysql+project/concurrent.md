```
系统编程：linux操作系统，应用层（shell命令，结构和功能）
        io网络编程（什么是io,）1.文件io 文件操作 open（） read（） write（） close（） seek（）                           flush()
                            2.网络io 1.网络基础***(七层模型，tcp,udp的区别和差异)
                                    2.tcp套接字编程 socket（） bind() listen() accept() recv()
                                      send() connect() 
                                      ***应用：http协议
                                    3.udp套接字编程 recvfrom() sendto() close() 
                                      ***应用：广播
        并发编程 多任务编程  1 进程 fork进程 （创建进程，进程概念，处理僵尸）
                                Process进程 进程创建 Process（） start（） join（）
                                           进程池 pool（） apply_async()
                ***进程线程的对比             进程间通信 pipe()  Queue() Value()                                            Array()
                                            Semaphore() 套接字

​```
                      2 线程   创建线程 Thread()
                              同步互斥 （解决线程间争夺资源问题） Event() Lock() 死锁
                              GIL问题 

                      3.io模型 阻塞io （阻塞情形，效率低，简单）
                              非阻塞io （非阻塞，超时检测）
                              io多路复用 select() poll() epoll() 
                                  
                              协程 原理 gevent
​```

函数式编程
						面向对象的程序设计
						装饰器
						网络编程模型
						进程线程io模型
						基础算法练习
```



并发编程
==========================

| Tedu Python 教学部 |
| --- |
| Author：吕泽|
| Days：6天|

-----------
python核心编程第三版
python程序员
开发者
算法爱好者
网站：伯乐在线
app:掘金 

[TOC]

## 多任务编程

1. 意义： 充分利用计算机多核资源，提高程序的运行效率。

2. 实现方案 ：多进程 ， 多线程

3. 并行与并发
>并发 ： 同时处理多个任务，内核在任务间不断的切换达到好像多个任务被同时执行的效果，实际每个时刻只有一个任务占有内核。
io密集型程序，实际上提高了效率。针对计算密集型程序，并没有提高效率。

>并行 ： 多个任务利用计算机多核资源在同时执行，此时多个任务间为并行关系。
io密集型和计算密集型


## 进程（process）

### 进程理论基础

1. 定义 ： 程序在计算机中的一次运行。
>* 程序是一个可执行的文件，是静态的占有磁盘。
>* 进程是一个动态的过程描述，占有计算机运行资源，有一定的生命周期。
资源管理器


2. 系统中如何产生一个进程
		  【1】 用户空间通过调用程序接口或者命令发起请求
			【2】 操作系统接收用户请求，开始创建进程
			【3】 操作系统调配计算机资源，确定进程状态等
			【4】 操作系统将创建的进程提供给用户使用

![](img/linux.png)
		
3. 进程基本概念

* cpu时间片：如果一个进程占有cpu内核则称这个进程在cpu时间片上。
切换和轮转由操作系统来完成

* PCB(进程控制块)：在内存中开辟的一块空间，用于存放进程的基本信息，也用于系统查找识别进程。
	
* 进程ID（PID）： 系统为每个进程分配的一个大于0的整数，作为进程ID。每个进程ID不重复。
	
	>Linux查看进程ID ： ps -aux
	
* 父子进程 ： 系统中每一个进程(除了系统初始化进程)都有唯一的父进程，可以有0个或多个子进程。父子进程关系便于进程管理。
	
>查看进程树： pstree
	
* 进程状态

	- 三态  
		就绪态 ： 进程具备执行条件，等待分配cpu资源
		运行态 ： 进程占有cpu时间片正在运行
		等待态 ： 进程暂时停止运行，让出cpu

![](img/4_3态.png)


  - 五态 (在三态基础上增加新建和终止)
		新建 ： 创建一个进程，获取资源的过程
		终止 ： 进程结束，释放资源的过程

![](img/4_5态.png)

  - 状态查看命令 ： ps -aux  --> STAT列

>				S 等待态
>				R 执行态
>				D 等待态
>				T 等待态
>				Z 僵尸

>				<  有较高优先级
>				N  优先级较低
>				+  前台进程
>				s  会话组组长
>				l  有多线程的

* 进程的运行特征
	【1】 进程可以使用计算机多核资源
	【2】 进程是计算机分配资源的最小单位
	线程，进程内部再调节分派
	【3】 进程之间的运行互不影响，各自独立
	【4】 每个进程拥有独立的空间，各自使用自己空间资源
	有利于数据单独处理

```
> 面试要求
>
> > 1. 什么是进程，进程和程序有什么区别

> > 2. 进程有哪些状态，状态之间如何转化
## 基于fork的多进程编程

### fork使用

***代码示例：day1/fork.py***
"""
基于fork的进程创建演示1
"""

import os
from time import sleep

pid = os.fork()

if pid < 0:
  print("Create process failed")
elif pid == 0:
  os._exit(0)
  sleep(3)
  print("New process")
else:
  sleep(5)
  print("Old process")

print("Fork test end")
***代码示例：day1/fork1.py***
import os
from time import sleep

print("=========================")
a = 1

pid = os.fork()

if pid < 0:
  print("Create process failed")
elif pid == 0:
  print("New process")
  print("a = ",a)
  a = 10000
else:
  sleep(1)
  print("Old process")
  print("a:",a)

print("All a = ",a)
```


基于Linux ，unix

> pid = os.fork()
		功能： 创建新的进程
		返回值：整数，如果创建进程失败返回一个负数，如果成功则在原有进程中返回新进程的PID，在新进程中返回0

>注意
<!-- >>* 子进程会复制父进程全部内存空间，从fork下一句开始执行。 -->
>>* 父子进程各自独立运行，运行顺序不一定。
>>* 利用父子进程fork返回值的区别，配合if结构让父子进程执行不同的内容几乎是固定搭配。
>>* 父子进程有各自特有特征比如PID PCB 命令集等。
>>* 父进程fork之前开辟的空间子进程同样拥有，父子进程对各自空间的操作不会相互影响。

### 进程相关函数

***代码示例：day1/get_pid.py***

```
# 获取pid值

import os
import time

pid = os.fork()

if pid < 0:
  print("Error")
elif pid == 0:
  time.sleep(1)
  print("Child PID:",os.getpid())
  print("Get parent PID:",os.getppid())
else:
  print("Get child PID:",pid)
  print("Parent PID:",os.getpid())
***代码示例：day1/exit.py***
mport os
import sys

# os._exit(1)

sys.exit("退出进程")

print("Process exit")
```



>os.getpid()
			功能： 获取一个进程的PID值
			返回值： 返回当前进程的PID 

>os.getppid()
			功能： 获取父进程的PID号
			返回值： 返回父进程PID

>os._exit(status)
			功能: 结束一个进程
			参数：进程的终止状态

>sys.exit([status])
			功能：退出进程
			参数：整数 表示退出状态
						字符串 表示退出时打印内容

### 孤儿和僵尸

1. 孤儿进程 ： 父进程先于子进程退出，此时子进程成为孤儿进程。

>特点： 孤儿进程会被系统进程收养，此时系统进程就会成为孤儿进程新的父进程，孤儿进程退出该进程会自动处理。

2. 僵尸进程 ： 子进程先于父进程退出，父进程又没有处理子进程的退出状态，此时子进程就会称为僵尸进程。

>特点： 僵尸进程虽然结束，但是会存留部分PCB在内存中，大量的僵尸进程会浪费系统的内存资源。

3. 如何避免僵尸进程产生
* 使用wait函数处理子进程退出

  ***代码示例：day1/wait.py***
	

```
"""
wait 处理僵尸
"""
import os

pid = os.fork()

if pid < 0:
  print("Error")
elif pid == 0:
  print("Child process",os.getpid())
  os._exit(3)
else:
  p,status = os.wait()  # 阻塞等待子进程退出
  print("p : ",p)

# 还原退出状态

  print("status:",os.WEXITSTATUS(status))
  while True:
    pass

```

```
pid,status = os.wait()
	功能：在父进程中阻塞等待处理子进程退出
	返回值： pid  退出的子进程的PID
		status  子进程退出状态
```


   * 创建二级子进程处理僵尸

      ***代码示例：day1/child.py***

      ```
      - """
        二级子进程处理僵尸
        """
        import os
        from time import sleep
      
      def f1():
        for i in range(4):
          sleep(2)
          print("写代码")
      
      def f2():
        for i in range(5):
          sleep(1)
          print("测代码")
      
      pid = os.fork()
      if pid < 0:
        print("Error")
      elif pid == 0:
        p = os.fork()  # 二级子进程
        if p == 0:
          f2()
        else:
          os._exit(0)  # 一级子进程退出
      else:
        os.wait() # 等一级子进程退出
        f1()
      ```

      ```
      - """
         创建父子进程,复制一个文件,各自复制一半到新的文件中
        """
      
      import os
      
      filename = "./img.jpg"
      size = os.path.getsize(filename)
      
      # 父子进程使用fr会相互影响
      
      # fr = open(filename, 'rb')
      
      def top():
        fr = open(filename,'rb')
        fw = open('top.jpg','wb')
        n = size // 2
        fw.write(fr.read(n))
        fr.close()
        fw.close()
      
      def bot():
        fr = open(filename, 'rb')
        fw = open('bot.jpg', 'wb')
        fr.seek(size//2,0)
        fw.write(fr.read())
        fr.close()
        fw.close()
      
      pid = os.fork()
      
      if pid < 0:
        print("Error")
      elif pid == 0:
        top()  # 复制上半部分
      else:
        bot()  # 下半部分
      如果父进程中生产文件描述符，子进程从父进程中拷贝，此时父子进程对该文件描述符的使用会相互影响
      如果父子进程中各自生成文件描述符，那么相互之间没有影响。
      ```


      

	【1】 父进程创建子进程，等待回收子进程
	【2】 子进程创建二级子进程然后退出
	【3】 二级子进程称为孤儿，和原来父进程一同执行事件


  * 通过信号处理子进程退出
				
	>原理： 子进程退出时会发送信号给父进程，如果父进程忽略子进程信号，则系统就会自动处理子进程退出。

	>方法： 使用signal模块在父进程创建子进程前写如下语句 ：
	```python
	import signal
	signal.signal(signal.SIGCHLD,signal.SIG_IGN)
	```
```
"""
信号方法处理僵尸进程
  """
  import signal
	  import os
	
	# 子进程退出时父进程会忽略,此时子进程自动由系统处理
	
	signal.signal(signal.SIGCHLD,signal.SIG_IGN)
	
	pid = os.fork()
	
	if pid < 0:
	  pass
	elif pid == 0:
	  print("Child pid:",os.getpid())
	else:
	  while True:
	    pass
		>特点 ： 非阻塞，不会影响父进程运行。可以处理所有子进程退出
	```
	
	


### 群聊聊天室 

>功能 ： 类似qq群功能
	【1】 有人进入聊天室需要输入姓名，姓名不能重复
	【2】 有人进入聊天室时，其他人会收到通知：xxx 进入了聊天室
	【3】 一个人发消息，其他人会收到：xxx ： xxxxxxxxxxx
	【4】 有人退出聊天室，则其他人也会收到通知:xxx退出了聊天室
	【5】 扩展功能：服务器可以向所有用户发送公告:管理员消息： xxxxxxxxx

```
# 1.功能和需求分析

# 产品原形

# 2.技术分析

# 怎么通过技术实现？

# 服务器，客户端

# 网络：udp

# 功能：用户信息进行存储 长期存储,文件

# 通过姓名和地址转发,列表套元组，字典，链表

# 客户端的收发消息：多路复用，多进程分别收发

# 3.结构设计

# 1.跨平台性

# 2.功能性扩展

# 3.采用什么方式封装

# 函数 封装

# *注释的添加，至少20%,文档的编写,功能的测试

# 4.分析功能模块，指定编写流程

# 1.搭建网络链接

# 2.进入聊天室

# 客户端1.输入姓名,将姓名发送到服务器,3收到服务器反馈4,进入聊天室或者重新输入姓名

# 服务端1.收到请求,2.判断姓名是否存在3反馈信息给客户端,4不允许进入结束，允许进入将

# 用户插入字典5.通知其他用户

# 3.聊天

# 客户端：1.创建新的进程

# 2.父进程收消息，子进程发消息

# 服务端：1.接受请求

# 2.将消息转发给其他人

# 3.退出聊天室

​```
客户端：1.输入退出
        2.将请求发送给服务端
        3.结束进程 发送进程
        4 接受Exit表示退出

服务端：1.接受请求
      2.给其他用户发送退出消息
      3.将退出的客户端发送EXIT
      4.删除用户
​```

# 4.管理员消息

# 5.协议的设置

# 1.客户端和服务端内部协议的设置

# 2.存储用户结构：{name:address}

# 3.进入聊天：如果允许进入，则服务端给客户端发送一个“ok”

# 如果不允许进入，则服务端给客户端发送一个：不允许进入的原因

# 请求类型,让服务端处理不同的类型 http类型

# * 进入聊天室： L name

# * 聊天信息 ：  C name content

# * 退出聊天： Q name

客户端退出：quit退出 ctr+c 表示意外退出
```

```
"""
chat room
客户端
"""
from socket import *
import os,sys

# 服务端地址

ADDR = ('127.0.0.1',8888)

# 发送消息

def send_msg(s,name):
  while True:
    try:
      text = input("发言:")
    except KeyboardInterrupt:
      text = "quit"
    # 退出
    if text.strip() == 'quit':
      msg = "Q " + name
      s.sendto(msg.encode(),ADDR)
      sys.exit("退出聊天室")
    msg = "C %s %s"%(name,text)
    s.sendto(msg.encode(),ADDR)

# 接收消息

def recv_msg(s):
  while True:
    try:
      data,addr = s.recvfrom(4096)
    except KeyboardInterrupt:
      sys.exit()
    # 服务器发送EXIT退出
    if data.decode() == 'EXIT':
      sys.exit()
    print(data.decode() + '\n发言:',end='')

# 启动客户端

def main():
  s = socket(AF_INET,SOCK_DGRAM)
  while True:
    name = input("请输入姓名:")
    msg = "L " + name
    s.sendto(msg.encode(),ADDR)
    # 等待反馈
    data,addr = s.recvfrom(1024)
    if data.decode() == 'OK':
      print("您已进入聊天室")
      break
    else:
      print(data.decode())

# 创建新的进程

  pid = os.fork()
  if pid < 0:
    sys.exit("Error!")
  elif pid == 0:
    send_msg(s,name)
  else:
    recv_msg(s)

if __name__ == "__main__":
  main()
```

```
"""
chat room
env: python 3.5
socket udp  fork  练习
"""

from socket import *
import os,sys

# 服务器地址

ADDR = ('0.0.0.0',8888)

# 存储用户 {name:address}

user = {}

# 登录

def do_login(s,name,addr):
  if name in user or '管理员' in name:
    s.sendto("该用户已存在".encode(),addr)
    return
  s.sendto(b'OK',addr)

# 通知其他人

  msg = "\n欢迎 %s 进入聊天室"%name
  for i in user:
    s.sendto(msg.encode(),user[i])

# 插入字典

  user[name] = addr

# 转发消息

def do_chat(s,name,text):
  msg = "\n%s : %s"%(name,text)
  for i in user:
    if i != name:
      s.sendto(msg.encode(),user[i])

# 退出

def do_quit(s,name):
  msg = "\n%s 退出了聊天室"%name
  for i in user:
    if i != name:
      s.sendto(msg.encode(),user[i])
    else:
      s.sendto(b'EXIT', user[i])

# 从字典移除

  del user[name]

# 循环接收来自客户端的请求

def do_request(s):
  while True:
    data,addr = s.recvfrom(1024)
    tmp = data.decode().split(' ') # 拆分请求
    # 根据请求类型执行不同内容
    if tmp[0] == 'L':
      do_login(s,tmp[1],addr)  # 完成具体服务端登录工作
    elif tmp[0] == 'C':
      text = ' '.join(tmp[2:]) # 拼接消息内容
      do_chat(s,tmp[1],text)
    elif tmp[0] == 'Q':
      if tmp[1] not in user:
        s.sendto(b'EXIT',addr)
        continue
      do_quit(s,tmp[1])

# 搭建udp网络

def main():

# udp套接字

  s = socket(AF_INET,SOCK_DGRAM)
  s.bind(ADDR)

  pid = os.fork()
  if pid < 0:
    return
  elif pid == 0:
    while True:
      msg = input("管理员消息:")
      msg = "C 管理员消息 " + msg
      s.sendto(msg.encode(),ADDR)
  else:

# 请求处理函数

​    do_request(s)

if __name__ == "__main__":
  main()
```



##  multiprocessing 模块创建进程
# 面向对象

### 进程创建方法

***代码示例：day2/process1.py***

```
import multiprocessing as mp
from time import sleep
a = 1
def fun():
    print("开始一个新的进程")
    sleep(5)
    global a
    print("a = ", a)
    a = 10000
    print("a = ", a)
    print("子进程结束了")

# 创建进程对象

p = mp.Process(target=fun)
p.start()  # 启动进程

sleep(2)
print("父进程干点啥")

p.join(1)  # 回收进程

print('a:', a)
```

***代码示例：day2/process2.py***

```
from multiprocessing import Process
from time import sleep
import os

def th1():
  sleep(3)
  print("吃饭")
  print(os.getppid(),'---',os.getpid())

def th2():
  sleep(2)
  print("睡觉")
  print(os.getppid(),'---',os.getpid())

def th3():
  sleep(4)
  print("打豆豆")
  print(os.getppid(),'---',os.getpid())

things = [th1,th2,th3]
jobs = []
for th in things:
  p = Process(target = th)
  p.start()
  jobs.append(p)  # 将进程对象保存在列表

# 一起回收

for i in jobs:
  i.join()
***代码示例：day2/process3.py***
from multiprocessing import Process
from time import sleep

# 带参数的进程函数

def worker(sec,name):
  for i in range(3):
    sleep(sec)
    print("I'm %s"%name)
    print("I'm working ... ")

# p = Process(target=worker,args=(2,'Baron'))

p = Process(target = worker,args=(2,),
            kwargs={'name':'Baron'})
p.start()
p.join()
```



1.  流程特点 
【1】 将需要子进程执行的事件封装为函数
【2】 通过模块的Process类创建进程对象，关联函数
【3】 可以通过进程对象设置进程信息及属性
【4】 通过进程对象调用start启动进程
【5】 通过进程对象调用join回收进程
	
2. 基本接口使用

```python
Process()
功能 ： 创建进程对象
参数 ： target 绑定要执行的目标函数 
	args 元组，用于给target函数位置传参
	kwargs 字典，给target函数键值传参
```

```python
p.start()
功能 ： 启动进程
```
>注意:启动进程此时target绑定函数开始执行，该函数作为子进程执行内容，此时进程真正被创建

```python
p.join([timeout])
功能：阻塞等待回收进程
参数：超时时间
```
>注意
>>* 使用multiprocessing创建进程同样是子进程复制父进程空间代码段，父子进程运行互不影响。
>>* 子进程只运行target绑定的函数部分，其余内容均是父进程执行内容。
>>* multiprocessing中父进程往往只用来创建子进程回收子进程，具体事件由子进程完成。
>>* multiprocessing创建的子进程中无法使用标准输入

3. 进程对象属性

***代码示例：day2/process_attr.py***

```
from multiprocessing import Process
from time import sleep,ctime

def tm():
  for i in range(3):
    sleep(2)
    print(ctime())

p = Process(target = tm,name = 'Tedu')

p.daemon = True # 子进程会随父进程退出

p.start()
print("Name:",p.name)  # 名称
print("PID:",p.pid)  # PID
print("Is alive:",p.is_alive()) # 生命周期


```

> p.name  进程名称
> 		

>p.pid   对应子进程的PID号

>p.is_alive() 查看子进程是否在生命周期

>p.daemon  设置父子进程的退出关系  
守护进程，生命周期很长，一般为操作系统
>>* 如果设置为True则子进程会随父进程的退出而结束
>>* 要求必须在start()前设置
>>* 如果daemon设置成True 通常就不会使用 join() -->


###  进程池实现

***代码示例：day2/pool.py***

```
from multiprocessing import Pool
from time import sleep,ctime

# 进程池事件

def worker(msg):
  sleep(2)
  print(msg)
  return ctime()

# 创建进程池

pool = Pool(4)

# 向进程池添加执行事件

for i in range(10):
  msg = "Hello %d"%i

# r 代表func事件的一个对象

  r = pool.apply_async(func=worker,args=(msg,))

# 关闭进程池

pool.close()

# 回收进程池

pool.join()

print(r.get()) # 可以获取事件函数的返回值
```



1.  必要性
	  【1】 进程的创建和销毁过程消耗的资源较多
		【2】 当任务量众多，每个任务在很短时间内完成时，需要频繁的创建和销毁进程。此时对计算机压力较大
		【3】 进程池技术很好的解决了以上问题。
	
2.  原理
>创建一定数量的进程来处理事件，事件处理完进	程不退出而是继续处理其他事件，直到所有事件全都处理完毕统一销毁。增加进程的重复利用，降低资源消耗。
对计算密集型的进程很好


3. 进程池实现

【1】 创建进程池对象，放入适当的进程

```python	  
from multiprocessing import Pool

Pool(processes)
功能： 创建进程池对象
参数： 指定进程数量，默认根据系统自动判定
```

【2】 将事件加入进程池队列执行

```python
pool.apply_async/e'sik/(func,args,kwds)
功能: 使用进程池执行 func事件
参数： func 事件函数
      args 元组  给func按位置传参
      kwds 字典  给func按照键值传参
返回值： 返回函数事件对象
```

【3】 关闭进程池

```python
pool.close()
功能： 关闭进程池
```

【4】 回收进程池中进程

```
pool.join()
功能： 回收进程池中进程
```


##  进程间通信（IPC）
微博可以登录喜马拉雅
套接字（网络）
文件（磁盘）效率低，保密性差

1. 必要性： 进程间空间独立，资源不共享，此时在需要进程间数据传输时就需要特定的手段进行数据通信。


2. 常用进程间通信方法
>管道  消息队列  共享内存  信号  信号量  套接字 


###  管道通信(Pipe)

***代码示例：day2/pipe.py***

```
from multiprocessing import Process, Pipe
import time

# 创建管道对象

fd1, fd2 = Pipe(duplex=False)

def read():
    # 从管道获取消息
    while True:
        data = fd1.recv()
        print(data)

def write():
    while True:
        time.sleep(2)
        fd2.send(tuple({1: 2, 3: 4}))

p = Process(target=read)
w = Process(target=write)
p.start()
w.start()
p.join()
w.join()
```





1. 通信原理
>在内存中开辟管道空间，生成管道操作对象，多个进程使用同一个管道对象进行读写即可实现通信

2. 实现方法

```python
字节流
from  multiprocessing import Pipe

fd1,fd2 = Pipe(duplex = True)
功能: 创建管道
参数：默认表示双向管道
如果为False 表示单向管道
# 返回值：表示管道两端的读写对象
	如果是双向管道均可读写
#	如果是单向管道fd1只读  fd2只写

fd.recv()
功能 ： 从管道获取内容
返回值：获取到的数据

fd.send(data)
功能： 向管道写入内容
参数： 要写入的数据
```

### 消息队列

***代码示例：day2/queue_0.py***

```
"""
消息队列
"""
from multiprocessing import Process, Queue
from time import sleep
from random import randint

# 创建消息队列

q = Queue(3)

# 请求进程

def request():
    for i in range(10):
        x = randint(0, 100)
        y = randint(0, 100)
        q.put((x, y))

# 处理进程

def handle():
    while True:
        sleep(1)
        try:
            x, y = q.get(timeout=5)
        except:
            break
        else:
            print("%d + %d = %d" % (x, y, x + y))

p1 = Process(target=request)
p2 = Process(target=handle)
p1.start()
p2.start()
p1.join()
p2.join()
进程间通信不一致，可以通过队列进行了缓冲
```




1.通信原理
>在内存中建立队列模型，进程通过队列将消息存入，或者从队列取出完成进程间通信。

2. 实现方法

```python
from multiprocessing import Queue

q = Queue(maxsize=0)
功能: 创建队列对象
参数：最多存放消息个数
返回值：队列对象

q.put(data,[block,timeout])
功能：向队列存入消息
参数：data  要存入的内容
block  设置是否阻塞 False为非阻塞
timeout  超时检测 设置阻塞时间

q.get([block,timeout])
功能：从队列取出消息
参数：block  设置是否阻塞 False为非阻塞
timeout  超时检测
返回值： 返回获取到的内容

q.full()   判断队列是否为满
q.empty()  判断队列是否为空
q.qsize()  获取队列中消息个数
q.close()  关闭队列
```

### 共享内存

***代码示例：day3/value.py***

```
"""
共享内存
"""
from multiprocessing import Value, Process
import time
from random import randint

# 共享内存

money = Value('i', 5000)

# 修改共享内存

def man():
    for i in range(30):
        time.sleep(0.2)
        money.value += randint(1, 1000)

def girl():
    for i in range(30):
        time.sleep(0.15)
        money.value -= randint(100, 800)

m = Process(target=man)
g = Process(target=girl)
m.start()
g.start()
m.join()
g.join()
print("一个月余额", money.value)
```

***代码示例：day3/array.py***

```
from multiprocessing import Process, Array

# 创建共享内存

# shm = Array("i", [1, 2, 3])

# shm = Array("i", 3)  # 表示开辟三个空间的列表

shm = Array('c', 'hello'.encode())

def fun():
    # 共享内存对象可迭代
    for i in shm:
        print(i)
    shm[1] = b'H'

p = Process(target=fun)
p.start()
p.join()
for i in shm:
    print(i)
print(shm.value)  # 直接打印字节串，只对字节串有效
```




1. 通信原理：在内中开辟一块空间，进程可以写入内容和读取内容完成通信，但是每次写入内容会覆盖之前内容。

2. 实现方法

![](img/6_ctype.png)

```python
from multiprocessing import Value,Array

obj = Value(ctype,data)
功能 ： 开辟共享内存
参数 ： ctype  表示共享内存空间类型 'i'  'f'  'c'
       data   共享内存空间初始数据
返回值：共享内存对象

obj.value  对该属性的修改查看即对共享内存读写


obj = Array(ctype,data)
功能： 开辟共享内存空间
参数： ctype  表示共享内存数据类型
      data   整数则表示开辟空间的大小，其他数据类型表示开辟空间存放的初始化数据 #只能是列表和字符串
返回值：共享内存对象


Array共享内存读写： 通过遍历obj可以得到每个值，直接可以通过索引序号修改任意值。

* #可以使用obj.value直接打印共享内存中的字节串
```

### 信号量（信号灯集）

***代码示例：day2/sem.py***
适用性：系统假如执行3个任务，10个人
1. 通信原理
>给定一个数量对多个进程可见。多个进程都可以操作该数量增减，并根据数量值决定自己的行为。

2. 实现方法

```python	  
from multiprocessing import Semaphore

sem = Semaphore(num)
功能 ： 创建信号量对象
参数 ： 信号量的初始值
返回值 ： 信号量对象

sem.acquire()  将信号量减1 当信号量为0时阻塞
sem.release()  将信号量加1
sem.get_value() 获取信号量数量
```

## 线程编程（Thread）

### 线程基本概念

1. 什么是线程
【1】 线程被称为轻量级的进程
【2】 线程也可以使用计算机多核资源，是多任务编程方式
【3】 线程是系统分配内核的最小单元
【4】 线程可以理解为进程的分支任务
进程是计算机分配资源的最小单位，线程，进程内部再调节分派
寄存器，cpu内核，内存，指令集
占有内核，可以并行，或者并发
没有分支，可以叫做单进程或者叫做单线程。
包含线程的进程，开启的线程叫做分支线程。原来的线程叫做主线程，和两个分支线程。
	
2. 线程特征
【1】 一个进程中可以包含多个线程
【2】 线程也是一个运行行为，消耗计算机资源
#【3】 一个进程中的所有线程共享这个进程的资源
【4】 多个线程之间的运行互不影响各自运行
【5】 线程的创建和销毁消耗资源远小于进程
【6】 各个线程也有自己的ID等特征

### threading模块创建线程

***代码示例：day3/thread1.py***

```
import threading
from time import sleep
import os

a = 1

def music():
    for i in range(3):
        sleep(0.1)
        print(os.getpid(), "播放'狂浪'")
    # global a
    print("a= ", a)
    # a = 1000

t = threading.Thread(target=music)
for i in range(4):
    sleep(1)
    print(os.getpid(), "播放葫芦娃")

t.start()
t.join()
print("main a", a)

# a=  1

# main a 1000

***代码示例：day3/thread2.py***
from threading import Thread
from time import sleep

# 含有参数的线程函数

def fun(sec, name):
    print("线程函数参数")
    sleep(sec)
    print("%s 线程完毕" % name)

# 创建多个线程

jobs = []
for i in range(5):
    t = Thread(target=fun, args=(2,), kwargs={'name': 'T%d' % i})
    jobs.append(t)
    t.start()

for i in jobs:
    i.join()
```



【1】 创建线程对象

```	  
from threading import Thread 

t = Thread()
功能：创建线程对象
参数：target 绑定线程函数
     args   元组 给线程函数位置传参
     kwargs 字典 给线程函数键值传参
```

【2】 启动线程

```
 t.start()
```

【3】 回收线程

```
 t.join([timeout])
```

### 线程对象属性

***代码示例：day3/thread_attr.py***

```
from threading import Thread
from time import sleep

def fun01():
    sleep(3)
    print("线程属性测试")

t = Thread(target=fun01, name="Tarena")
t.setDaemon(True)
t.start()
t.setName("Baidu")
print(t.name)
print("Name:", t.getName())
print("Alive:", t.is_alive())
print("is daemon",t.isDaemon())

# Baidu

# Name: Baidu

# Alive: True

# is daemon True
```



>t.name 线程名称
>t.setName()  设置线程名称
>t.getName()  获取线程名称

>t.is_alive()  查看线程是否在生命周期

>t.daemon  设置主线程和分支线程的退出关系
>t.setDaemon()  设置daemon属性值
>t.isDaemon()  查看daemon属性值
>
>>daemon为True时主线程退出分支线程也退出。要在start前设置，通常不和join一起使用。


### 自定义线程类
任务比较复杂，可能会用线程类

***代码示例：day3/myThread.py***

```
from threading import Thread
from time import sleep, ctime

class MyThread(Thread):
    def __init__(self, target=None, args=(), kwargs={}):
        super().__init__()
        self.target = target
        self.args = args
        self.kwargs = kwargs

​```
# def player(self, sec, song):
#     for i in range(3):
#         print("Playing %s : %s" % (song, ctime()))
#         sleep(sec)

def run(self):
    self.target(*self.args, **self.kwargs)
​```

# ---------------------------------------

# 通过完成上面的Mythread使程序正常运行

def player(sec, song):
    for i in range(3):
        print("Playing %s : %s" % (song, ctime()))
        sleep(sec)

t = MyThread(target=player, args=(3,), kwargs={"song": '凉凉'})
t.start()
t.join()
```




1. 创建步骤
【1】 继承Thread类
【2】 重写__init__方法添加自己的属性，使用super加载父类属性
【3】 重写run方法

2. 使用方法
【1】 实例化对象
【2】 调用start自动执行run方法
【3】 调用join回收线程


## 同步互斥

### 线程间通信方法

1. 通信方法
>线程间使用全局变量进行通信


2. 共享资源争夺

* 共享资源：多个进程或者线程都可以操作的资源称为共享资源。对共享资源的操作代码段称为临界区。

* 影响 ： 对共享资源的无序操作可能会带来数据的混乱，或者操作错误。此时往往需要同步互斥机制协调操作顺序。
	
3. 同步互斥机制

>同步 ： 同步是一种协作关系，为完成操作，多进程或者线程间形成一种协调，按照必要的步骤有序执行操作。

![](img/7_同步.png)

>互斥 ： 互斥是一种制约关系，当一个进程或者线程占有资源时会进行加锁处理，此时其他进程线程就无法操作该资源，直到解锁后才能操作。


![](img/7_互斥.png)

### 线程同步互斥方法

#### 线程Event

***代码示例：day3/thread_event.py***

```
from threading import Thread, Event
# from time import sleep

s = None
e = Event()

# 通信的全局变量

def 杨子荣():
    print("杨子荣前来拜山头")
    global s
    s = "天王盖地虎"
    e.set()

t = Thread(target=杨子荣)
t.start()
print("说对口令就是自己人")
e.wait()  # 阻塞等待口令
if s == "天王盖地虎":
    print("宝塔镇河妖")
    print("确认过眼神，你是对的人")
else:
    print("打死他...")
t.join()
```





```python		  
from threading import Event

e = Event()  创建线程event对象

e.wait([timeout])  阻塞等待e被set

e.set()  设置e，使wait结束阻塞

e.clear() 使e回到未被设置状态

e.is_set()  查看当前e是否被设置
```

#### 线程锁 Lock

***代码示例：day3/thread_event.py***

```
from threading import Thread, Lock

a = b = 0

# 创建锁对象

lock = Lock()

def value():
    while True:
        lock.acquire()
        if a != b:
            print("a= %d,b= %d" % (a, b))
        lock.release()

t = Thread(target=value)
t.start()
while True:
    with lock:
        a += 1
        b += 1

t.join()
```

```python
from  threading import Lock

lock = Lock()  创建锁对象
lock.acquire() 上锁  如果lock已经上锁再调用会阻塞
lock.release() 解锁

with  lock:  上锁
...
...
	 with代码块结束自动解锁

```
通过上锁达到一种共享资源的限制

### 死锁及其处理

1. 定义
>死锁是指两个或两个以上的线程在执行过程中，由于竞争资源或者由于彼此通信而造成的一种阻塞的现象，若无外力作用，它们都将无法推进下去。此时称系统处于死锁状态或系统产生了死锁。

![](img/死锁.jpg)

2. 死锁产生条件

***代码示例: day3/dead_lock.py***

>死锁发生的必要条件
>>* 互斥条件：指线程对所分配到的资源进行排它性使用，即在一段时间内某资源只由一个进程占用。如果此时还有其它进程请求资源，则请求者只能等待，直至占有资源的进程用毕释放。
>>* 请求和保持条件：指线程已经保持至少一个资源，但又提出了新的资源请求，而该资源已被其它进程占有，此时请求线程阻塞，但又对自己已获得的其它资源保持不放。
>>* 不剥夺条件：指线程已获得的资源，在未使用完之前，不能被剥夺，只能在使用完时由自己释放,通常CPU内存资源是可以被系统强行调配剥夺的。
>>* 环路等待条件：指在发生死锁时，必然存在一个线程——资源的环形链，即进程集合{T0，T1，T2，···，Tn}中的T0正在等待一个T1占用的资源；T1正在等待T2占用的资源，……，Tn正在等待已被T0占用的资源。

>死锁的产生原因
>>简单来说造成死锁的原因可以概括成三句话：
>>* 当前线程拥有其他线程需要的资源
>>* 当前线程等待其他线程已拥有的资源
>>* 都不放弃自己拥有的资源


3. 如何避免死锁

死锁是我们非常不愿意看到的一种现象，我们要尽可能避免死锁的情况发生。通过设置某些限制条件，去破坏产生死锁的四个必要条件中的一个或者几个，来预防发生死锁。预防死锁是一种较易实现的方法。但是由于所施加的限制条件往往太严格，可能会导致系统资源利用率。



## python线程GIL

1. python线程的GIL问题 （全局解释器锁）

>什么是GIL ：由于python解释器设计中加入了解释器锁，导致python解释器同一时刻只能解释执行一个线程，大大降低了线程的执行效率。

>导致后果： 因为遇到阻塞时线程会主动让出解释器，去解释其他线程。所以python多线程在执行多阻塞高延迟IO时可以提升程序效率，其他情况并不能对效率有所提升。

>GIL问题建议
>* 尽量使用进程完成无阻塞的并发行为
>* 不使用c作为解释器 （Java  C#）

2. 结论 ： 在无阻塞状态下，多线程程序和单线程程序执行效率几乎差不多，甚至还不如单线程效率。但是多进程运行相同内容却可以有明显的效率提升。

## 进程线程的区别联系

### 区别联系
1. 两者都是多任务编程方式，都能使用计算机多核资源
2. 进程的创建删除消耗的计算机资源比线程多
3. 进程空间独立，数据互不干扰，有专门通信方法；线程使用全局变量通信
4. 一个进程可以有多个分支线程，两者有包含关系
5. 多个线程共享进程资源，在共享资源操作时往往需要同步互斥处理
6. 进程线程在系统中都有自己的特有属性标志，如ID,代码段，命令集等。

### 使用场景

1. 任务场景：如果是相对独立的任务模块，可能使用多进程，如果是多个分支共同形成一个整体任务可能用多线程

2. 项目结构：多种编程语言实现不同任务模块，可能是多进程，或者前后端分离应该各自为一个进程。

3. 难以程度：通信难度，数据处理的复杂度来判断用进程间通信还是同步互斥方法。


### 要求
1. 对进程线程怎么理解/说说进程线程的差异
2. 进程间通信知道哪些，有什么特点
3. 什么是同步互斥，你什么情况下使用，怎么用
4. 给一个情形，说说用进程还是线程，为什么
5. 问一些概念，僵尸进程的处理，GIL问题，进程状态


## 并发网络通信模型

### 常见模型分类

1. 循环服务器模型 ：循环接收客户端请求，处理请求。同一时刻只能处理一个请求，处理完毕后再处理下一个。

	>优点：实现简单，占用资源少
	>缺点：无法同时处理多个客户端请求

	>适用情况：处理的任务可以很快完成，客户端无需长期占用服务端程序。udp比tcp更适合循环。

2. IO并发模型：利用IO多路复用,异步IO等技术，同时处理多个客户端IO请求。

	>优点 ： 资源消耗少，能同时高效处理多个IO行为
	>缺点 ： 只能处理并发产生的IO事件，无法处理cpu计算

	>适用情况：HTTP请求，网络传输等都是IO行为。
	
3. 多进程/线程网络并发模型：每当一个客户端连接服务器，就创建一个新的进程/线程为该客户端服务，客户端退出时再销毁该进程/线程。

	>优点：能同时满足多个客户端长期占有服务端需求，可以处理各种请求。
	>缺点： 资源消耗较大

	>适用情况：客户端同时连接量较少，需要处理行为较复杂情况。


### 基于fork的多进程网络并发模型

***代码实现: day4/fork_server.py***

```
"""
fork_server  基于fork搭建基础网络并发模型
重点代码

思路分析:

1. 每当有一个客户端就创建一个新的进程作为客户端处理进程
2. 客户端如果结束,对应进程应该销毁
   """

from socket import *
import os
import signal

# 创建监听套接字

HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST,PORT)

# 客户端服务函数

def handle(c):
  while True:
    data = c.recv(1024)
    if not data:
      break
    print(data.decode())
    c.send(b'OK')
  c.close()

s = socket()  # tcp套接字
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(ADDR)
s.listen(3)

# 处理僵尸进程

signal.signal(signal.SIGCHLD,signal.SIG_IGN)

print("Listen the port %d..."%PORT)

# 循环等待客户端连接

while True:
  try:
    c,addr = s.accept()
  except KeyboardInterrupt:
    os._exit(0)
  except Exception as e:
    print(e)
    continue

# 创建子进程处理这个客户端

  pid = os.fork()
  if pid == 0:  # 处理客户端请求
    s.close()
    handle(c)
    os._exit(0)  # handle处理完客户端请求子进程也退出

# 无论出错或者父进程都要循环回去接受请求

# c对于父进程没用

  c.close()
```




#### 实现步骤

1. 创建监听套接字
2. 等待接收客户端请求
3. 客户端连接创建新的进程处理客户端请求
4. 原进程继续等待其他客户端连接
5. 如果客户端退出，则销毁对应的进程

### 基于threading的多线程网络并发

***代码实现: day4/thread_server.py***

```
"""
thread_server 基于线程的网络并发
重点代码

思路分析:

1. 基本与进程相同,只是换为线程处理客户端请求
2. 当主线程结束,同时终止所有对客户端的服务
   """

from socket import *
from threading import Thread
import sys

# 创建监听套接字

HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST,PORT)

# 处理客户端请求

def handle(c):
  while True:
    data = c.recv(1024)
    if not data:
      break
    print(data.decode())
    c.send(b'OK')
  c.close()

s = socket()  # tcp套接字
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(ADDR)
s.listen(3)

print("Listen the port %d..."%PORT)

# 循环等待客户端连接

while True:
  try:
    c,addr = s.accept()
  except KeyboardInterrupt:
    sys.exit("服务器退出")
  except Exception as e:
    print(e)
    continue

# 创建线程处理客户端请求

  t = Thread(target=handle,args=(c,))
  t.setDaemon(True)
  t.start()
```




#### 实现步骤

1. 创建监听套接字
2. 循环接收客户端连接请求
3. 当有新的客户端连接创建线程处理客户端请求
4. 主线程继续等待其他客户端连接
5. 当客户端退出，则对应分支线程退出


### ftp 文件服务器

***代码实现: day5/ftp***


1. 功能 
	【1】 分为服务端和客户端，要求可以有多个客户端同时操作。
	【2】 客户端可以查看服务器文件库中有什么文件。
	【3】 客户端可以从文件库中下载文件到本地。
	【4】 客户端可以上传一个本地文件到文件库。
	【5】 使用print在客户端打印命令输入提示，引导操作
```
# 1.功能和需求分析

# 产品原形

# 2.技术分析

# 怎么通过技术实现？

# * 并发模型 多线程并发

# 网络：tcp传输  对数据的完整性比较好

# 功能：客户端 查看 下载 上传 打印命令提示符引导操作

​```
  服务端 文件库 存储 文件，内存
​```

# 3.结构设计

- 客户端发起请求 ——>界面
  list   get filename   put filename
  *类进行封装

*

# *注释的添加，至少20%,文档的编写,功能的测试

# 4.分析功能模块，指定编写流程

  1 网络并发结构的搭建

  2 查看 客户端 发送请求查看请求
      服务端 接受请求，打开文件库

  3 下载 客户端：请求发送下载命令，指定文件名
      服务端：接受请求，打开指定的文件名，进行数据传输，http协议

  4 上传 客户端：打开本地文件，请求发送上传命令
      服务端：接受请求，判断文件名是否重复，如果重复
             如果不重复，进行传输

  5 处理客户端对出
# 

# 5.协议的设置

# 文件列表查看：只提供普通文件（非隐藏文件）

# 客户端请求类型： L 请求文件列表
            G  文件名
            P  文件名  
            Q
```

```
"""
ftp 文件服务器
多线程并发/线程练习
"""
from socket import *
from threading import Thread
import os
import time

# 全局变量

HOST = '0.0.0.0'
PORT = 8080
ADDR = (HOST,PORT)
FTP = "/home/tarena/FTP/"  #　文件库位置

# 创建文件服务器服务端功能类

class FTPServer(Thread):
  def __init__(self,connfd):
    self.connfd = connfd
    super().__init__()

  def do_list(self):
    #　获取文件列表
    files = os.listdir(FTP)
    if not files:
      self.connfd.send("文件库为空".encode())
      return
    else:
      self.connfd.send(b'OK')
      time.sleep(0.1)  #　防止和后面发送内容粘包

​```
#　拼接文件列表
files_ = ""
for file in files:
  if file[0] != '.' and \
          os.path.isfile(FTP+file):
    files_ += file + '\n'
self.connfd.send(files_.encode())
​```

  def do_get(self,filename):
    try:
      fd = open(FTP+filename,'rb')
    except Exception:
      self.connfd.send("文件不存在".encode())
      return
    else:
      self.connfd.send(b'OK')
      time.sleep(0.1)
    #　文件发送
    while True:
      data = fd.read(1024)
      if not data:
        time.sleep(0.1)
        self.connfd.send(b'##')
        break
      self.connfd.send(data)

  def do_put(self,filename):
    if os.path.exists(FTP+filename):
      self.connfd.send("该文件已存在".encode())
      return
    self.connfd.send(b'OK')
    f = open(FTP + filename,'wb')
    while True:
      data = self.connfd.recv(1024)
      if data == b'##':
        break
      f.write(data)
    f.close()

# 循环接收客户端请求

  def run(self):
    while True:
      data = self.connfd.recv(1024).decode()
      if not data or data == 'Q':
        return 
      elif data == 'L':
        self.do_list()
      elif data[0] == 'G':   # G filename
        filename = data.split(' ')[-1]
        self.do_get(filename)
      elif data[0] == 'P':   # P filename
        filename = data.split(' ')[-1]
        self.do_put(filename)

# 网络搭建

def main():

# 创建套接字

  sockfd = socket()
  sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
  sockfd.bind(ADDR)
  sockfd.listen(3)
  print("Listen the port %d..."%PORT)
  while True:
    try:
      connfd,addr = sockfd.accept()
      print("Connect from",addr)
    except KeyboardInterrupt:
      print("服务器程序退出")
      return
    except Exception as e:
      print(e)
      continue

​```
#　创建新的线程处理客户端
client = FTPServer(connfd)
client.setDaemon(True)
client.start()   #　运行ｒｕｎ方法
​```

if __name__ == "__main__":
  main()
```

```
"""
ftp 客户端
"""
from socket import *
import sys
import time

ADDR = ('127.0.0.1', 8080)  # 服务器地址

# 客户端功能处理类

class FTPClient:
  def __init__(self, sockfd):
    self.sockfd = sockfd

  def do_list(self):
    self.sockfd.send(b'L')  # 发送请求
    # 等待回复
    data = self.sockfd.recv(128).decode()
    if data == 'OK':
      # 　一次接收文件列表字符串
      data = self.sockfd.recv(4096)
      print(data.decode())
    else:
      print(data)

  def do_get(self, filename):
    # 　发送请求
    self.sockfd.send(('G ' + filename).encode())
    # 等待回复
    data = self.sockfd.recv(128).decode()
    if data == 'OK':
      fd = open(filename, 'wb')
      # 　接收文件
      while True:
        data = self.sockfd.recv(1024)
        if data == b'##':
          break
        fd.write(data)
      fd.close()
    else:
      print(data)

  def do_quit(self):
    self.sockfd.send(b'Q')
    self.sockfd.close()
    sys.exit("谢谢使用")

  def do_put(self, filename):
    try:
      f = open(filename, 'rb')
    except Exception:
      print("该文件不存在")
      return
    # 获取文件名
    filename = filename.split('/')[-1]
    # 　发送请求
    self.sockfd.send(('P ' + filename).encode())
    # 　等待回复
    data = self.sockfd.recv(128).decode()
    if data == 'OK':
      while True:
        data = f.read(1024)
        if not data:
          time.sleep(0.1)
          self.sockfd.send(b'##')  # 结束发送
          break
        self.sockfd.send(data)
      f.close()
    else:
      print(data)

# 创建客户端网络

def main():
  sockfd = socket()
  try:
    sockfd.connect(ADDR)
  except Exception as e:
    print(e)
    return

  ftp = FTPClient(sockfd)  # 实例化对象

# 循环发送请求

  while True:
    print("\n=========命令选项==========")
    print("****      list         ****")
    print("****    get file       ****")
    print("****    put file       ****")
    print("****      quit         ****")
    print("=============================")

​```
cmd = input("输入命令：")

if cmd.strip() == 'list':
  ftp.do_list()
elif cmd[:3] == 'get':
  # 　get filename
  filename = cmd.strip().split(' ')[-1]
  ftp.do_get(filename)
elif cmd[:3] == 'put':
  # 　put ../filename
  filename = cmd.strip().split(' ')[-1]
  ftp.do_put(filename)
elif cmd.strip() == 'quit':
  ftp.do_quit()
else:
  print("请输入正确命令")
​```

if __name__ == "__main__":
  main()               
```




1. GIL问题

2. 进程线程的差异

3. 网络并发模型:  循环网络  IO并发   多进程线程并发

4. 多进程多线程并发

   原理 : 每当有一个客户端连接就创建一个新的进程或者线程处理

	 fork 多进程
	 Thread 多线程
	 Process 多进程

5. 文件服务器
   
	 技术点分析--> 类的封装 -->功能模块划分--> 协议设定


## IO并发

### IO 分类

>IO分类：*阻塞IO ，非阻塞IO，IO多路复用*，异步IO等
高并发量  在硬件条件一定的基础上，优化程序，实现高并发量
高的运行速度  计算密集型  算法优化 io  完善io模型（io阻塞）
高的安全保障


#### 阻塞IO 

1.定义：在执行IO操作时如果执行条件不满足则阻塞。阻塞IO是IO的默认形态。

2.效率：阻塞IO是效率很低的一种IO。但是由于逻辑简单所以是默认IO行为。
逻辑简单，便于操作

3.阻塞情况：
* 因为某种执行条件没有满足造成的函数阻塞
e.g.  accept   input   recv

* 处理IO的时间较长产生的阻塞状态
e.g. 网络传输，大文件读写
			

####　非阻塞IO

1. 定义 ：通过修改IO属性行为，使原本阻塞的IO变为非阻塞的状态。
因为某种执行条件没有满足造成的函数阻塞

* 设置套接字为非阻塞IO

 >sockfd.setblocking(bool)
 功能：设置套接字为非阻塞IO
 参数：默认为True，表示套接字IO阻塞；设置为False则套接字IO变为非阻塞

* 超时检测 ：设置一个最长阻塞时间，超过该时间后则不再阻塞等待。

	>sockfd.settimeout(sec)
	功能：设置套接字的超时时间
	参数：设置的时间
"""
block_io.py
socket 套接字非阻塞ＩＯ



```
如果没有客户端连接，每隔３秒填充一个日志
"""

from socket import *
from time import sleep,ctime

# 日志文件

f = open('log.txt','a+')

# 创建套接字

sockfd = socket()
sockfd.bind(('127.0.0.1',8888))
sockfd.listen(3)

# 设置套接字为非阻塞

# sockfd.setblocking(False)

# 设置超时检测时间

sockfd.settimeout(3)

while True:
  print("Waiting for connect...")
  try:
    connfd,addr = sockfd.accept()
  except (BlockingIOError,timeout) as e:
    #　如果没有客户端连接，每隔３秒写一个日志
    f.write("%s : %s\n"%(ctime(),e))
    f.flush()
    sleep(3)
  else:
    print("Connect from",addr)
    data = connfd.recv(1024).decode()
    print(data)

### 
```


### IO多路复用

1. 定义
>同时监控多个IO事件，当哪个IO事件 准备就绪 就执行哪个IO事件。以此形成可以同时处理多个IO的行为，避免一个IO阻塞造成其他IO均无法执行，提高了IO执行效率。

2. 具体方案

>select方法 ： windows  linux  unix
>poll方法： linux  unix
>epoll方法： linux


#### select 方法

***代码实现: day5/select_server.py***

```
"""
select tcp服务模型
重点代码

思路分析：
1.将关注的IO放入对应的监控类别列表
2.通过select函数进行监控
3.遍历select返回值列表，确定就绪IO事件
4.处理发生的IO事件
"""

from socket import *
from select import select

# 创建一个监听套接字作为关注的ＩＯ

s = socket()
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(('0.0.0.0',8888))
s.listen(3)

# 设置关注列表

rlist = [s]
wlist = []
xlist = [s]

# 循环监控ＩＯ

while True:
  rs,ws,xs = select(rlist,wlist,xlist)

# 遍历三个返回列表,处理ＩＯ

  for r in rs:
    # 根据遍历到ＩＯ的不同使用ｉｆ分情况处理
    if r is s:
      c,addr = r.accept()
      print("Connect from",addr)
      rlist.append(c) #　增加新的ＩＯ事件
    # else为客户端套接字就绪情况
    else:
      data = r.recv(1024)
      # 客户端退出
      if not data:
        rlist.remove(r) #　从关注列表移除
        r.close()
        continue # 继续处理其他就绪ＩＯ
      print("Receive:",data.decode())
      # r.send(b'OK')
      #　我们希望主动处理这个ＩＯ对象
      wlist.append(r)

  for w in ws:
    w.send(b'OK')
    wlist.remove(w) #　使用后移除

  for x in xs:
    pass

"""
tcp_client.py  tcp客户端流程
重点代码
"""

from socket import *

# 创建ｔｃｐ套接字

sockfd = socket() #　参数默认即ｔｃｐ套接字

# 连接服务端程序

server_addr = ("127.0.0.1",8888)  #　服务端地址
sockfd.connect(server_addr)

while True:

# 消息发送接收

  data = input("Msg>>")

# 如果直接回车，则跳出循环

  if not data:
    break
  sockfd.send(data.encode()) #　转换字节串发送
  data = sockfd.recv(1024)
  print("Server:",data.decode())

sockfd.close()
```





```python
rs, ws, xs=select(rlist, wlist, xlist[, timeout])

select(rlist, wlist, xlist[, timeout]) -> (rlist, wlist, xlist) 
Wait until one or more file descriptors are ready for some kind of I/O.
The first three arguments are sequences of file descriptors to be waited for:
rlist -- wait until ready for reading
wlist -- wait until ready for writing
xlist -- wait for an ``exceptional condition''
If only one kind of condition is required, pass [] for the other lists.
A file descriptor is either a socket or file object, or a small integer
gotten from a fileno() method call on one of those.
The optional 4th argument specifies a timeout in seconds; it may be
a floating point number to specify fractions of seconds.  If it is absent
or None, the call will never time out.

The return value is a tuple of three lists corresponding to the first three
arguments; each contains the subset of the corresponding file descriptors
that are ready.

*** IMPORTANT NOTICE ***
On Windows, only sockets are supported; on Unix, all file
descriptors can be used.
"""
功能: 监控IO事件，阻塞等待IO发生
参数：rlist  列表  存放关注的等待发生的IO事件
      wlist  列表  存放关注的要主动处理的IO事件
      xlist  列表  存放关注的出现异常要处理的IO
      timeout  超时时间
读事件 input accept recv
写事件 send 
异常   
返回值： rs 列表  rlist中准备就绪的IO
        ws 列表  wlist中准备就绪的IO
	      xs 列表  xlist中准备就绪的IO
```
```
"""
select 示例
"""
from socket import *
from select import select

s = socket()
s.bind(('0.0.0.0',8888))
s.listen(3)

print("监控ＩＯ")
rs,ws,xs = select([],[s],[])
print("rlist:",rs)
print("wlist:",ws)
print("xlist:",xs)

select 实现tcp服务
```



	【1】 将关注的IO放入对应的监控类别列表
	【2】通过select函数进行监控
	【3】遍历select返回值列表，确定就绪IO事件
	【4】处理发生的IO事件

>注意
>>wlist中如果存在IO事件，则select立即返回给ws
>>处理IO过程中不要出现死循环占有服务端的情况
>>IO多路复用消耗资源较少，效率较高

------------
###@@扩展: 位运算

定义 ： 将整数转换为二进制，按二进制位进行运算

运算符号： 
>		&  按位与
>		|  按位或
>		^  按位异或
>		<< 左移
>		>> 右移

```python
e.g.  14 --> 01110
      19 --> 10011

14 & 19 = 00010 = 2  一0则0
14 | 19 = 11111 = 31 一1则1
14 ^ 19 = 11101 = 29 相同为0不同为1
14 << 2 = 111000 = 56 向左移动低位补0
14 >> 2 = 11 = 3  向右移动去掉低位
```
----------------
应用层


#### poll方法

***代码实现: day5/poll_server.py***

```
"""
poll 服务端程序
尽量掌握

思路分析：

1. 创建套接字作为监控ＩＯ
2. 将套接字register
3. 创建查找字典，并维护(要时刻与注册ＩＯ保持一致)
4. 循环监控IO发生
5. 处理发生的IO
   """

from socket import *
from select import *

# 创建套接字

s = socket()
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(('0.0.0.0',8888))
s.listen(3)

# 创建ｐｏｌｌ对象关注ｓ

p = poll()

# 建立查找字典，用于通过ｆｉｌｅｎｏ查找ＩＯ对象

fdmap = {s.fileno():s}

# 关注ｓ

p.register(s,POLLIN|POLLERR)

# 循环监控

while True:
  events = p.poll()

# 循环遍历发生的事件　ｆｄ-->fileno

  for fd,event in events:
    #　区分事件进行处理
    if fd == s.fileno():
      c,addr = fdmap[fd].accept()
      print("Connect from",addr)
      #　添加新的关注ＩＯ
      p.register(c,POLLIN|POLLERR)
      fdmap[c.fileno()] = c #　维护字典
    #　按位与判定是ＰＯＬＬＩＮ就绪
    elif event & POLLIN:
      data = fdmap[fd].recv(1024)
      if not data:
        p.unregister(fd) #　取消关注
        fdmap[fd].close()
        del fdmap[fd]  #　从字典中删除
        continue
      print("Receive:",data.decode())
      fdmap[fd].send(b'OK')
```


```python
p = select.poll()
功能 ： 创建poll对象
返回值： poll对象
```


```python	
p.register(fd,event)   
功能: 注册关注的IO事件
参数：fd  要关注的IO
      event  要关注的IO事件类型
  	     常用类型：POLLIN  读IO事件（rlist）
		      POLLOUT 写IO事件 (wlist)
		      POLLERR 异常IO  （xlist）
		      POLLHUP 断开连接 
		  e.g. p.register(sockfd,POLLIN|POLLERR)

p.unregister(fd)
功能：取消对IO的关注
参数：IO对象或者IO对象的fileno
```

```python
events = p.poll()
功能： 阻塞等待监控的IO事件发生
返回值： 返回发生的IO
        events格式  [(fileno,event),()....]
        每个元组为一个就绪IO，元组第一项是该IO的fileno，第二项为该IO就绪的事件类型
```
查找地图

poll_server 步骤
	   
	【1】 创建套接字
	【2】 将套接字register
	【3】 创建查找字典，并维护
	【4】 循环监控IO发生
	【5】 处理发生的IO


#### epoll方法

***代码实现: day5/epoll_server.py***

```
"""
epoll 服务端程序
尽量掌握
"""

from socket import *
from select import *

# 创建套接字

s = socket()
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(('0.0.0.0',8888))
s.listen(3)

# 创建eｐｏｌｌ对象关注ｓ

ep = epoll()

# 建立查找字典，用于通过ｆｉｌｅｎｏ查找ＩＯ对象

fdmap = {s.fileno():s}

# 关注ｓ

ep.register(s,EPOLLIN|EPOLLERR)

# 循环监控

while True:
  events = ep.poll()

# 循环遍历发生的事件　ｆｄ-->fileno

  for fd,event in events:
    print("亲，你有ＩＯ需要处理哦")
    #　区分事件进行处理
    if fd == s.fileno():
      c,addr = fdmap[fd].accept()
      print("Connect from",addr)
      #　添加新的关注ＩＯ
      #　将触发方式变为边缘触发
      ep.register(c,EPOLLIN|EPOLLERR|EPOLLET)
      fdmap[c.fileno()] = c #　维护字典
    #　按位与判定是EＰＯＬＬＩＮ就绪
    # elif event & EPOLLIN:
    #   data = fdmap[fd].recv(1024)
    #   if not data:
    #     ep.unregister(fd) #　取消关注
    #     fdmap[fd].close()
    #     del fdmap[fd]  #　从字典中删除
    #     continue
    #   print("Receive:",data.decode())
    #   fdmap[fd].send(b'OK')
```




1. 使用方法 ： 基本与poll相同

	 * 生成对象改为 epoll()
   * 将所有事件类型改为EPOLL类型
	
2. epoll特点

   * epoll 效率比select poll要高
   内核机制
   select（1024） poll 从应用层拷贝到内核，然后监控，告知应用层，应用层在经过一次轮循，返回给用户处理
   水平触发
   epoll（100000） 直接在内核申请空间，加载到内核空间，注册，加载，就绪之后，内核直接返回给应用层，返回用户处理
   * epoll 监控IO数量比select要多
   * epoll 的触发方式比poll要多 （EPOLLET边缘触发）



### 协程技术

#### 基础概念

1. 定义：纤程，微线程。是为非抢占式多任务产生子程序的计算机组件。协程允许不同入口点在不同位置暂停或开始，简单来说，协程就是可以暂停执行的函数。（生成器函数 yield）
非抢占式 类似于同步行为，主动让出，彼此之间相互协调，可以完成多任务
进程和线程式 抢占式 抢占cpu
产生子程序的计算机组件 程序的封装

2. 协程原理 ： 记录一个函数的上下文栈帧，协程调度切换时会将记录的上下文保存，在切换回来时进行调取，恢复原有的执行内容，以便从上一次执行位置继续执行。
一个函数调用时，会在内存中开辟空间，函数栈帧

3. 协程优缺点
	
>优点
>>1. 协程完成多任务占用计算资源很少
>>2. 由于协程的多任务切换在应用层完成，因此切换开销少
>>3. 协程为单线程程序，无需进行共享资源同步互斥处理

>缺点
>
>> 协程的本质是一个单线程，无法利用计算机多核资源

--------------------------------
####扩展延伸@标准库协程的实现

python3.5以后，使用标准库asyncio和async/await 语法来编写并发代码。asyncio库通过对异步IO行为的支持完成python的协程。虽然官方说asyncio是未来的开发方向，但是由于其生态不够丰富，大量的客户端不支持awaitable需要自己去封装，所以在使用上存在缺陷。更多时候只能使用已有的异步库（asyncio等），功能有限

------------------------------

#### 第三方协程模

1.  greenlet模块

***示例代码: day6/greenlet_0.py***

```
"""
协程运行形态示例
"""
from greenlet import greenlet

def test1():
    print("执行text1")
    gr2.switch()
    print("结束text1")
    gr2.switch()

def test2():
    print("执行text2")
    gr1.switch()
    print("结束text2")

gr1 = greenlet(test1)
gr2 = greenlet(test2)

gr1.switch()  # 选择执行协程1
```



* 安装 ： sudo  pip3 install greenlet

* 函数 

```python
greenlet.greenlet(func)
功能：创建协程对象
参数：协程函数

g.switch()
功能：选择要执行的协程函数
```

2. gevent模块

***示例代码: day6/gevent_test.py***

```
"""
gevent 协程示例
"""
import gevent
from time import sleep

def foo(a, b):
    print("running foo...", a, b)
    print("foo again")

if __name__ == "__main__":
    f = gevent.spawn(foo, 1, 2)
    gevent.joinall([f])
    # gevent.sleep(3)

***示例代码: day6/gevent_server.py***
"""
gevent server基于协程的tcp并发
扩展代码
"""
import gevent
from gevent import monkey

monkey.patch_all()

# 在导入socket之前执行

from socket import *

# 创建tcp套接字

s = socket()
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 6666))
s.listen(8)

def handle(c):
    while True:
        data = c.recv(1224)
        if not data:
            break
        print(data.decode())
        c.send(b"ok")
    c.close()

while True:
    c, addr = s.accept()
    print("connect from", addr)
    # handle(c)
    gevent.spawn(handle, c)

s.close()
```




* 安装：sudo pip3 install gevent

* 函数

```python
gevent.spawn(func,argv)
功能: 生成协程对象
参数：func  协程函数
     argv  给协程函数传参（不定参）
返回值： 协程对象

gevent.joinall(list,[timeout])
功能: 阻塞等待协程执行完毕
参数：list  协程对象列表
     timeout 超时时间

gevent.sleep(sec)
功能: gevent睡眠阻塞
参数：睡眠时间

* gevent协程只有在遇到gevent指定的阻塞行为时才会自动在协程之间进行跳转
如gevent.joinall(),gevent.sleep()带来的阻塞
```

* monkey脚本

>作用：在gevent协程中，协程只有遇到gevent指定类型的阻塞才能跳转到其他协程，因此，我们希望将普通的IO阻塞行为转换为可以触发gevent协程跳转的阻塞，以提高执行效率。

> 转换方法：gevent 提供了一个脚本程序monkey,可以修改底层解释IO阻塞的行为，将很多普通阻塞转换为gevent阻塞。

> 使用方法

>>【1】 导入monkey

			from gevent  import monkey

>>【2】 运行相应的脚本，例如转换socket中所有阻塞

			monkey.patch_socket()

>>【3】 如果将所有可转换的IO阻塞全部转换则运行all

			monkey.patch_all()

>>【4】 注意：脚本运行函数需要在对应模块导入前执行



### HTTPServer v2.0 

***day6/http_server.py***

  1. 主要功能 ：
	  【1】 接收客户端（浏览器）请求
		【2】 解析客户端发送的请求
		【3】 根据请求组织数据内容
		【4】 将数据内容形成http响应格式返回给浏览器
	
	2. 升级点 ：
	    【1】 采用IO并发，可以满足多个客户端同时发起请求情况
		【2】 做基本的请求解析，根据具体请求返回具体内容，同时满足客户端简单的非网页请求情况

    【3】 通过类接口形式进行功能封装

```
接口设计
1.提供句柄，通过句柄调用属性方法解决问题（句柄，fd就是句柄，对象）
fd = open()
sockfd = socket()
lock = Lock()
db = pymysql.connect()
2.实例化对象，通过对象设置，启动服务
t = Thread()
p = Process()
s = socketserver()
通过对象启动服务

参数根据功能需求，如果无法替使用者决定的内容，通过参数传递

如果能够解决的问题，不要让用户解决，需要用户解决的问题可以用重写的方式让用户重写
技术分析：
1.http协议熟悉
2.select 并发
3.使用tcp套接字
4.使用类进行封装

从使用者的角度分析问题：
```

```
"""
http server 2.0
io 多路复用 http 练习
思路分析：
1.使用类进行分装
2.从用户使用角度决定类的编写

"""
from socket import *
from select import select

# 具体的http server功能

class HTTPServer:
    def __init__(self, host, port, dir):
        self.address = (host, port)
        self.host = host
        self.port = port
        self.dir = dir
        self.create_socket()
        self.bind()
        self.rlist = []
        self.wlist = []
        self.xlist = []
# 创建套接字
def create_socket(self):
    self.sockfd = socket()
    self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

def bind(self):
    self.sockfd.bind(self.address)

def handle(self, c):
    # 接受客户端请求
    request = c.recv(4096)
    # 防止客户端断开
    if not request:
        self.rlist.remove(c)
        c.close()
        return
    # 提取请求
    request_line = request.splitlines()[0]
    info = request_line.decode().split(" ")[1]
    print(c.getpeername(), ":", info)
    # info分为网页或者其他内容
    if info == "/" or info[-5:] == ".html":
        self.get_html(c, info)
    else:
        self.get_data(c)

def get_data(self, connfd):
    responseHeaders = "HTTP/1.1 200 OK\r\n"
    responseHeaders += "Content-Type:text/html\r\n"
    responseHeaders += "\r\n"
    responseBody = "<h1>waiting for httpserver 3.0</h1>"
    response = responseHeaders + responseBody
    connfd.send(response.encode())

def get_html(self, connfd, info):
    if info == "/":
        filename = self.dir + "/index.html"
    else:
        filename = self.dir + info
    try:
        fd = open(filename)
    except Exception:
        # 没有网页
        responseHeaders = "HTTP/1.1 404 Not Found\r\n"
        responseHeaders += "\r\n"
        responseBody = "<h1>sorry,Not found the page</h1>"
        # response = responseHeaders + responseBody
        # connfd.send(response.encode())
    else:
        responseHeaders = "HTTP/1.1 200 OK\r\n"
        responseHeaders += "\r\n"
        responseBody = fd.read()
    finally:
        response = responseHeaders + responseBody
        connfd.send(response.encode())

# 启动服务
def serve_forever(self):
    self.sockfd.listen(5)
    print("listen the port %d" % self.port)
    self.rlist.append(self.sockfd)
    while True:
        rs, ws, xs = select(self.rlist, self.wlist, self.xlist)
        for r in rs:
            if r is self.sockfd:
                c, addr = r.accept()
                print("connect from", addr)
                self.rlist.append(c)
            else:
                # 处理请求
                self.handle(r)
        for w in ws:
            pass
        for x in xs:
            pass
if __name__ == "__main__":
    # 希望通过http server类快速的搭建http服务用以展示自己的网页
    # 用户自己决定的内容以参数的形式传递
    HOST = "0.0.0.0"
    PORT = 8000
    DIR = "./static"
    # 网页存储位置
    httppd = HTTPServer(HOST, PORT, DIR)
    # 实例化对象
    # 启动http服务
    httppd.serve_forever()
```













