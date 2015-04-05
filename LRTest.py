import pandas as pd
import statsmodels.api as sm  #这就是要安装的两个库，import进来

train = pd.read_csv("sample.csv")    #sample的格式是target,view_num,buy_num即你标记好的训练集，记得第一行一定要是标题
train_cols = train.columns[1:]       #以第一列以后的列，即二三列作为训练特征，就是以view_num和buy_num为训练特征
logit = sm.Logit(train['target'], train[train_cols]) #表示以后两列作为训练特征，target列为标记值进行逻辑回归
result = logit.fit()              #要是开心的话可以用result.summary()看一下回归结果

combos = pd.read_csv("vectors.csv")   #vectors是未标记的特征向量，也就是我们要预测的，格式为uid,bid,view_num,buy_num
train_cols = combos.columns[2:]
combos['prediction'] = result.predict(combos[train_cols])  #为每组特征进行预测打分，存储在一个新的prediction列，这里是第五列

predicts = defaultdict(set)
for term in combos.values:
    uid, bid, prediction = str(int(term[0])), str(int(term[1])), term[4]
if prediction > POINT:      #可以通过调节POINT的大小来控制最后结果的个数，当然你也可以取分数topN
    predicts[uid].add(bid)