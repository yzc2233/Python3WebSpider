import time
import GetIP as ip
import requests
import pymysql
import json

env = 'qa2'
order_id = '1301190209498244'

Order_IP = ip.get_ip('order',env)
OMS_IP = ip.get_ip('OMS',env)

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
# req = requests.get(get_orderSync_url)
# content = req.text
# response = json.loads(content)
# # print(response)
#
# if not response['results'] is True:
#     print('推送订单至OMS并索引至elasticSearch失败',response['results'])
#     exit()


oms_conn = pymysql.connect(host = '10.157.26.92',# 连接名称，默认127.0.0.1
                       user = 'marketing', # 用户名
                       passwd='123456' ,# 密码
                       port= 3306 ,# 端口 默认为3306
                       db='oms' ,# 数据库名称
                       charset='utf8' # 字符编码
                       )

getomssalesorder_sql = "select a.ORDER_INTERNAL_STATUS,a.TYPE,a.SALES_ORDER_SYS_ID from sales_order a where a.SALES_ORDER_NUMBER="+"'"+order_id+"';"
omscur = oms_conn.cursor()
omscur.execute(getomssalesorder_sql)
salesorder_data = omscur.fetchall()
ORDER_INTERNAL_STATUS = salesorder_data[0][0]
orderSysId = salesorder_data[0][2]

while ORDER_INTERNAL_STATUS=='PENDING':
    execJob_url = OMS_IP+'/job/exec/orders?th=omsPendingOrdersJob'
    req = requests.get(get_orderSync_url)
    content = req.text
    response = json.loads(content)
    if not response['results'] is True:
        print('执行出来PENDING状态Job失败',response['results'])
        exit()
    time.sleep(3)
    omscur.execute(getomssalesorder_sql)
    salesorder_data = omscur.fetchall()
    ORDER_INTERNAL_STATUS = salesorder_data[0][0]

if ORDER_INTERNAL_STATUS=='EXCEPTION':
    except_url = OMS_IP+'/v1/oms/order/exception/status/close?orderSysId='+orderSysId+'&comment=undefined&orderFrom=SO'
    req = requests.post(except_url)
    content = req.text
    response = json.loads(content)
    if not response['results'] is True:
        print('处理EXCEPTION状态失败',response['results'])
        exit()
    time.sleep(10)
    omscur.execute(getomssalesorder_sql)
    salesorder_data = omscur.fetchall()
    ORDER_INTERNAL_STATUS = salesorder_data[0][0]

if ORDER_INTERNAL_STATUS=='WAIT_SEND_SAP':
    time.sleep(10)
    omscur.execute(getomssalesorder_sql)
    salesorder_data = omscur.fetchall()
    ORDER_INTERNAL_STATUS = salesorder_data[0][0]

if ORDER_INTERNAL_STATUS=='WAIT_SAPPROCESS':
    print('订单状态WAIT_SAPPROCESS')

getomspurchaseOrder_sql = "select a.PURCHASE_ORDER_NUMBER,a.SIGN_TIME,a.ORDER_INTERNAL_STATUS  from purchase_order a where a.SALES_ORDER_NUMBER="+"'"+order_id+"';"
omscur.execute(getomspurchaseOrder_sql)
purchaseOrder_data = omscur.fetchall()


if len(purchaseOrder_data) == 1:
    updatepurchase_sql = "update purchase_order set ORDER_INTERNAL_STATUS ='SIGNED',SIGN_TIME='2019-09-20 09:47:39' where PURCHASE_ORDER_NUMBER="+"'"+purchaseOrder_data[0][0]+"';"
    omscur.execute(updatepurchase_sql)
    updatesalesorder_sql = "update sales_order set ORDER_INTERNAL_STATUS='SIGNED' where  SALES_ORDER_NUMBER="+"'"+order_id+"';"
    cur.execute(updatesalesorder_sql)
elif len(purchaseOrder_data) > 1:
    print('订单被拆单')
    length = len(purchaseOrder_data)
    for i in range (0,length):
        if i == 0 :
            updatepurchase_sql2 = "update purchase_order set ORDER_INTERNAL_STATUS ='SIGNED/SIGNED',SIGN_TIME='2019-09-20 09:47:39' where PURCHASE_ORDER_NUMBER="+"'"+purchaseOrder_data[0][0]+"';"
            omscur.execute(updatepurchase_sql2)
        elif i > 0:
            updatepurchase_sql3 = "update purchase_order set ORDER_INTERNAL_STATUS ='SIGNED',SIGN_TIME='2019-09-20 09:47:39' where PURCHASE_ORDER_NUMBER="+"'"+purchaseOrder_data[i][0]+"';"
            omscur.execute(updatepurchase_sql3)
    updatesalesorder_sql2 = "update sales_order set ORDER_INTERNAL_STATUS='SIGNED/SIGNED' where  SALES_ORDER_NUMBER="+"'"+order_id+"';"
    cur.execute(updatesalesorder_sql2)

cur.close()
omscur.close()


modifyorderstatus_url = Order_IP+"/v1/order/orderSync/orderStatusSync"
modifyorderstatus_data = {"head":{"token":"string","userId":"string"},"queryBody":[{"orderNo":order_id,"orderStatus":"DELIVERED","orderType":"NORMAL"}]}
headers = {'Content-Type':'application/json'}
req = requests.post(modifyorderstatus_url,modifyorderstatus_data,headers=headers)
content = req.text
response = json.loads(content)
if not response['results'] is True:
    print('修改订单状态失败',response['results'])
    exit()










