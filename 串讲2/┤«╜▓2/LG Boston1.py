from sklearn.datasets import load_boston
from sklearn.preprocessing import scale
from sklearn.model_selection import train_test_split
X, y = load_boston(True)
X = scale(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
#数据标归一化处理
from sklearn import preprocessing
#分别初始化对特征和目标值的标准化器
min_max_scaler = preprocessing.MinMaxScaler()
#分别对训练和测试数据的特征以及目标值进行标准化处理
X_train=min_max_scaler.fit_transform(X_train)
X_test=min_max_scaler.fit_transform(X_test)
y_train=min_max_scaler.fit_transform(y_train.reshape(-1,1))#reshape(-1,1)指将它转化为1列，行自动确定
y_test=min_max_scaler.fit_transform(y_test.reshape(-1,1))#reshape(-1,1)指将它转化为1列，行自动确定

#使用线性回归模型LinearRegression对波士顿房价数据进行训练及预测
from sklearn.linear_model import LinearRegression
lr=LinearRegression()
#使用训练数据进行参数估计
lr.fit(X_train,y_train)
#回归预测
lr_y_predict=lr.predict(X_test)
from sklearn.metrics import r2_score
score = r2_score(y_test, lr_y_predict)
print(score)