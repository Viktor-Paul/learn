# **shell_day01_回顾**

- **变量**

```shell
#  = 左右两侧不能有空格
1、自定义变量
2、环境变量
3、位置变量
4、预定义变量 : $# $* $?
```

- **算术运算命令**

```shell
1、`expr n1 + n2`
2、$[n1+n2]
3、let i++
```

- **条件判断**

```shell
 # [ 条件 ]
 1、字符比较:  ==  !=  -z
 2、数值比较:  -gt -ge -lt -le -eq
 3、文件|目录比较: -e !-e -f -d 
```

- **if分支结构**

```shell
if [ 条件 ];then
	语句
elif [ 条件 ];then
	语句
else
	语句
fi
```

- **for循环**

```shell
# for
for 变量名 in `seq {1..5}`
do
	循环体
done

# cfor
for ((i=1;i<=10;i++))
do
	循环体
done
```

- **while循环**

```shell
while [ 条件 ]
do
	循环体
done

# 死循环
while :
do
	循环体
done
```

- **sed**

```shell
sed -i '' file.txt
sed -n '' file.txt

1、增   : a | i
2、删   : d
3、改   : c
4、查   : p
5、替换 : s
```

- **其他**

```shell
1、获取随机数
  $[RANDOM%num]
```

# **shell_day02_笔记**

- **作业**

**用户从终端输入名字，创建该目录，回车直接退出**

```shell
/home/tarean/libai
判断路径是否存在
不存在:创建
#!/bin/bash
if [ -d /home/tarena/libai ];then
        echo "文件已存在"
else
        mkdir /home/tarena/libai
        echo "文件已创建"
fi


# 2.用户从终端输入要创建的目录名,存在则告知用户,否则帮用户创建此目录
终止条件,用户什么都不输入
#!/bin/bash
read -p "请输入要创建的文件目录名:" filename
if [ -z $filename ];then
        exit
elif [ -d $filename ];then
        echo "文件已存在"
else
        mkdir $filename
        echo "$filename文件目录已创建"
fi

```



- **until循环**

```shell
# 1、特点
条件判断不成立时执行循环体,成立时循环结束

# 2、语法格式
until [ 条件 ]
do
	循环体
done

# 3、示例:把172.40.91.10-15内不在线的IP输出来
#!/bin/bash

x=10
until [ $x -gt 15 ]
do
        ping -c 2 172.40.74.$x &> /dev/null
        if [ $? -eq 1 ];then
                echo "172.40.74.$x 不在线"
                let x++
        fi
done
```

- **case分支结构**		

```shell
# 1、特点
根据变量值的不同,执行不同的操作

# 2、语法格式
case $变量名 in
模式1)
	代码块 
	;;
模式2)
	代码块
	;;
*)
	代码块
	;;
esac

# 3、示例 : 输入一个字符,判断是数字、字母还是其他字符
#!/bin/bash
read -p "请输入一个字符:" char
# 判断用户输入的是否是一个字符
if [ ${#char} -ne 1 ];then
        echo "你输入的不是一个字符!"
        exit
fi
case $char in
        [0-9])
                echo "$char 是一个数字"
                ;;
        [a-Z])
                echo "$char 是一个字母"
                ;;
        *)
                echo "$char 是特殊字符"
                ;;
esac
# 4、练习 : 编写1个nginx的启动脚本，包含: start stop restart
#!/bin/bash

echo "请输入对nginx的操作:(start|stop|restart)"
read -p "请输入操作命令:" input
case $input in
        start)
                sudo /etc/init.d/nginx start
                ;;
        stop)
                sudo /etc/init.d/nginx stop
                ;;
        restart)
                sudo /etc/init.d/nginx restart
                ;;
        *)
                echo "Useage Please input start|stop|restart !"
esac

```

**知识点总结**

```shell
# 1、获取字符串长度
${#变量名}

# 2、字符串索引及切片
${string:index:number} # number为取元素的数量
key='ABCDE'
${key:0:1} # A 获取下表索引为0的元素
${key:1:2} # BC

# 3、vim批量缩进
1、进入命令行模式 : shift + :
2、1,3> + Enter  : 1-3行缩进
3、1,3< + Enter  : 1-3行往回缩进
```

- **函数**

- **补充一点点Linux命令**

  ```shell
  # 复制文件|目录
  1 文件 : cp src.txt (可以多个文件)+ 路径
  2 目录 : cp -r dir1 + 路径
  ~ 表示/home/tarena
  linux下重命名文件或文件夹的命令mv既可以重命名，又可以移动文件或文件夹
  例子：将目录A重命名为B
  mv A B
  例子：将/a目录移动到/b下，并重命名为c
  mv /a /b/c
  其实在文本模式中要重命名文件或目录的话也是很简单的，我们只需要使用mv命令就可以了，比如说我们要将一个名为abc的文件重命名为1234就可以这样来写：mv abc 1234，但是要注意的是，如果当前目录下也有个1234的文件的话，我们的这个文件是会将它覆盖的
  ```

```shell
# 1、语法格式
函数名(){
	代码块
}
函数名  # 函数调用,不能加()

# 2、示例: 打印10个*
star(){
	echo "**********"
}
star # 第1次调用
star # 第2次调用

# 3、练习: 写1个计算器程序,计算 加 减 即可 -- 函数+case
#!/bin/bash

read -p "请输入第一个数字:" number1
read -p "请输入第二个数字:" number2
read -p "请选择要计算的方式(+-*/)" option

sumx(){
	echo $[$number1+$number2]
}
subx(){
        echo $[$number1-$number2]
}

case $option in
	+)
		sumx
		;;
	-)
		subx
		;;
	*)
		echo "操作符无效"
esac

```

**练习**

```shell
在用户主目录下创建一个目录,如果存在则提示,否则提示创建成功
#!/bin/bash
fun01(){
        read -p "请输入要创建的文件夹:" filename
        directory=/home/tarena/$filename
        if [ -e $directory ];then
                echo "$filename已存在"
        else
                mkdir $directory
                echo "$filename创建成功"
        fi
}
fun01
```

- **字符串处理 - ${变量名  替换符号 匹配条件}**

**从左向右删除**

```shell
# 1、语法
${变量名##匹配条件}

# 2、示例
directory="/home/tarena/mysql"   # 注意{}中不需要加空格
echo ${directory##*/}   --> mysql 
echo ${directory#*/}    --> home/tarena/mysql
```

**从右向左删除**

```shell
# 1、语法
${变量名%%匹配条件}

# 2、示例
directory="/home/tarena/mysql"
echo ${directory%%/mysql}   --> /home/tarena
echo ${directory%/*}        --> /home/tarena
echo ${directory%%/*}       --> ""

shell中的字符串操作——字符串的切割总结

1、${var#}
#! /bin/bash
var=“www.google.com”
echo ${var#*.*. }
echo ${var#*.}
输出结果为：
com
google.com

在这里 ${var#} 意思是从前向后（从左向右）截取，如上面的 ${var#*.*.} 的意思是从左到右截取第二个 . 后面的所有内容，也就是 com。 ${var#*.} 也就是截取第一个点后面的所有内容， google.com。（这里面的 * 是匹配任意多个字符的意思，正则匹配）

2、${var##}
#! /bin/bash
var=“www.google.com”
echo ${var##*.}
输出结果为：
com

${var##} 是从左向右截取最后一个 . 后（右边）的所有内容。

3、${var%}
#! /bin/bash
var=“www.google.com”
echo ${var%.*.*}
echo ${var%.*}
输出结果为：
www
www.google

用法 ${var##} 和相似，不过 ${var%} 是从后往前（从右向左）截取，第一个为从右向左截取第二个 . 左边的内容 www，第二个是从右向左截取第一个 . 左边的所有内容 www.google 。

4、${var%%}
#! /bin/bash
var=“www.google.com”
echo ${var%%.*}
输出结果为：
www

${var%%} 是从右向左截取最后一个 . 后（左边）的所有内容。

5、步长截取法 ${var:num1:num2}
#! /bin/bash
var=“www.google.com”
echo ${var:2:5}
echo ${var:0-5:3}
echo ${var:6}
输出结果为：
ww.go
.co
oogle.com

${var:2:5} 从第二位开始（包括第二位）截取5个字符
${var:0-5:3} 从倒数第五位开始（不包括倒数第五位）截取3个字符（可以把0-5看成-5，同样1-6也是这样，看成-5，结果和0-5一样）
${var:6} 从第六位开始（包括第六位）截取剩余所有字符
```

**案例**

```shell
输出系统中的前10个用户
#!/bin/bash

# root:x:0:0:root:/root:/bin/bash
for line in `head -10 /etc/passwd`
do
        echo ${line%%:*}
done


# 2.
awk -F ':' '{print $1}' /etc/passwd | head -10

# 3.
sed 's/:.*//g' /etc/passwd | head -10
```

**练习**

```shell
批量修改文件名 : 把当前目录下的.txt文件全部改为.doc文件
#!/bin/bash

for file in `ls *.txt`
do
        mv $file ${file%.*}.doc
done
```

- **shell磨练**

**1、依次提示用户输入3个整数，脚本根据数字大小依次排序输出 3个数字**

```shell
#!/bin/bash

read -p "请输入第一个数字" n1
read -p "请输入第二个数字" n2
read -p "请输入第三个数字" n3

if [ $n1 -ge $n2 ];then
        temp=$n1
        n1=$n2
        n2=$temp
#echo "数字从小到大为 $n1 $n2"
fi
if [ $n1 -ge $n3 ];then
        temp1=$n1
        n1=$n3
        n3=$temp1
fi
if [ $n2 -ge $n3 ];then
        temp2=$n2
        n2=$n3
        n3=$temp2

fi
echo "数字从小到大为 $n1 $n2 $n3"

```

**2、编写脚本，实现人机<石头，剪刀，布>游戏** 

```shell
# 提示 - Linux中数组使用
# Linux数组: (元素1 元素2 元素3)  元素之间用空格隔开
game=("石头" "剪刀" "布") 
```

​	**代码实现**

```shell
#!/bin/bash
game=("石头" "剪刀" "布")
computer=${game[$[RANDOM%3]]}
echo "$computer"
read -p "请输入(石头|剪刀|布)" you
if [ $computer == $you ];then
       echo "这是平局"
elif ([ $computer == "石头" ] && [ $you == "剪刀" ]) || ([ $computer == "剪刀" ] && [ $you == "布" ]) || ([ $computer == "布" ] && [ $you == "石头" ]);then
        echo "你输了"
else
        echo "你赢了"
fi

```

**3、每2秒中检测一次MySQL数据库的连接数量**

```mysql
# mysqladmin命令
mysql服务器管理任务的工具，它可以检查mysql服务器的配置和当前工作状态
mysqladmin -uroot -p123456 status
mysqladmin: [Warning] Using a password on the command line interface can be insecure.
Uptime: 31201  Threads: 1  Questions: 6  Slow queries: 0  Opens: 105  Flush tables: 1  Open tables: 98  Queries per second avg: 0.000
```

​	**代码实现**

```shell
#!/bin/bash

while :
do
        count=`mysqladmin -uroot -p123456 status | awk '{print $4}'`
        echo "`date +%F` 并发连接数为$count"
        sleep 2
done
```

**4、根据md5校验码，检测文件是否被修改**

```shell
# 1、生成md5的文件校验码
md5sum nginx.conf
```

​	**代码实现**

```shell
#!/bin/bash

for file in `ls /etc/*.conf`
do
        md5sum $file >> md5log2.txt
done


tarena@tarena:~/shell/day02$ diff md5log.txt md5log22.txt
11c11
< 89408008f2585c957c031716600d5a80  /etc/host.conf
---
> 37aa7b2b356da60b35482b8656108c48  /etc/host.conf

```

**5、备份MySQL数据库**

```mysql
# mysql数据库备份
mysqldump -hip -uroot -p123456 库 > xxx.sql

#!/bin/bash

user="root"
password="123456"
dbname="mysql"

date=$(date +%Y%m%d)
[ ! -d /home/tarena/backup ] && mkdir /home/tarena/backup
mysqldump -u"$user" -p"$password" "$dbname" > /home/tarena/backup/"$dbname"-${date}.sql

```

**6、随机生成8为密码**

```shell
# 1.获取字符串长度:${#变量名}
# 2.字符串的切片和索引 ${变量名:起始索引:数量}
#!/bin/bash
key="0123456789abcdefghigklmnopqrstuvwxyzABCDEFGHIGKLMNOPQRSTUVWXYZ_"
length=${#key}
pass=''
for i in {1..8}
do 
        pass=$pass${key:$[RANDOM%$length]:1}
done
echo $pass


```







