# -*- coding: cp936 -*-
import csv
import time
import re

cut_time   = '2014-12-05 23'
remove_time = '2014-12-12 23'

dir = 'D://TianChi//'
input_user_file = dir + 'tianchi_mobile_recommend_train_user.csv'
input_item_file = dir + 'tianchi_mobile_recommend_train_item.csv'
#input_user_file = dir + 'G2.csv'
#input_item_file = dir + 'G1.csv'
raw_train_file = dir + 'row_record.csv'
raw_buy_file = dir + 'buy_record.csv'
good_dic = {} # 商品词典

#处理时间的字符串为 小时
def TransferTime(TimeString) :
        if(re.match(r"time",TimeString)) :
                return -1;
        test_time_array = time.strptime(TimeString,"%Y-%m-%d %H")
        test_time_stamp = int(time.mktime(test_time_array))
        #0点的时候需要转换，不然会出错误
        days = int(test_time_stamp/(3600*24))
        if test_time_array[3] == 0 :
            return days + 1
        else :
            return days

def GenerateTrainTest() :
	#商品子集的统计
	with open(input_item_file) as item_csv_file :
		item_reader = csv.DictReader(item_csv_file)
		for row in item_reader :
			good_dic[row['item_id']] = {'category': row['item_category'],'geohash': row['item_geohash']}
	
	#提取有商品子集交互
	writer = csv.writer(file(raw_train_file,'wb'))
	writer.writerow(['user_id','item_id','behaviro_type','user_geohash','item_geohash','item_category','time'])
	reader = csv.reader(open(input_user_file))
	for user_id, item_id, behaviro_type, user_geohash, item_category, time in reader:
	if good_dic.has_key(item_id) and (TransferTime(time) != TransferTime(remove_time)) :  #如果要提取某一天的，就加上时间判断
			writer.writerow([user_id, item_id, behaviro_type, user_geohash, good_dic[item_id]['geohash'], item_category, time]) 

	return 1;

#提取某一天的购买记录（以dic的方式返回）
def GetOneDayBuyData(ref_time) :
	#商品子集的统计
	with open(input_item_file) as item_csv_file :
		item_reader = csv.DictReader(item_csv_file)
		for row in item_reader :
			good_dic[row['item_id']] = {'category': row['item_category'],'geohash': row['item_geohash']}

	#提取有商品子集交互
	writer = csv.writer(file(raw_train_file,'wb'))
	writer.writerow(['user_id','item_id','behaviro_type','user_geohash','item_geohash','item_category','time'])
	reader = csv.reader(open(input_user_file))
	for user_id, item_id, behaviro_type, user_geohash, item_category, time in reader:
	if good_dic.has_key(item_id) and (TransferTime(time) != TransferTime(remove_time)) :  #如果要提取某一天的，就加上时间判断
			writer.writerow([user_id, item_id, behaviro_type, user_geohash, good_dic[item_id]['geohash'], item_category, time]) 

	return 1;

if __name__ == '__main__' :
        GenerateTrainTest()
        print "row record generate ok"
