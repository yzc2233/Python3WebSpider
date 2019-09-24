import GetIP as ip
import requests
import pymysql
import json

env = 'qa2'
order_id = '1301190209498244'

Order_IP = ip.get_ip('order',env)

# print(Order_IP)

conn = pymysql.connect(host = '10.157.26.92',# 连接名称，默认127.0.0.1
user = 'marketing', # 用户名
passwd='123456' ,# 密码
port= 3306 ,# 端口 默认为3306
db='order' ,# 数据库名称
charset='utf8' # 字符编码
 )
getorder_sql = "select * from orders where order_id="+"'"+order_id+"';"
cur = conn.cursor()
cur.execute(getorder_sql)
data = cur.fetchall()
# print(data)
if not len(data):
    print('未找到订单',order_id);
    exit()

updateorder_sql = "update orders set create_time=DATE_SUB(a.create_time ,INTERVAL 1 HOUR) where order_id="+"'"+order_id+"';"
# print(updateorder_sql)
# try :
#     cur.execute(updateorder_sql)
#     conn.commit()
# except:
#     conn.rollback()
#     print('更新失败')
#     exit()
#

get_orderSync_url = Order_IP+'/v1/order/orderSync/orderSync/'+order_id
# print(get_orderSync_url)
req = requests.get(get_orderSync_url)
content = req.text
response = json.loads(content)
# print(response)

if not response['results'] is True:
    print('推送订单至OMS并索引至elasticSearch失败',response['results'])
    exit()







