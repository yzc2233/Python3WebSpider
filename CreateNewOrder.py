import requests
import pymysql
import sys
import json
import configparser
import GetIP
import time

config =configparser.ConfigParser()
config.read('properties.conf')


# env = sys.argv[1].lower()
env = 'qa2'

# uid = sys.argv[2]
uid = '2001844981'

skuId = config['skuId'][env + '_skuId']

mysqlhost = config['mysql_'+ env]['host']
mysqluser = config['mysql_'+ env]['user']
mysqlpassword = config['mysql_'+ env]['password']

ShopCart_IP = GetIP.getIp(env,'shop-cart')
Order_IP = GetIP.getIp(env,'order')


def addToCartForSingleProduct():
    print('-'*20,'开始添加单个商品至购物车','-'*20)
    headers = {"Content-Type":"application/json","uid":uid}
    param = {"queryBody":{"channel":"PC","checked":1,"quantity":1,"skuId":skuId,"type":1}}
    addproduct_url = ShopCart_IP + '/v1/shopcart/shopcart/addToCartForSingleProduct'
    req = requests.post(addproduct_url,json=param,headers=headers)
    response = json.loads(req.text)
    if response['errorCode'] is not None or response['results'] <=0:
        print('开始添加单个商品至购物车失败',response)
        exit()
    else:
        print('开始添加单个商品至购物车成功')
    print('-'*20,'添加单个商品至购物车结束','-'*20)

def getShopcartStepTwo():
    print('-'*20,'开始购物车第二步','-'*20)
    headers = {"Content-Type":"application/json","uid":uid}
    param = {"queryBody":{"orderType":"1","channel":"PC"}}
    ShopcartStepTwo_url = ShopCart_IP + '/v1/shopcart/shopcart/getShopcartStepTwo'
    req = requests.post(ShopcartStepTwo_url,json=param,headers=headers)
    response = json.loads(req.text)
    if response['errorCode'] is not None:
        print('开始购物车第二步失败',response)
        exit()
    else:
        print('开始购物车第二步成功')
    print('-'*20,'开始购物车第二步结束','-'*20)

def changePayment():
    print('-'*20,'开始修改支付方式','-'*20)
    headers = {"Content-Type":"application/json","uid":uid}
    param = {"queryBody":{"payMethod":"COD","type":"1"}}
    changePayment_url = ShopCart_IP + '/v1/shopcart/payment/changePayment'
    req = requests.put(changePayment_url,json=param,headers=headers)
    response = json.loads(req.text)
    if response['errorCode'] is not None or response['results']['status'] != 'SUCCESS':
        print('修改支付方式失败',response)
        exit()
    else:
        print('修改支付方式成功')
    print('-'*20,'修改支付方式结束','-'*20)

def addOrders():
    print('-'*20,'开始提交订单','-'*20)
    headers = {"Content-Type":"application/json","uid":uid}
    param = {"queryBody":{"channel":"PC","type":1,"firstOrderSource":{"utm_source":"samsung","utm_medium":"referral","utm_campaign":"bixby","utm_content":"undefined","utm_term":"undefined"}}}
    addOrders_url = ShopCart_IP + '/v1/shopcart/order/addOrders'
    req = requests.post(addOrders_url,json=param,headers=headers)
    response = json.loads(req.text)
    if response['errorCode'] is not None or response['results']['resultStatus'] != 'SUCCESS':
        print('提交订单失败',response)
        exit()
    else:
        orderId = response['results']['orderId']
        print('提交订单成功，订单号：',orderId)
        return orderId
    print('-'*20,'提交订单结束','-'*20)

def orderSync(orderId):
    print('-'*20,'开始推送订单至OMS并索引至elasticSearch','-'*20)
    orderSync_url = Order_IP + '/v1/order/orderSync/orderSync/' + orderId
    req = requests.get(orderSync_url)
    response = json.loads(req.text)
    if response['errorCode'] is not None or response['results'] is not True:
        print('推送订单至OMS并索引至elasticSearch失败:',response)
        exit()
    else:
        print('推送订单至OMS并索引至elasticSearch成功')
    print('-'*20,'推送订单至OMS并索引至elasticSearch结束','-'*20)

def forwadOnehour(orderId):
    print('-'*20,'开始将订单提前一小时','-'*20)
    # 连接数据库
    conn = pymysql.connect(mysqlhost,mysqluser,mysqlpassword,'order')
    # 得到一个可执行的光标对象
    cursor = conn.cursor()
    # 定义要执行的额SQL语句
    print('查询订单号为 %s 的订单记录' %orderId)
    sql = "select * from orders where order_id="+"'"+orderId+"';"
    print(sql)
    cursor.execute(sql)
    data = cursor.fetchone()
    if len(data) == 0:
        print('未找到订单号为 %s 的记录' %orderId)
        exit()
    print('数据库开始将订单号为 %s 的订单记录创建时间提前一小时' %orderId)
    updatesql = "update orders set create_time=DATE_SUB(create_time ,INTERVAL 1 HOUR) where order_id="+"'"+orderId+"';"
    print(updatesql)
    try :
        # 执行更新语句
        cursor.execute(updatesql)
        # 提交到数据库执行
        conn.commit()
        print('数据库开始将订单号为 %s 的订单记录创建时间提前一小时成功' %orderId)
        time.sleep(3)
    except:
        # 发生错误时回滚
        conn.rollback()
        print('数据库开始将订单号为 %s 的订单记录创建时间提前一小时失败' %orderId)
        exit()
    print('-'*20,'将订单提前一小时结束','-'*20)


def CreateNewOrder():
    ## 添加单个商品至购物车
    addToCartForSingleProduct()
    ## 购物车第二步
    getShopcartStepTwo()
    ## 修改支付方式
    changePayment()
    ## 提交订单
    orderId = addOrders()
    ## 将订单提前一小时
    forwadOnehour(orderId)
    ## 推送订单至OMS并索引至elasticSearch
    orderSync(orderId)
    return orderId


if __name__ == '__main__':
    CreateNewOrder()



