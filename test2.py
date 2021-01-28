null = None
false = False
true = True



#
# orderDetail_old = {
#     "timeStamp": 1592287559737,
#     "status": 0,
#     "results": {
#         "pageSize": 50,
#         "pageNo": 2,
#         "totalCount": 123,
#         "orderInfoList": []
#     },
#     "errorCode": null,
#     "errorMessage": null
# }
#
# orderDetail_old = orderDetail_old["results"]['orderInfoList']
#
# orderDetail_new = {
#     "timeStamp": 1592287564084,
#     "status": 0,
#     "results": {
#         "pageSize": 50,
#         "pageNo": 2,
#         "totalCount": 123,
#         "orderInfoList":  []
#     },
#     "errorCode": null,
#     "errorMessage": null
# }
#
# orderDetail_new = orderDetail_new["results"]['orderInfoList']
#
#
#
#
# for item in orderDetail_old :
#     for key in item:
#         if item[key] != orderDetail_new[orderDetail_old.index(item)][key]:
#             print("订单号：%s 字段：%s 老接口返回值：%s ，新接口返回值：%s" %(item["orderId"],key,item[key],orderDetail_new[orderDetail_old.index(item)][key]))
#



#新增发票抬头
import requests,json,threading,time
# count = 0
# alock = threading.Lock()
# def dealthread():
#     alock.acquire()
#     uid = uidlist.pop()
#     print('{} {}'.format(threading.current_thread(),uid))
#     alock.release()
#
# with open(r'F:\丝芙兰\压测\单服务压测2020-2021\Myaccount\对比压测\user_stage.csv') as f:
#     userids = f.readlines()
#     uidlist = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16']
#     threadcount = 2
#     length = len(uidlist)
#     for i in range(length):
#
#         th = threading.Thread(target=dealthread,args=())
#         th.start()
        # th.join()


        # print(str(uid).strip())
        # try:

            # timestamp = str(int(time.time()*1000))
            # uid = uid.split(',')[0]
            # count += 1
            # print(count)
            # print(cardNo)
            # url = 'http://10.157.26.170:10022/v1/portal/invoicetitle'
            # header = {'Content-Type':'application/json','uid':uid,'channel':'APP'}
            # body = {
            #     "type": 1,
            #     "name": "压测发票抬头-" + uid,
            #     "taxNo": uid + timestamp,
            #     "bankName": "银行名称",
            #     "bankAccount": "BA"+uid + timestamp,
            #     "address": "上海市静安区南京西路街道{uid}号101室".format(uid=uid),
            #     "tel": "021-12345678",
            #     "isDefault": 1
            # }
            # Response = requests.post(url=url,json=body,headers=header)
            # Response = json.loads(Response.text)
            # # print(Response)
            # if not Response['results']:
            #     # print(uid,'成功')
            #     #     pass
            #     # else:
            #     print(uid,'失败',Response)
        # except :
        #     continue




import threadpool
import time

def sayhello (a):
    print("hello: "+a)
    time.sleep(2)
#
# def main():
#     global result
#     seed=["a","b","c",'d','e','f','g']
#     start=time.time()
#     task_pool=threadpool.ThreadPool(5)
#     requests=threadpool.makeRequests(sayhello,seed)
#     for req in requests:
#         task_pool.putRequest(req)
#     task_pool.wait()
#     # end=time.time()
#     # time_m = end-start
#     # print("time: "+str(time_m))
#     # start1=time.time()
#     # for each in seed:
#     #     sayhello(each)
#     # end1=time.time()
#     # print("time1: "+str(end1-start1))
#
# if __name__ == '__main__':
#     main()
#
#
#
#

import datetime

# utc_now = datetime.datetime.utcnow()
# print(utc_now.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None))

# utc_time = '2021-01-14T08:38:09'
# utc_time = datetime.datetime.strptime(utc_time,'%Y-%m-%dT%H:%M:%S')
# print(utc_time)
# print(utc_time.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None))

# time.strftime("%Y/%m/%d %H:%M:%S")

results = {
    "已使用": {
        "count": 1,
        "list": [
            {
                "imageUrl": "https://sslstage1.sephorastatic.cn/soa/nmobile/img/normalCoupon/express_normal.png",
                "name": "全场买一件免运费",
                "timeLimit": "限2020.11.27至2021.11.27使用",
                "rule": "全场买一件免运费"
            }
        ]
    },
    "已过期": {
        "count": 2,
        "list": [
            {
                "imageUrl": "https://sslstage1.sephorastatic.cn/soa/nmobile/img/normalCoupon/off_normal.png",
                "name": "粉白黑金在O2O端offer Code测试",
                "timeLimit": "限2020.01.07至2021.01.17使用",
                "rule": "粉白黑金在O2O端offer Code测试11"
            },
            {
                "imageUrl": "https://sslstage1.sephorastatic.cn/soa/nmobile/img/normalCoupon/gift_normal.png",
                "name": "crm多个赠券促销",
                "timeLimit": "限2020.11.28至2020.11.28使用",
                "rule": "crm多个赠券促销"
            }
        ]
    },
    "未使用": {
        "count": 64,
        "list": [
            {
                "imageUrl": "https://sslstage1.sephorastatic.cn/soa/nmobile/img/normalCoupon/off_normal.png",
                "name": "补100元生日网站电子抵用券",
                "timeLimit": "限2020.11.20至2021.11.27使用",
                "rule": "网站专用100元生日礼券"
            }
        ]
    }
}

bb = results['已使用']
print(bb)
print(results.get('已使用'))