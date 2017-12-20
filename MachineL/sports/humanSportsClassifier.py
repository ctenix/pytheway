# _*_ coding:utf-8 _*_
# 导入模块
import numpy as np
import pandas as pd
from sklearn.preprocessing import Imputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
# 导入分类器，K近邻，决策树以及高斯朴素贝叶斯
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB


# 数据导入函数
def load_dataset(feature_paths, label_paths):
    """取特征文件列表和标签文件列表中的内容，归并后返回"""
    feature = np.ndarray(shape=(0, 41))
    label = np.ndarray(shape=(0, 1))

    for file in feature_paths:
        # 使用逗号分隔符读取特征数据，将问号替换标记为缺失值，文件中不包含表头
        df = pd.read_table(file, delimiter=',', na_values='?', header=None)
        imp = Imputer(missing_values="NaN", strategy="mean", axis=0)
        imp.fit(df)
        df = imp.transform(df)
        # 将新读入的数据合并到特征集合中
        feature = np.concatenate((feature, df))

    for file in label_paths:
        # 读取标签数据，文件中不包含表头
        df = pd.read_table(file, header=None)
        # 将新读入的数据合并到标签集合中
        label = np.concatenate((label, df))
        # 将标签归整为一维向量
    label = np.ravel(label)
    return feature, label


if __name__ == '__main__':
    # 设置数据路径
    feature_paths = ['A/A.feature', 'B/B.feature', 'A/A.feature', 'C/C.feature', 'D/D.feature', 'E/E.feature']
    label_paths = ['A/A.label', 'B/B.label', 'C/C.label', 'D/D.label', 'E/E.label']
    # 将前4个数据作为训练集读入
    x_train, y_train = load_dataset(feature_paths[:4], label_paths[:4])
    # 将最后1个数据作为测试集读入
    x_test, y_test = load_dataset(feature_paths[4:], label_paths[4:])
    # 使用全量数据作为训练集，借助train_test_split函数将训练数据打乱, 数据随机打乱，便于后续分类器的初始化和训练
    x_train, x_, y_train, y_ = train_test_split(x_train, y_train, test_size=0.0)
    # 创建K近邻分类器，并在测试集上进行预测
    print("Start training knn")
    knn = KNeighborsClassifier().fit(x_train, y_train)
    print("Training done!")
    answer_knn = knn.predict(x_test)
    print("Prediction done!")
    # 创建决策树分类器，并在测试集上进行预测
    print("Start training DT")
    dt = DecisionTreeClassifier().fit(x_train, y_train)
    print("Training done!")
    answer_dt = dt.predict(x_test)
    print("Prediction done!")
    # 创建贝叶斯分类器，并在测试集上进行预测
    print("Start training Bayes")
    gnb = GaussianNB().fit(x_train, y_train)
    answer_gnb = gnb.predict(x_test)
    print("Prediction done!")
    # 计算准确率与召回率
    print("\n\nThe classification report for knn:")
    print(classification_report(y_test, answer_knn))
    print("\n\nThe classification report for dt:")
    print(classification_report(y_test, answer_dt))
    print("\n\nThe classification report for gnb:")
    print(classification_report(y_test, answer_gnb))
