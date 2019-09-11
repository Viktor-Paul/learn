[TOC]
# 一、尺寸与颜色单位
## 1.  尺寸单位
- px 像素单位
-  % 百分比，参照父元素对应属性的值进行计算
- em 字体尺寸单位，参照父元素的字体大小计算，1em=16px
- rem字体尺寸单位,参照根元素的字体大小计算，1rem=16px
## 2.  颜色单位
- 英文单词：red，green，blue
- rgb(r,g,b) 使用三原色表示，每种颜色取值0~255
- rgba(r,g,b,alpha) 三原色每种取值0~255，alpha取值0（透明）~1（不透明）
- 十六进制表示：以#为前缀，分为长十六进制和短十六进制。
  - 长十六进制：每两位为一组，代表一种三原色；每位的取值范围0~9，a~f
    例：red rgb(255,0,0) #ff0000
  - 短十六进制：由3位组成，每一位代表一种三原色，浏览器会自动对每一位进行重复扩充，仍然按照长十六进制解析
    例：#000  #fff   #f00

# 2. CSS 盒模型
## 1.  内容尺寸
- 一般情况下，为元素设置width/height，指定的是内容框的大小

- 内容溢出：内容超出元素的尺寸范围，称为溢出。默认情况下溢出部分仍然可见，可以使用overflow调整溢出部分的显示,取值如下：

  | 取值    | 作用                           |
  | ------- | ------------------------------ |
  | visible | 默认值，溢出部分可见           |
  | hidden  | 溢出部分隐藏                   |
  | scroll  | 强制在水平和垂直方向添加滚动条 |
  | auto    | 自动在溢出方向添加可用滚动条   |
## 2.  边框
### 1. 边框实现
语法：
```css
border:width style color;
```
边框样式为必填项，分为：

| 样式取值 | 含义     |
| -------- | -------- |
| solid    | 实线边框 |
| dotted   | 点线边框 |
| dashed   | 虚线边框 |
| double   | 双线边框 |

### 2. 单边框设置
分别设置某一方向的边框，取值：width style color;

| 属性          | 作用       |
| ------------- | ---------- |
| border-top    | 设置上边框 |
| border-bottom | 设置下边框 |
| border-left   | 设置左边框 |
| border-right  | 设置右边框 |


### 3. 网页三角标制作
1. 元素设置宽高为0

2. 统一设置四个方向透明边框

3. 调整某个方向边框可见色

   ```css
   width:0px;
   height:0px;
   border:10px solid transparent;
   border-top:10px solid red;
   ```
### 4. 圆角边框
1. 属性：border-radius 指定圆角半径
2. 取值：像素值或百分比
3. 取值规律：
```
一个值 	表示统一设置上右下左
四个值 	表示分别设置上右下左
两个值 	表示分别设置上下 左右
三个值 	表示分别设置上右下，左右保持一致
```
### 5. 轮廓线
1. 属性：outline
1. 取值：width style color
1. 区别：边框实际占位，轮廓不占位
1. 特殊：取none可以取消文本输入框默认轮廓线
### 6. 盒阴影
1. 属性：box-shadow
1. 取值：offsetX offsetY(水平和垂直方向的偏移量) blur (spread 延伸) color;
1. 使用：
不管是浏览器窗口还是元素自身都可以构建坐标系，统一以左上角为原点，向右向下为X轴和Y轴的正方向
```
offsetX 	取像素值，阴影的水平偏移距离
offsetY 	取像素值，阴影的垂直偏移距离
blur 		取像素值，表示阴影的模糊程度，值越大越模糊
spread 		选填，取像素值，阴影是否需要延伸
color 		设置阴影颜色,默认为黑色
```
## 3. 内边距
1. 属性：padding
2. 作用：调整元素内容框与边框之间的距离
3. 取值：
```
20px;					一个值表示统一设置上右下左
20px 30px;				两个值表示分别设置(上下) (左右)
20px 30px 40px;			三个值表示分别设置上右下，左右保持一致
20px 30px 40px 50px;	表示分别设置上右下左
```
4. 单方向内边距,只能取一个值：
```
padding-top
padding-right
padding-bottom
padding-left
```
## 4. 外边距
1. 属性：margin

1. 作用：调整元素与元素之间的距离

1. 特殊：
    		1）margin:0; 取消默认外边距
      2）margin:0 auto;左右自动外边距，实现元素在父元素范围内水平居中
      3）margin:-10px;元素位置的微调
      
1. 单方向外边距：只取一个值
    				  margin-top
        		margin-right
        		margin-bottom
        		margin-left
      
1. 外边距合并：
    		1）垂直方向
        			1. 子元素的margin-top作用于父元素上
      
        				解决：
        					为父元素添加顶部边框；
        					或为父元素设置padding-top:0.1px;
      
        			2. 元素之间同时设置垂直方向的外边距，最终取较大的值
      
          2）水平方向
            
            块元素对盒模型相关属性（width,height,padding,border,margin）完全支持;
            行内元素对盒模型相关属性不完全支持，不支持width/height,不支持上下边距
            行内元素水平方向上的外边距会叠加显示
            带有默认边距的元素：
            body,h1,h2,h3,h4,h5,h6,p,ul,ol{
            margin:0;
            padding:0;
            list-style:none;
            }
## 5. 元素最终尺寸的计算
  	盒模型相关的属性会影响元素在文档中的实际占位，进而影响布局
  	属性：box-sizing
  	取值：content-box/border-box
  	1）标准盒模型计算：各个属性值累加得到最终尺寸
  		box-sizing:content-box;
  		元素设置width/height指定的是内容框的大小
  		最终尺寸 = width/height+padding+border+margin
  	2）特殊盒模型计算（按钮元素）：
  		box-sizing:border-box;
  		元素设置width/height指定的是包含边框在内的区域大小
  			最终尺寸 = width/height+margin

 作业：
 1.在横向导航栏的基础上，调整导航项的边距

 2.整体导航栏水平居中

 3.导航项之间10px的外边距

```html
***homework.html***
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>document</title>
    <style>
        #nav,#search{
            width:650px;
            margin:0px auto;
        }
        #nav{
            margin-bottom:50px;
            height:30px;
            background:gray;
            font-size:0px;
        }
        a{

            display:inline-block;
            text-decoration:none;/*取消超链接下划线*/
            color:#fff;
            width:122px;
            height:30px;
            font-size:20px;
            background:green;
            /*调整元素之间的边距,行内块元素是完全支持盒模型属性的
            margin:5px 10px;*/
            margin-right:10px;
            text-align:center;
            line-height:30px;
        }
        a:hover{
            background:red;
        }
        .no-margin{
            margin-right:0px;
        }
        #search{
            height:200px;
            /*background:gray;*/

        }
        input{
            width:500px;
            height:50px;
            /*调整盒模型的计算方式，取值为border-box时,表示当前元素指定的
            width/height是包含边框在内区域的尺寸*/
            box-sizing:border-box;
            border:1px solid #5e5ef1;
            padding:5px 10px;
        }
        input:hover{
            outline:none;
        }
        button{
            /*水平方向上元素之间的垂直对齐方式，可取：top/middle/bottom*/
            vertical-align:bottom;
            width:150px;
            height:50px;
            box-sizing:border-box;
            background:#5e5ef1;
            color:#fff;
            border:1px solid #5e5ef1;
        }
    </style>
</head>
<body>
    <!--导航栏-->
    <div id="nav">
        <a href="">天猫</a>
        <a href="">天猫</a>
        <a href="">天猫</a>
        <a href="">天猫</a>
        <a href="" class="no-margin">天猫</a>
    </div>
    <!--搜索栏-->
    <div id="search">
        <input type="text"><button>百度一下</button>
    </div>
</body>
</html>
```

```color.html
color.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>document</title>
    <style>
        div{
            width:600px;
            height:300px;
            background:red;
            font-size:20px;
        }
        h1{
            width:50%;
            height:50%;
            background:green;
        }
    </style>
</head>
<body>
    <div>
        <h1>隔壁老王</h1>
    </div>
</body>
</html>
```

02_size_oversize

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>document</title>
    <style>
        div{
            width:200px;
            height:200px;
            background:#ff9999;
            font-size:32px;
            overflow:auto;

        }
    </style>
</head>
<body>
    <div>
        盒模型主要包含内容框,边框和内外边框,关系元素的样式和在
        文档中的实际占位
    </div>
</body>
</html>
```

03_border

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>document</title>
    <style>
        h1{
            width:300px;
            height:100px;
            background:pink;
        }
        #d1{
            border:solid;
        }
        #d2{
            border:5px solid red;
        }
        #d3{
            border:5px dotted green;
        }
        #d4{
            border:5px dashed blue;
        }
        #d5{
            border:5px double gray;
        }
        #d6{
            /*
            width:0px;
            height:0px;
            border-top:30px solid red;
            border-right:30px solid transparent;
            border-bottom:30px solid transparent;
            border-left:30px solid transparent;
            */
            width:0px;
            height:0px;
            border:10px solid transparent;
            border-top:10px solid red;

        }
        span{
            /*display:inline-block
            width:0px;
            height:0px;
            */
            /*行内元素默认不能手动调宽高，空标签默认宽度为0,默认高度
            与字体大小有关,可以设置字体大小为0实现高度为0的效果*/
            font-size:0px;
            border-top:10px solid red;
            border-right:10px solid green;
            border-bottom:10px solid blue;
            border-left:10px solid gray;
        }
    </style>
</head>
<body>
    <div id="d6"></div>
    <span></span>
    <h1 id="d1"></h1>
    <h1 id="d2"></h1>
    <h1 id="d3"></h1>
    <h1 id="d4"></h1>
    <h1 id="d5"></h1>
</body>
</html>
```

04_border_radius

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>document</title>
    <style>
        div{
            width:300px;
            height:50px;
            background:orange;
            /*统一设置四个方向*/
            border-radius:25px;
            /*参照元素自身尺寸,分别计算横轴半径和纵轴半径
            统一设置四个角的圆角半径时,最多取到50%,改变元素形状*/
            /*border-radius:50%;*/
        }
        h1{
            width:200px;
            height:200px;
            background:orange;
            /*过渡属性：在元素两种状态切换时添加平滑过渡效果
            transition:3s;*/
        }
        h1:hover{
            border-radius:100px;
            background:blue;
            transition:3s;
        }
    </style>
</head>
<body>
    <div></div>
    <h1></h1>

</body>
</html>
```

05_outline

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>document</title>
    <style>
        div,h1{
            width:300px;
            height:50px;
            background:pink;
        }
        div{
            border:5px solid red;
        }
        h1{
            outline:5px solid green;

        }
        input:focus{
            /*取消表单控件焦点状态下默认轮廓线*/
            outline:none;
        }
        h2{
            width:300px;
            height:100px;
            background:orange;
            box-shadow:10px 10px 5px -5px gray;
        }
    </style>
</head>
<body>
    <div></div>
    <h1></h1>
    <input type="text">
    <h2></h2>
</body>
</html>
```

06_padding

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>document</title>
    <style>
        div{
            width:200px;
            height:200px;
            border:1px solid orange;
            /*padding:10px 20px 30px 40px;*/
            padding-top:10px;
            padding-left:20px;

        }
        h1{
            width:200px;
            height:200px;
            background:gray;
            padding:50px;
        }
        span{
             width:200px;
             height:200px;
             border:1px solid blue;
             /*行内元素对盒模型属性不完全支持,不能设置宽高,不支持上下
            内边距*/
             padding:0px 50px;
        }
    </style>
</head>
<body>
    <div>打雷了</div>
    <h1>下雨了</h1>
    <span>回家收衣服喽</span>
</body>
</html>
```

07_margin

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>document</title>
    <style>
        div{
            width:200px;
            height:200px;
            background:red;
        }
        #d1{

            background:green;
            /*margin:0 auto;*/
            border:1px solid blue;
            padding:50px;
            margin:50px;
        }
        b,span{
            background:green;
            margin:50px;
            /*行内元素不支持上下边距*/

        }
        /*行内元素不支持上下边距
        b{
            margin-right:-5px;
        }*/

    </style>
</head>
<body>
    <div id="d1"></div>
    <div></div>
    <b>打雷了</b>
    <span>下雨了</span>
</body>
</html>
```

margin_html

```ht
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
    <style>
        body{
            margin:0;
            /*border-top:1px solid blue;*/
            padding-top:0.1px;
        }
        div{
            width:200px;
            height:200px;
            background:red;
            margin-top:100px;
            margin-bottom:200px;
        }
        h1{
            width:200px;
            height:200px;
            background:green;
            margin-top:100px;
        }
        b,span{
            background:blue;
            /*行内元素不支持垂直边距,水平方向上外边距会
            叠加显示*/
            margin:10px 50px;
        }
        body,h1,h2,h3,h4,h5,h6,p,ul,ol{
            /*取消默认样式*/
            margin:0;
            padding:0;
            list-style:none;
        }
    </style>
</head>
<body>
    <!--第一个子元素的margin-top作用于父元素上
    解决:
        方式1.父元素添加顶部边框
        方式2.父元素添加padding-top:0.1px;
    -->
    <div></div>
    <!--同时设置垂直方向上的边距,取最大值-->
    <h1></h1>
    <b>加粗</b>
    <span>span文本</span>
    <h2></h2>
    <p></p>
    <ul></ul>
    <form action=""></form>



</body>
</html>
```

01_vertical_align

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>document</title>
    <style>
        input{
            height:50px;
        }
        img,input,span{
            vertical-align:bottom;
        }

        /*文本的底部对齐,baseline
        */
    </style>
</head>
<body>

    <span>行内元素</span>
    <input type="text">
    <input type="submit">
    <img src="123.jpg" alt="">
</body>
</html>
```



  	​		

