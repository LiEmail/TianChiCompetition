# -*- coding: cp936 -*-
import csv
import time

#数据模块
start_time = '2014-11-13 00'
cut_time = '2014-12-18 00'
test_time = '2014-12-19 00'
dir = 'E:\\Github\\TianChiCompete\\'
input_user_file = dir + 'row_record_no1212.csv'
input_item_file = dir + 'tianchi_mobile_recommend_train_item.csv'
#input_user_file = dir + 'G2.csv'
#input_item_file = dir + 'G1.csv'
output_train_file = dir + 'TrainSet.csv'
output_vec_file = dir + 'PredictVector.csv'
days_feature = (3, 7, 15)  #前3, 7, 15天的数据
days_featureName = ("Sales_3","Sales_7","Sales_15")
behavior = ("","click","store","shopcar","buy")     #用户行为的title
user_feature_name  = ("active_ratio","buy_ratio","buy_day")  #用户特征的title
train_title  = ['target',behavior[4],behavior[3],days_featureName[0],user_feature_name[0],user_feature_name[1]] #trainSet的title row
predict_title  = ['user_id','item_id',behavior[4],behavior[3],days_featureName[0],user_feature_name[0],user_feature_name[1]] #PredictSet的title row

ratio = 30 # 百分比型的特征归一化的参数
#########################################################################################
#时间戳转化成天数
def date2days(date):
    test_time_array = time.strptime(date,'%Y-%m-%d %H')
    days_i = int((time.mktime(test_time_array))/(3600*24))
    days_f = float((time.mktime(test_time_array))/(3600*24))
    if(days_f - days_i) > 0.66 : 
        return days_i + 1
    else:
        return days_i

#形成 userid_itemid串，用于匹配target
def AppendUseItemString(user_id, item_id) :
    s = []
    s.append(user_id)
    s.append('-')
    s.append(item_id)
    item = ''.join(s)
    return item

#判断日期是否相等
def IsThatDay(target, source) :
    if target == source :
        return True
    return False
	
#清除一些明显不符合的样本
def clearNagetiveSample(user_good_item):
    if user_good_item[behavior[4]] == 0:
        if user_good_item[behavior[3]] == 0 and (user_good_item[behavior[1]] + user_good_item[behavior[2]]) < 4:
            return True
        if user_good_item[behavior[3]] > 8:
            return True
    return False
	
start_time_stamp = date2days(start_time)
cut_time_stamp   = date2days(cut_time)
test_time_stamp  = date2days(test_time)
user_dic = {}  #用户商品词典
good_dic = {}  #商品统计词典  
user_good = {}  #用户-品牌词典
use_item_result = {} # 用户-商品购买情况(二类结果)
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
    user_count = 0
    whole_count = 0
    with open(input_user_file) as csvfile :
        reader = csv.DictReader(csvfile)
        for row in reader:
            user_id = row['user_id']
            item_id = row['item_id']
            behavior_type = behavior[int(row['behavior_type'])]
            b_time = date2days(row['time'])
            item_category = row['item_category']
            user_count = user_count + 1
            if user_count %100000 == 0:
                print user_count
            if good_dic.has_key(item_id) == False:
                continue
            whole_count = whole_count + 1
            
	    #如果out_put_type  == 1（PredictVectors）,test_time之前的都要加入
            #如果out_put_type  == 0（trainSet）,cut_time之前的都要加入     
            if (out_put_type  == 1 and b_time < test_time_stamp) or \
               (out_put_type == 0 and b_time < cut_time_stamp ):
                #更新商品统计词典（只统计出现过的商品/未出现商品暂时过滤掉）
                if good_dic.has_key(item_id) == True :
                    one_good = good_dic[item_id]
                    # 更新行为
                    one_good[behavior_type] = one_good[behavior_type] + 1
                    # 更新火爆程度 时间差值可能有12小时的误差
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
			    
		#更新用户特征
                one_user = user_dic[user_id]
                one_user[behavior_type] = one_user[behavior_type] + 1   #更新行为
                one_user[AppendUseItemString(behavior_type,'days')].add(b_time) #更新活跃度
                      
                #更新用户-品牌特征 （等待添加）
                use_good_id = AppendUseItemString(user_id, item_id)
                if user_good.has_key(use_good_id) == False :   #如果不存在键值，先创建一个键值
                    user_good[use_good_id] = {    behavior[1]: 0,\
                                                  behavior[2]: 0,\
                                                  behavior[3]: 0,\
                                                  behavior[4]: 0
                                                 }
                user_good[use_good_id][behavior_type] = user_good[use_good_id][behavior_type] + 1
                
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
            #加入分割点时间的tag
            #如果out_put_type  == 0 （trainSet）,利用cut_time当天的结果标记之前的TrainSet的tag
            elif out_put_type == 0 and IsThatDay(b_time, cut_time_stamp):
                    result = False
                    if behavior_type == 'buy' :
                        print 'buy'
                    result = True
                    use_item_result[AppendUseItemString(user_id, item_id)] = { 'tag' : result}
    csvfile.close()
    print "read ok"
    print 'whole : ' + str(whole_count)
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

    if out_put_type == 0 :
        user_good_list = use_item_result
    elif out_put_type == 1 :
        user_good_list = user_good

    for user_good_key in user_good_list :
        array = user_good_key.split('-')
        user = array[0]
        good = array[1]
        if (user_dic.has_key(user) is True) and (good_dic.has_key(good) is True) :
            # 没发生过行为的 && 超过一些 负样本边界条件的 都剔除掉
            if( (not user_good.has_key(user_good_key)) or clearNagetiveSample(user_good[user_good_key])) :
                continue;

            good_feature = good_dic[good]
            user_feature = user_dic[user]					
            good_f1 = good_feature[behavior[4]]
            good_f2 = good_feature[behavior[3]]
            good_f3 = good_feature[days_featureName[0]]
            good_f3 = good_f3 * 1.0 * 10 / 500 #归一化处理
            #good_f4 = good_feature[days_featureName[1]]  #前7天结果和前3天一样，统计上可能是集合划分的问题，暂时先不用
            user_f1 = len(user_feature[AppendUseItemString(behavior[4], 'days')]) * 1.0 * ratio / (cut_time_stamp - start_time_stamp)
            user_f2 = user_feature[behavior[4]] * 1.0 * ratio / ( user_feature[behavior[1]] + user_feature[behavior[2]] + user_feature[behavior[3]] + user_feature[behavior[4]] )
							
            #判断 一些刷单用户，取消噪点
            if user_f1 < 0.00001 and user_f2 < 0.01 :
                continue
					
            #未考虑正负样本抽样，正负样本比例先按照 1：3 来取
            if out_put_type == 0 :
                if (use_item_result[user_good_key]['tag'] is False) and (count == 3) :
                    writer.writerow([0, good_f1, good_f2, good_f3, good_f4, user_f1, user_f2])
                    count = 0
                elif (use_item_result[user_good_key]['tag'] is False) and (count < 3) :
                    count = count + 1
                elif use_item_result[user_good_key]['tag'] is True :
                    writer.writerow([1, good_f1, good_f2, good_f3, user_f1, user_f2])
            elif out_put_type == 1 :
                writer.writerow([user, good, good_f1, good_f2, good_f3, user_f1, user_f2])
    csvfile.close()
    print 'generate over'
    return
    
if __name__ == '__main__' :
    #GenerateFeature(0)
    GenerateFeature(0)
