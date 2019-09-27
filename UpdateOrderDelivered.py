#coding=utf-8
import time
import CreateNewOrder
import sys
import json
import configparser
import pymysql
import GetIP
import requests

config = configparser.ConfigParser()
config.read('properties.conf')

allowedenv = config.get('allowedenv','allowedenv')
allowedenv = allowedenv.split(',')

env = sys.argv[1]
# env = 'qa2'

uid = sys.argv[2]
# uid = '2001844981'

OMS_IP = GetIP.getIp(env,'oms')
Order_IP = GetIP.getIp(env,'order')

mysqlhost = config['mysql_'+ env]['host']
mysqluser = config['mysql_'+ env]['user']
mysqlpassword = config['mysql_'+ env]['password']

inputargvlength = len(sys.argv)
if inputargvlength == 3:
    orderId = CreateNewOrder.CreateNewOrder()
elif inputargvlength == 4:
    orderId = sys.argv[3]

orderId = str(orderId)
# orderId = '1149816951901267'

def get_SalesOrderStatus():
    print('-'*20,'开始获取sales_order中订单状态','-'*20)
    conn = pymysql.connect(mysqlhost,mysqluser,mysqlpassword,'oms')
    cur = conn.cursor()
    sql = "select a.ORDER_INTERNAL_STATUS,a.TYPE,a.SALES_ORDER_SYS_ID from sales_order a where a.SALES_ORDER_NUMBER="+ "'" + orderId + "';"
    print(sql)
    try:
        cur.execute(sql)
        data = cur.fetchone()
        ORDER_INTERNAL_STATUS = data[0]
        SALES_ORDER_SYS_ID = data[2]
        print('成功获取sales_order中订单状态 %s,orderSysId= %s' %(ORDER_INTERNAL_STATUS,SALES_ORDER_SYS_ID))
        return ORDER_INTERNAL_STATUS,SALES_ORDER_SYS_ID
    except:
        print('获取sales_order中订单状态失败')
        cur.close()
        exit()
    finally:
        cur.close()
        print('-'*20,'获取sales_order中订单状态结束','-'*20 ,'\n\n')

def dealPending():
    print('-'*20,'开始处理Pending状态订单','-'*20)
    url = OMS_IP + '/job/exec/orders?th=omsPendingOrdersJob'
    req = requests.get(url)
    response = json.loads(req.text)
    if response['errorCode'] is not None or response['results'] is not True:
        print('处理Pending状态订单失败:',response)
        exit()
    else:
        for step in range(0,45,3):
            print('等待3s')
            time.sleep(3)
        print('处理Pending状态订单成功')
    print('-'*20,'处理Pending状态订单结束','-'*20 ,'\n\n')

def dealException(orderSysId):
    print('-'*20,'开始处理Exception状态订单','-'*20)
    url = OMS_IP+'/v1/oms/order/exception/status/close?orderSysId='+str(orderSysId)+'&comment=undefined&orderFrom=SO'
    req = requests.post(url)
    response = json.loads(req.text)
    if response['errorCode'] is not None or response['results'] is not True:
        print('处理Exception状态订单失败:',response)
        exit()
    else:
        for step in range(0,24,3):
            print('等待3s')
            time.sleep(3)
        print('处理Exception状态订单成功')

    print('-'*20,'处理Exception状态订单结束','-'*20 ,'\n\n')

def dealWaitSend(sec):
    print('-'*20,'开始处理WAIT_SEND_SAP状态订单','-'*20)
    for step in range(0,sec,3):
        print('等待3s')
        time.sleep(3)
    print('-'*20,'处理Exception状态订单结束','-'*20 ,'\n\n')

def getPurchaseOrder():
    print('-'*20,'开始获取purchase_order对应订单记录','-'*20)
    conn = pymysql.connect(mysqlhost,mysqluser,mysqlpassword,'oms')
    cur = conn.cursor()
    sql = "select a.PURCHASE_ORDER_NUMBER,a.SIGN_TIME,a.ORDER_INTERNAL_STATUS  from purchase_order a where a.SALES_ORDER_NUMBER=" + "'" + orderId + "';"
    print(sql)
    try:
        cur.execute(sql)
        data = cur.fetchall()
        print('成功获取purchase_order对应订单记录\n\n %s' %data)
        return data
    except:
        print('获取purchase_order对应订单记录失败')
        cur.close()
        exit()
    finally:
        cur.close()
        print('-'*20,'获取purchase_order对应订单记录结束','-'*20 ,'\n\n')


def IsSplit(data):
    data = list(data)
    IsSplit = False
    if len(data) > 1:
        IsSplit = True
    return IsSplit

def updateOrder_NotSpilt(data):
    print('-'*20,'开始非拆单情况下更新订单数据','-'*20)
    conn = pymysql.connect(mysqlhost,mysqluser,mysqlpassword,'oms')
    cur = conn.cursor()
    sql = "update purchase_order set ORDER_INTERNAL_STATUS ='SIGNED',SIGN_TIME='2019-09-20 09:47:39' where PURCHASE_ORDER_NUMBER="+"'"+data[0][0]+"';"
    sql2  = "update sales_order set ORDER_INTERNAL_STATUS='SIGNED' where  SALES_ORDER_NUMBER="+"'"+orderId+"';"
    try:
        cur.execute(sql)
        print(sql)
        cur.execute(sql2)
        print(sql2)
        conn.commit()
        print('非拆单情况下更新订单数据成功')
    except:
        conn.rollback()
        print('非拆单情况下更新订单数据失败')
        cur.close()
        exit()
    finally:
        cur.close()
        print('-'*20,'非拆单情况下更新订单数据结束','-'*20 ,'\n\n')

def updateOrder_IsSpilt(data):
    print('-'*20,'开始拆单情况下更新订单数据','-'*20)
    length = len(data)
    conn = pymysql.connect(mysqlhost,mysqluser,mysqlpassword,'oms')
    cur = conn.cursor()
    sql = "update purchase_order set ORDER_INTERNAL_STATUS ='SIGNED/SIGNED',SIGN_TIME='2019-09-20 09:47:39' where PURCHASE_ORDER_NUMBER="+"'"+data[0][0]+"';"
    sql2  = "update sales_order set ORDER_INTERNAL_STATUS='SIGNED/SIGNED' where  SALES_ORDER_NUMBER="+"'"+orderId+"';"
    try:
        for i in range(1,length):
            sql3 = updatepurchase_sql3 = "update purchase_order set ORDER_INTERNAL_STATUS ='SIGNED',SIGN_TIME='2019-09-20 09:47:39' where PURCHASE_ORDER_NUMBER="+"'"+data[i][0]+"';"
            cur.execute(sql3)
            print(sql3)
        cur.execute(sql)
        print(sql)
        cur.execute(sql2)
        print(sql2)
        conn.commit()
        print('拆单情况下更新订单数据成功')
    except:
        conn.rollback()
        print('拆单情况下更新订单数据失败')
        cur.close()
        exit()
    finally:
        cur.close()
        print('-'*20,'拆单情况下更新订单数据结束','-'*20 ,'\n\n')

def orderStatusSync():
    print('-'*20,'开始修改订单状态','-'*20)
    headers = {"Content-Type":"application/json","uid":uid}
    param = {"head":{"token":"string","userId":"string"},"queryBody":[{"orderNo":orderId,"orderStatus":"DELIVERED","orderType":"NORMAL"}]}
    orderStatusSync_url = Order_IP + '/v1/order/orderSync/orderStatusSync'
    req = requests.put(orderStatusSync_url,json=param,headers=headers)
    response = json.loads(req.text)
    if response['errorCode'] is not None or response['results']['info'] != '成功':
        print('修改订单状态失败',response)
        exit()
    else:
        print('修改订单状态成功')
        print('-'*20,'修改订单状态结束','-'*20 ,'\n\n')
        return orderId


def UpdateOrderDelivered():
    # 处理订单状态至WAIT_SAPPROCESS
    dealflag = True
    waitTimes = 0
    while dealflag and waitTimes < 5:
        # 获取sales_order中订单状态
        OrderStatus,orderSysId = get_SalesOrderStatus()
        if OrderStatus == 'PENDING':
            dealPending()
            waitTimes += 1
        elif OrderStatus == 'EXCEPTION':
            dealException(orderSysId)
        elif OrderStatus == 'WAIT_SEND_SAP' or OrderStatus == 'WAIT_ROUTE_ORDER':
            dealWaitSend(30)
            waitTimes += 1
        elif OrderStatus == 'WAIT_SAPPROCESS':
            dealflag = False
        elif OrderStatus == 'SIGNED':
            print('订单已经是已签收状态')
            exit()
        if waitTimes >= 5:
            print('已等待五次还未处理成功')
    # 获取purchase_order对应订单记录
    data = getPurchaseOrder()
    #判断是否拆单
    splitFlag = IsSplit(data)
    if splitFlag:
        #拆单情况下更新数据库对应记录
        updateOrder_IsSpilt(data)
    else:
        #未拆单情况下更新数据库对应记录
        updateOrder_NotSpilt(data)
    #修改订单状态
    orderStatusSync()
    print('%s环境已生成已签收订单：%s' % (env,orderId))

if __name__ == '__main__':
    UpdateOrderDelivered()