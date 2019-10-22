#coding=utf-8
import os
import requests
import sys
import GetIP
import time
import json

try:
    import pymysql
except:
    print('pymysql模块未安装，现在开始安装')
    os.system('pip install pymysql')
    import pymysql


try:
    import configparser
except:
    print('configparser模块未安装，现在开始安装')
    os.system('pip install configparser')
    import configparser

config =configparser.ConfigParser()
config.read('properties.conf')

allowedenv = config.get('allowedenv','allowedenv')
allowedenv = allowedenv.split(',')

print('仅支持Python3环境')

def getskuIdlist():
    print('-'*20,'开始数据库随机获取两个skuId，请稍作等待','-'*20)
    datalist = []
    conn = pymysql.connect(mysqlhost,mysqluser,mysqlpassword,'product')
    cur = conn.cursor()
    sql = "select b.sku_id from prod_product a LEFT JOIN prod_sku b on a.id=b.product_id left join  inventory.inventory c on CONVERT(c.sku_code USING utf8) COLLATE utf8_unicode_ci  =b.sku_code JOIN (SELECT ROUND(RAND() * ((SELECT MAX(id) FROM prod_product)-(SELECT MIN(id) FROM prod_product))+(SELECT MIN(id) FROM prod_product)) AS id) AS t2 where a.`status`=1 and b.`status`=1 and b.sku_type=1  and b.sale_channel->'$[0]'='ALL' and  c.inventory_type=1 and c.quantity>100  and a.id >= t2.id limit 2"
    cur.execute(sql)
    data = cur.fetchall()
    for da in data:
        datalist.append(da[0])
    print('获取到的skuId的集合是 %s' %datalist)
    print('-'*20,'数据库获取随机两个skuId结束','-'*20,'\n\n')
    cur.close()
    return datalist


skuIdlist = []
inputargvlength = len(sys.argv)

if inputargvlength < 3:
    print('请输入完整的请求至少包含：需要执行的文件 执行环境 用户uid，example：python CreateNewOrder.py qa2 2001844981 \n','需在文件目录下执行命令')
    exit()
elif inputargvlength >= 3:
    env = sys.argv[1].lower()
    if env not in allowedenv:
        print('输入的环境 %s 有误，仅支持qa2及stage环境！' %env)
        exit()
    mysqlhost = config['mysql_'+ env]['host']
    mysqluser = config['mysql_'+ env]['user']
    mysqlpassword = config['mysql_'+ env]['password']
    uid = sys.argv[2]
    try:
        uid = int(uid)
        uid = str(uid)
    except ValueError as e:
        print('输入的用户uid：%s 格式错误' %uid)
        exit()
    defaultskuId = [config['skuId'][env + '_skuId']]
    if inputargvlength > 3:
        for arg in sys.argv[3:]:
            try:
                skuIdlist.append(int(arg))
            except ValueError:
                print('输入的skuId集合中 %s 格式错误！' %arg)
                exit()
    elif inputargvlength == 3:
        skuIdlist = getskuIdlist()
    else:
        skuIdlist = defaultskuId

# env = 'qa2'
# uid = '2001844981'

ShopCart_IP = GetIP.getIp(env,'shop-cart')
Order_IP = GetIP.getIp(env,'order')

def addToCartForSingleProduct(skuId):
    print('-'*20,'开始添加单个商品至购物车','-'*20)
    headers = {"Content-Type":"application/json","uid":uid}
    param = {"queryBody":{"channel":"PC","checked":1,"quantity":2,"skuId":skuId,"type":1}}
    addproduct_url = ShopCart_IP + '/v1/shopcart/shopcart/addToCartForSingleProduct'
    req = requests.post(addproduct_url,json=param,headers=headers)
    response = json.loads(req.text)
    if response['errorCode'] is not None or response['results'] <=0:
        print('添加单个商品%s至购物车失败：%s' %(skuId,response))
        exit()
    else:
        print('添加单个商品%s至购物车成功' %skuId)
    print('-'*20,'添加单个商品至购物车结束','-'*20 ,'\n\n')

def getShopcartStepTwo():
    print('-'*20,'开始购物车第二步','-'*20)
    headers = {"Content-Type":"application/json","uid":uid}
    param = {"queryBody":{"orderType":"1","channel":"PC"}}
    ShopcartStepTwo_url = ShopCart_IP + '/v1/shopcart/shopcart/getShopcartStepTwo'
    req = requests.post(ShopcartStepTwo_url,json=param,headers=headers)
    response = json.loads(req.text)
    if response['errorCode'] is not None:
        print('购物车第二步失败',response)
        exit()
    else:
        print('购物车第二步成功')
    print('-'*20,'开始购物车第二步结束','-'*20 ,'\n\n')

def clearShopcartSkuId(skuId):
    print('-'*20,'开始清除购物车指定商品','-'*20)
    skuId = str(skuId)
    headers = {"Content-Type":"application/json","uid":uid}
    param = {"head":{"token":"string","userId":"string"},"queryBody":[{"skuId":skuId,"type":1,"userId":uid}]}
    clearShopcartSkuId_url = ShopCart_IP + '/v1/shopcart/shopcart/removeFromCart'
    req = requests.post(clearShopcartSkuId_url,json=param,headers=headers)
    response = json.loads(req.text)
    if response['errorCode'] is not None:
        print('清除购物车指定商品%s失败 %s'%(skuId,response))
        exit()
    else:
        print('清除购物车指定商品%s成功' %skuId)
    print('-'*20,'清除购物车指定商品结束','-'*20 ,'\n\n')

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
    print('-'*20,'修改支付方式结束','-'*20 ,'\n\n')

def addOrders():
    print('-'*20,'开始提交订单','-'*20)
    headers = {"Content-Type":"application/json","uid":uid}
    param = {"queryBody":{"channel":"PC","type":1,"firstOrderSource":{"utm_source":"samsung","utm_medium":"referral","utm_campaign":"bixby","utm_content":"undefined","utm_term":"undefined"}}}
    addOrders_url = ShopCart_IP + '/v1/shopcart/order/addOrders'
    req = requests.post(addOrders_url,json=param,headers=headers)
    response = json.loads(req.text)
    if response['errorCode'] is not None or response['results']['resultStatus'] != 'SUCCESS':
        print('提交订单失败',response)
        #清除添加的商品
        for skuId in skuIdlist:
            time.sleep(1)
            clearShopcartSkuId(skuId)
            print('\n创建订单失败')
        exit()
    else:
        orderId = response['results']['orderId']
        print('提交订单成功，订单号：',orderId)
        print('-'*20,'提交订单结束','-'*20 ,'\n\n')
        return orderId


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
        time.sleep(3)
    print('-'*20,'推送订单至OMS并索引至elasticSearch结束','-'*20 ,'\n\n')

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
    if not data == 0:
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
    finally:
        cursor.close()
        print('-'*20,'将订单提前一小时结束','-'*20 ,'\n\n')


def CreateNewOrder():
    ## 循环添加单个商品至购物车
    for sku in skuIdlist:
        addToCartForSingleProduct(sku)
    ## 购物车第二步
    getShopcartStepTwo()
    ## 修改支付方式
    changePayment()
    ## 提交订单
    orderId = addOrders()
    time.sleep(5)
    ## 将订单提前一小时
    forwadOnehour(orderId)
    ## 推送订单至OMS并索引至elasticSearch
    orderSync(orderId)
    return orderId


if __name__ == '__main__':
    CreateNewOrder()


