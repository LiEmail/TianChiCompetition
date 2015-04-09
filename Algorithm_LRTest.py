# -*- coding: utf-8 -*-
import pandas as pd
from collections import defaultdict
import statsmodels.api as sm
POINT = 0.0
train = pd.read_csv("E://天池_移动推荐//feature_train.csv")    #FeatureData的格式是target,feature1,feature2,... 即你标记好的训练集，第一行是标题
train_cols = train.columns[1:]       #第一列是分类label，后面的列就是训练特征

logit = sm.Logit(train['result'], train[train_cols]) #表示以后两列作为训练特征，target列为标记值进行逻辑回归
result = logit.fit()              #要是开心的话可以用result.summary()看一下回归结果

combos = pd.read_csv("E://天池_移动推荐//vectors.csv")   #vectors是未标记的特征向量，也就是我们要预测的，格式为uid,bid,view_num,buy_num
train_cols = combos.columns[2:]       #前两行是uid-bid，后面的才是特征向量
combos['prediction'] = result.predict(combos[train_cols])  #为每组特征进行预测打分，存储在一个新的prediction列，这里是第五列

import csv
writer = csv.writer(file('E://predict_result.csv','wb'))
writer.writerow(['user_id','iterm_id'])
for term in combos.values:
    uid, bid, prediction = str(int(term[0])), str(int(term[1])), term[6]
if prediction > 0.5:      #可以通过调节POINT的大小来控制最后结果的个数，当然你也可以取分数topN
    writer.writerow([uid,bid]) #结果输出到新的csv当中
