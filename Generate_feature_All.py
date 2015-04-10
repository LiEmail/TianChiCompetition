# -*- coding: cp936 -*-
import csv
import time

#数据模块
start_time = '2014-11-13 00'
cut_time = '2014-12-18 00'
test_time = '2014-12-19 00'
dir = 'E:\\Github\\TianChiCompete\\'
#input_user_file = dir + 'tianchi_mobile_recommend_train_user.csv'
#input_item_file = dir + 'tianchi_mobile_recommend_train_item.csv'
input_user_file = dir + 'G2.csv'
input_item_file = dir + 'G1.csv'
output_train_file = dir + 'TrainSet.csv'
output_vec_file = dir + 'PredictVector1212.csv'
days_feature = (3, 7, 15)  #前3, 7, 15天的数据
days_featureName = ("Sales_3","Sales_7","Sales_15")
behavior = ("","click","store","shopcar","buy") 	#用户行为的title
user_feature_name  = ("active_ratio","buy_ratio","buy_day")  #用户特征的title
train_title  = ['target',behavior[4],behavior[3],days_featureName[0],days_featureName[1],user_feature_name[0],user_feature_name[1]] #trainSet的title row
predict_title  = ['user_id','item_id',behavior[4],behavior[3],days_featureName[0],days_featureName[1],user_feature_name[0],user_feature_name[1]] #PredictSet的title row

ratio = 10 # 百分比型的特征归一化的参数
#########################################################################################
#时间戳转化成天数
def date2days(date):
    date_array = time.strptime(date,'%Y-%m-%d %H')
    days = int((time.mktime(date_array))/(3600*24))
    return days

#形成 userid_itemid串，用于匹配target
def AppendUseItemString(user_id, item_id) :
    s = []
    s.append(user_id)
    s.append('-')
    s.append(item_id)
    item = ''.join(s)
    return item

def IsThatDay(target, source) :
    if target == source :
        return True
    return False
	
start_time_stamp = date2days(start_time)
cut_time_stamp   = date2days(cut_time)
test_time_stamp  = date2days(test_time)
user_dic = {}  #用户商品词典
good_dic = {}  #商品统计词典  
user_good = {}  #用户-品牌词典
use_item_result = set() # 用户-商品购买情况(二类结果)
test_user_dic = {}

#生成需要的带特征向量的文件
# out_put_type取值 
#0-trainSet;
#1-PredictVector
#2-refenceSet(有待扩展) 
def GenerateFeature(out_put_type) :
        #商品信息的统计
	with open(input_item_file) as item_csv_file:
		item_reader = csv.DictReader(item_csv_file)
		for row in item_reader :
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
			behavior_type = behavior[int(row['behavior_type'])]
			b_time = date2days(row['time'])
			item_category = row['item_category']
			
			#如果out_put_type  == 1（PredictVectors）,test_time之前的都要加入
            #如果out_put_type  == 0（trainSet）,cut_time之前的都要加入		
			if (out_put_type  == 1 and b_time < test_time_stamp) or \
			   (out_put_type == 0 and b_time < cut_time_stamp ):
				#更新商品统计词典（只统计出现过的商品/未出现商品暂时过滤掉）
				if good_dic.has_key(item_id) == True :
					one_good = good_dic[item_id]
					# 更新行为
					one_good[behavior_type] = one_good[behavior_type] + 1
					# 更新火爆程度
					if b_time - cut_time_stamp <= days_feature[0] :
						one_good[days_featureName[0]] = one_good[days_featureName[0]] + 1
						one_good[days_featureName[1]] = one_good[days_featureName[1]] + 1
						one_good[days_featureName[2]] = one_good[days_featureName[2]] + 1
					elif b_time - cut_time_stamp <= days_feature[1] :
						one_good[days_featureName[1]] = one_good[days_featureName[1]] + 1
						one_good[days_featureName[2]] = one_good[days_featureName[2]] + 1
					elif b_time - cut_time_stamp <= days_feature[2] :
						one_good[days_featureName[2]] = one_good[days_featureName[2]] + 1
				
				#更新用户统计词典
				if user_dic.has_key(user_id) == False :  #如果不存在键值，先创建一个键值
					user_dic[user_id] = { behavior[1]: 0,\
										  behavior[2]: 0,\
										  behavior[3]: 0,\
										  behavior[4]: 0,\
  										  AppendUseItemString(behavior[1], 'days'): set(),\
										  AppendUseItemString(behavior[2], 'days'): set(),\
										  AppendUseItemString(behavior[3], 'days'): set(),\
										  AppendUseItemString(behavior[4], 'days'): set()
										}
				one_user = user_dic[user_id]
				one_user[behavior_type] = one_user[behavior_type] + 1  	#更新行为
				one_user[AppendUseItemString(behavior_type,'days')].add(b_time)	#更新活跃度
					  
				#更新用户-品牌特征 （等待添加）
				
				#加入分割点时间的购买结果，来对
				use_good_id = AppendUseItemString(user_id, item_id)
				if user_good.has_key(use_good_id) == False :   #如果不存在键值，先创建一个键值
					user_good[use_good_id] = {behavior[1]: 0,\
												  behavior[2]: 0,\
												  behavior[3]: 0,\
												  behavior[4]: 0
												 }
				user_good_info = user_good[use_good_id]
				one_user[behavior_type] = one_user[behavior_type] + 1  	#更新行为
				
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
			#如果out_put_type  == 0 （trainSet）,利用cut_time当天的结果标记之前的TrainSet的tag
			elif (out_put_type == 0 and b_time == cut_time_stamp ) : 
				if behavior_type == "buy" and IsThatDay(b_time, cut_time_stamp) : 
					use_item_result.add(AppendUseItemString(user_id, item_id))
						
	csvfile.close()
	print "read ok"

	##############特征提取##################################################
	
	#确定标题	
	
	if out_put_type == 0 :
	    Title = train_title
	    output_file = output_train_file
	elif out_put_type == 1 :
	    Title = predict_title
	    output_file = output_vec_file
	
	writer = csv.writer(file(output_file,'wb'))
	writer.writerow(Title)

	count = 0;
	for user in user_dic.keys() : 	#后期考虑剔除 爬虫类账户，暂时做全部用户的		
		for good in good_dic.keys() :
			if(user_good.has_key(AppendUseItemString(user, good))) :
				target = 0
				if AppendUseItemString(user, good) in use_item_result :
					target = 1
				
				good_feature = good_dic[good]
				user_feature = user_dic[user]
				
				good_f1	= good_feature[behavior[4]]
				good_f2	= good_feature[behavior[3]]
				good_f3	= good_feature[days_featureName[0]]
				good_f4 = good_feature[days_featureName[1]]
				user_f1 = len(user_feature[AppendUseItemString(behavior[4], 'days')]) * 1.0 * ratio / (cut_time_stamp - start_time_stamp)
				user_f2 = user_feature[behavior[4]] * 1.0 * ratio /( user_feature[behavior[1]] + user_feature[behavior[2]] + user_feature[behavior[3]] + user_feature[behavior[4]] )
				
				#判断 一些刷单用户，取消噪点
				if user_f1 < 0.00001 and user_f2 < 0.01 : 
					continue

				#未考虑正负样本抽样，正负样本比例先按照 1：7 来取
				if out_put_type == 0 :
					if target == 0 and count == 7 :
						writer.writerow([target, good_f1, good_f2, good_f3, good_f4, user_f1, user_f2])
						count = 0
					elif target == 0 and count < 7 : 
						count = count + 1
					elif target == 1 : 
						writer.writerow([target, good_f1, good_f2, good_f3, good_f4, user_f1, user_f2])
				elif out_put_type == 1 :
					writer.writerow([user, good, good_f1, good_f2, good_f3, good_f4, user_f1, user_f2])
	csvfile.close()
	print 'generate over'
	return
	
if __name__ == '__main__' :
	#GenerateFeature(0)
	GenerateFeature(0)
