# **shell编程 - Day01笔记**



- **Shell格式**

```shell
# 解释器 bash / sh
1、扩展名: xxx.sh
2、正文第一行必须指定解释器: #!/bin/bash
```

-  **shell执行方式**

```shell
# 方式一: 加权限,  ./xxx.sh 执行
1、chmod +x  xxx.sh
2、./xxx.sh

# 方式二: 手动指定解释器
bash xxx.sh
```

- **自定义变量**

```shell
# 1. 定义变量
变量名=值    ---->  注意: =两侧绝对不能有空格
eg1: name="take me to your heart"

# 2. 调用变量的格式
echo $变量名

# 01_variable_1.sh
name="风云雄霸天下"
echo $name
     
# 3. 小细节: 单引号和双引号的区别
单引号: 在输出的时候无法获取变量的值 
双引号: 可以获取变量的值 
```

- **环境变量+位置变量+预设变量**

```shell
# 普通用户信息
tarena : x  :		1000	:	1000	:	tarena,,,	:	/home/tarena	:	/bin/bash
用户名 密码占位符  UID		 GID     用户描述     用户的主目录      登录权限
# 环境变量
echo $USER   --  当前用户
echo $UID    --  当前用户的UID号
echo $PWD    --  当前路径
echo $PATH   --  命令搜索路径

# 位置变量
$1 $2 $3 ... ... shell的位置变量
./xxx.sh 1 2

python 的位置变量
sys.argv  -->列表
sys.argv[0] -->文件名
sys.argv[1] -->第一个命令行参数
'''计算和'''
import sys
print(sys.argv)
length= len(sys.argv)
if length == 3:
    number = int(sys.argv[1]) +int(sys.argv[2])
    print('{}+{}={}'.format(sys.argv[1],sys.argv[2],number))
else:
    print('参数个数有误')
# print(number)
tarena@tarena:~/day01$ python3 hello.py 3
['hello.py', '3']
参数个数有误
tarena@tarena:~/day01$ python3 hello.py 3 5
['hello.py', '3', '5']
3+5=8

# 预定义变量
$# $* $?

# $? : 返回上一条命令执行的状态(0代表正确,非0代表失败)
# $# 参数的个数
# $* 获取所有参数的值
```

**练习**

```shell
输出$1+$2,例如输出结果: 3+5
#!/bin/bash
echo $1+$2
```

- **变量赋值 - 接收用户从终端输入的值**

```shell
# 语法格式
read -p 提示信息 变量名

# 05_read.sh
#!/bin/bash
read -p 请输入姓名: name
echo "您输入的姓名是:$name"

# 指定超时时间
read -p 提示信息 变量名
read -t n -p 提示信息 变量名

# 06_read_t.sh 限制3秒中之内必须输入值
#!/bin/bash
read -t 3 -p 请输入用户名: username
```

**练习**

```shell
1、输入学生姓名: 赵敏
2、输入学生成绩: 88
3、输出: 赵敏的成绩为88分
```

**Ubuntu设置sudo免密码**

```shell
# 通过更改 /etc/sudoers 实现
1、备份: sudo cp /etc/sudoers .
2、修改: sudo vi /etc/sudoers
   添加: tarena ALL=(ALL) NOPASSWD : ALL
```

**练习**

```shell
请使用位置变量的方式实现用户名的创建
#!/bin/bash

#read -p "请输入用户:" username
#sudo useradd $username
#echo "$username创建成功"

sudo useradd $1
echo "$1创建成功"
```

- **shell - 算术运算符**

```shell
# 运算符
1、+ - * / % 
2、++ : 自加1运算,类似于python中 i++  等同于 i+=1
3、-- : 同++
			
# 运算命令
1、let 运算表达式
	i=1
	let i++
	echo $i
2、expr 运算表达式
	i=1
	sum=`expr $i + 5` # +两侧要有空格
	echo $sum
3、$[]
	echo $[1+1]
	echo $[1-1]
	echo $[a+a] # 调用变量不用多次添加$符号
	echo $[1*1] # 乘法无需转义
```

**练习**

```shell
使用 位置变量+以上方法一、二中任何一种,实现2个数字的相加
#!/bin/bash
echo $[$1+$2]
echo `expr $1 + $2`
```

- **shell - 比较运算符**

```shell
# 语法格式
 [  判断语句  ]      # 注意括号必须有空格
# 组合
&& 并且
|| 或者
A命令  &&  B命令   //仅当A成功时才执行B
A命令  ||  B命令   //仅当A失败时才执行B
思考: [ a == a ] && echo Y || echo N 代表什么意思？

# 1、字符比较
[ A == A ]    #相等(等号两边需要有空格)
[ A != B ]    #不相等
[ -z $变量 ]  #判断是否为空
思考(Y 还是 N):  [ $USER == tarena ] && echo Y || echo N

练习: 用户输入用户名，不存在时则创建，否则不做任何操作
#!/bin/bash

# 2、数字比较
	-eq	等于(equal)
	-ne	不等于(not equal)
	-gt	大于(greater than)
	-ge	大于等于(great or equal)
	-lt	小于(less than)
	-le	小于等于(less or equal)
思考输出什么:
[ 10 -eq 10 ] && echo Y || echo N
[ 11 -le 10 ] && echo Y || echo N
[ 12 -ge 3 ] && echo Y || echo N

# 3、文件|目录比较
   [ -e 文件或目录 ]    #是否存在exist
   [ -f  文件 ]    #存在且为文件file
   [ -d  目录 ]    #存在且为目录directory
   [ -r 文件或目录 ]    #判断是否可读read
   [ -w 文件或目录 ]    #判断是否可写write
   [ -x 文件或目录 ]    #判断是否可执行
思考输出:
	[ -e /etc/passwd ] && echo Y || echo N 
	[ -f /etc/passwd ] && echo Y || echo N
	[ -d /etc/passwd ] && echo Y || echo N
```

**if分支结构**

```shell
# 1、单分支语法格式
     if 判断 ;then
        命令
        命令
     fi
# 2、双分支语法格式
	if 判断 ;then
		命令1
	else
		命令2
	fi
# 3、多分支语法格式
  if 判断;then
    命令1
  elif 判断 ;then
    命令2
  else
    命令3
  fi
# 示例
#!/bin/bash
if [ $USER == tarena ];then
	echo "Yes,You are Tarena."
else
	echo "You are other man."
fi
```

**练习**

```shell
使用shell编写猜数字游戏,无须循环
# 计算机随机出数字:computer=$RANDOM
#!/bin/bash 

#生成1-5直接的随机整数
computer=$[RANDOM%5+1]
echo $computer
read -p "请猜数字:" you

if [ $you -eq $computer ];then
        echo '恭喜,猜对了'
        exit
elif [ $you -lt $computer ];then
        echo '猜小了'
else
        echo '猜大了'
fi
```

- **for循环**

```shell
# 语法格式
for 变量 in 值序列
do
	命令
done
# 示例
for i in 1 2 3 4 5
do
	echo "hello world"
done
# 示例1
#!/bin/bash
# 打印1-5之间的整数
for i in 1 2 3 4 5
do
        echo $i
done

# 示例2
#!/bin/bash
# 打印1-5之间的整数
#for i in 1 2 3 4 5
for i in {1..5}
do
        echo $i
done

# 当前文件中所有的sh文件
#for file in  *.sh
for file in `ls *.sh`
do
        echo $file
done

```

队列
seq 

```bash
seq 5 --> 1 2 3 4 5
seq 3 8 --> 3 4 5 6 7 8
seq 1 2 10 --> 1 3 5 7 9
# 一般用于for循环
for num in `seq 10`
do 
	echo 
done
```

练习**

```shell
把猜数字游戏改为for循环，猜测100次
#!/bin/bash

computer=$[RANDOM%10000+1]
for i in {1..30}
do
        read -p "请猜数字:" you
if [ $computer -eq $you ];then
        echo "猜对了"
        exit
elif [ $computer -lt $you ];then
        echo "猜大了"
else
        echo "猜小了"
fi
done
# 练习:判断指定网段的IP地址哪些可以用,哪些不能用？
ping -c  2 172.40.74.2 
# 垃圾回收
ls &> /dev/null
```

c-for 循环

```
for((赋初值;条件;步长))
do 
	执行命令
done
```



- **while循环**

```shell
# 语法格式
while 条件判断
do
	命令
done

# 示例
#!/bin/bash
i=1
while [ $i -lt 5 ]
do
   echo baby
   let i++
done

# 死循环
while :
do
	执行命令
done
```

 **sed文本处理工具**

```shell
# 1.定义
非交互式文本编辑器,逐行处理

# 2.语法格式
sed [选项] '条件指令' 文件名
指令:增删改查

# 查 -p
sed -n (屏蔽终端输出) 'p' 文件名 # 打印文件所有内容
sed -n '1p' file.txt # 打印文件第1行
sed -n '1,3p' file.txt # 打印文件第1-3行
sed -n '1p;3p' file.txt # 打印文件第1,3行

# 删 -d
sed -i 'd' file.txt # 删除文件的第一行
sed -i '$d' file.txt # 删除文件的最后一行

# 增 -a i
a:在当前处理行的下一行插入
i:在当前处理行的上一行插入
sed -i 'a内容' file.txt 每一行的下一行插入内容


# 改 - c
sed -i 'c内容' file.txt # 修改所有行内容 
sed -i -e '1c内容' -e '3c杜甫' file.txt 

# 文本替换 -s
sed -i '条件s/原内容/新内容/选项' file.txt
选项:g 表示全局替换 i 忽略字母大小写
# sed -i 's/李白/李清照/g' file.txt
```

**练习:**

```
每个一秒中,从1个文件中随机取出1行,在终端显示

查询 
1.文件有多少行,利用$random 取出随机数
wc -l file.txt 返回行数
number=$(wc -l file.txt)
number=$(sed -n '$=' file.txt)

2.sed -n '1p' file.txt

#!/bin/bash

# 获取行数
#number=$(wc -l 17.sh)
file="17.sh"
number=$(sed -n '$=' $file)
echo "$number"
while :
do
        clear
        num=$[RANDOM%number+1]
        echo "$num"
        sed -n "${num}p" $file
        sleep 1
done

```

**文件|目录判断示例**

```
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











