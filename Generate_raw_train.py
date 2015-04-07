import csv
import time
import re
import sys

#处理时间的字符串为 小时
def TransferTime(TimeString) :
        if(re.match(r"time",TimeString)) :
                return -1;
        test_time_array = time.strptime(TimeString,"%Y-%m-%d %H")
        test_time_stamp = int(time.mktime(test_time_array))
        return int(test_time_stamp/3600)

def GenerateTrainTest() :
	#分割点
        cut_time   = '2014-12-11 23'
        input_file = 'tianchi_mobile_recommend_train_user.csv'
        #input_file = '1.csv'

	#定义写文件的位置
        writer = csv.writer(file('cut_time_user.csv','wb'))

        reader = csv.reader(open(input_file))
        for user_id, item_id, behaviro_type, user_geohash, item_category, time in reader:
                if TransferTime(time) <= TransferTime(cut_time) :
                        writer.writerow([user_id, item_id, behaviro_type, user_geohash, item_category, time])
                #else :
                #        print "big than that"
        return 1;

if __name__ == '__main__' :
        GenerateTrainTest()
        print "generate ok"
