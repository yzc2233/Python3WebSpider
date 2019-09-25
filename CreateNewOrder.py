import requests
import sys
import configparser
import GetIP

config =configparser.ConfigParser()
config.read('properties.conf')


# env = sys.argv[1]
env = 'qa2'

# uid = sys.argv[2]
uid = '2001844981'


skuId =

ShopCart_IP = GetIP.getIp(env,'shop-cart')
Order_IP = GetIP.getIp(env,'order')


def addToCartForSingleProduct():













