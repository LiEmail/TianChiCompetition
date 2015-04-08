import csv
import time
print time.time()

#数据模块
start_time = '2014-11-13 00'
cut_time = '2014-12-18 00'
test_time = '2014-12-19 00'
#input_user_file = 'E:\\天池_移动推荐\\tianchi_mobile_recommend_train_user.csv'
#input_item_file = 'E:\\天池_移动推荐\\tianchi_mobile_recommend_train_item.csv'
input_user_file = 'E:\\天池_移动推荐\\G2.csv'
input_item_file = 'E:\\天池_移动推荐\\G1.csv'
output_train_file = 'E:\\天池_移动推荐\\TrainSet.csv'
output_ref_file = 'E:\\天池_移动推荐\\RefSet.csv'
train_title  = ['target','feature1','feature2','feature3'] #trainSet的title row
Predict_title  = ['user_id','item_id','feature1','feature2','feature3'] #PredictSet的title row
days_feature = (3, 7, 15)  #前3, 7, 15天的数据
days_featureName = ("Sales_3","Sales_7","Sales_15")
behavior = ("","click","store","shopcar","buy") 	#用户行为的title
user_feature  = ("active_day","buy_sum","buy_day")  #用户特征的title
ratio = 10 # 百分比型的特征归一化的参数
#########################################################################################

start_time_stamp = TransferTime(start_time)
cut_time_stamp   = TransferTime(cut_time)
test_time_stamp  = TransferTime(test_time)
total_day = float(cut_time_stamp - start_time_stamp)

user_dic = {}  #用户商品词典
good_dic = {}  #商品统计词典  
user_item_dic = {}  #用户-品牌词典
use_item_result = Set() # 用户-商品购买情况(二类结果)
test_user_dic = {}

#时间戳转化成小时数
def TransferTime(Time) :
	Time_array = time.strptime(Time,"%Y-%m-%d %H")
	Time_stamp = int(time.mktime(Time_array))
	Time_stamp = int(Time_stamp/(3600*24))
	return Time_stamp
	
#形成 userid_itemid串，用于匹配target
def AppendString(user_id, item_id) :
    s = []
    s.append(user_id)
    s.append('-')
    s.append(item_id)
    item = ''.join(s)
    return item

def GenerateFeature(Title) :
	#商品信息的统计
	with open(input_item_file) as item_csv_file:
		item_reader = csv.DictReader(item_csv_file)
		for item_row in item_reader
			good_dic[row['item_id']] = {'category': row['item_category'],\
										'geohash': row['item_geohash'],\
										behavior[1]: 0,\
										behavior[2]: 0,\
										behavior[3]: 0,\
										behavior[4]: 0,\
										days_featureName[0]: 0,\
										days_featureName[1]: 0,\
										days_featureName[2]: 0\
										}
	#用户 && 用户-品牌 信息的统计
	with open(input_user_file) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			user_id = row['user_id']
			item_id = row['item_id']
			behavior_type = behavior[row['behavior_type']]
			b_time = TransferTime(row['time'])
			item_category = row['item_category']
			
			if b_time <= cut_time_stamp :  # 时间分割点之前的才记入trainSet
				
				#更新商品统计词典（只统计出现过的商品/未出现商品暂时过滤掉）
				if good_dic.has_key(item_id) == True :
					one_good = good_dic[item_id]
					# 更新行为
					one_good[behavior[behavior_type]] = one_good[behavior[behavior_type]] + 1
					# 更新火爆程度
					if b_time - cut_time_stamp >= days_feature[0] :
						one_good[days_featureName[0]] = one_good[days_featureName[0]] + 1
						one_good[days_featureName[1]] = one_good[days_featureName[1]] + 1
						one_good[days_featureName[2]] = one_good[days_featureName[2]] + 1
					else if b_time - cut_time_stamp >= days_feature[1] :
						one_good[days_featureName[1]] = one_good[days_featureName[1]] + 1
						one_good[days_featureName[2]] = one_good[days_featureName[2]] + 1
					else if b_time - cut_time_stamp >= days_feature[2] :
						one_good[days_featureName[2]] = one_good[days_featureName[2]] + 1
				
				#更新用户统计词典
				if user_dic.has_key(user_id) == False :  #如果不存在键值，先创建一个键值
					user_dic[user_id] = { behavior[1]: 0,\
										  behavior[2]: 0,\
										  behavior[3]: 0,\
										  behavior[4]: 0,\
  										  AppendString(behavior[1], 'days'): Set(),\
										  AppendString(behavior[2], 'days'): Set(),\
										  AppendString(behavior[3], 'days'): Set(),\
										  AppendString(behavior[4], 'days'): Set()
										}
				one_user = user_dic[user_id]
				one_user[behavior[behavior_type]] = one_good[behavior[behavior_type]] + 1  	#更新行为
				one_user[AppendString(behavior[behavior_type],'days')].add(b_time)			#更新活跃度		
				if behavior_type == 4 :
					use_item_result.add(AppendItems(user_id, item_id))
											  
				#更新用户-品牌特征 （等待添加）
				'''
				if one_user_one_good.has_key(behavior_type) == True:
					one_user_one_good_one_behavior = one_user_one_good[behavior_type]
					one_user_one_good_one_behavior = one_user_one_good_one_behavior + [b_time]
				else:
					one_user_one_good[behavior_type] = [b_time]
				else:
					one_user[item_id] = {behavior_type:[b_time]}
				
				if test_user_dic.has_key(user_id) == True:
					good = test_user_dic[user_id]
					if good.has_key(item_id) != True:
						good[item_id] = 1
				else:
					test_user_dic[user_id] = {item_id:1}
				'''
	csvfile.close()
	print "read ok"

	#特征提取
	writer = csv.writer(file(output_train_file,'wb'))
	writer.writerows(Title)
	for user in user_dic.keys() : 	#后期考虑剔除 爬虫类账户，暂时做全部用户的		
		for good in good_dic.keys() :
			target = 0
			if AppendString(user, good) in user_behavior :
				target = 1
			
			good_feature = good_dic[good]
			user_feature = user_dic[user]
			
			good_f1	= good_feature[behavior[4]]
			good_f2	= good_feature[behavior[3]]
			good_f3	= good_feature[days_featureName[0]]
			good_f4 = good_feature[days_featureName[1]]
			user_f1 = len(user_feature[AppendItems(behavior[4], 'days')]) * 1.0 * ratio / (cut_time - start_time)  
			user_f2 = user_feature[behavior[4]] * 1.0 * ratio /( user_feature[behavior[1]] + user_feature[behavior[2]] + user_feature[behavior[3]] + user_feature[behavior[4]] )
			
			if Title[0] == 'target' : 
				writer.writerows([target, good_f1, good_f2, good_f3, good_f4, \
							  user_f1, user_f2])
			else if Title[0] == 'user_id'
				writer.writerows([good, user, good_f1, good_f2, good_f3, good_f4, \
							  user_f1, user_f2])
	csvfile.close()
	print '提取完毕'
	return
	
if __name__ == '__main__' :
	GenerateFeature(train_title)
	#GenerateFeature(Predict_title)
