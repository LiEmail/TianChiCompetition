# TianChiCompete
Our responding code and resources for TianChi competition

#Update 2015/04/06
1. 基本框架的构建：
 特征工程部分 
     Generate_raw_train.py (从原始数据中按照分割点，得到分割点前的数据)
	 Generate_feature_train.py (从raw_train数据中提取特征，并构建基于特征向量的训练集合)
 算法框架部分
	 LRTest.py (利用LR回归，进行分类预测)
	 CalF1.py (F1函数的计算)
 调用模块的文件
     根据网上的建议，当前主要选用pandas & statemodel，暂不清楚是否方便修改相关算法的API。先试着跑通流程
	 pandas/statmodels 为相关库(依赖库较多，暂未上传)
	 docs-py2.7(python官方文档pdf)

2. 所需要处理的工作
 特征提取上:
   增加 商品相关特征： 销量（前3/7/15天） 、分类中商品的排名（可能需要折合成数值型）
        用户相关特征： 购买总量/总的购买天数
		用户-分类特征：用户对该分类进行访问/购买/加购物车的次数
 数据分布的问题：
   当然，在进一步利用单模型对特征进行多重训练之前，先要解决好数据的一些问题，保证不会使"知识"在测试集上无法有效应用
#Update 2015/04/05
初步准备利用LR,把 *特征工程的构建* 和 *算法模型的选取* 分开来，也方便将整体流程顺一下。
然后有机会在进一步深入学习和探究
