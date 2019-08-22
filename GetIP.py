'''
    使用Xpath获取对应IP
'''
import requests
from requests import RequestException
from lxml import etree
from urllib.parse import urlsplit

def get_html(env='stage'):
    env = env.lower()
    if env == 'stage':
        url = 'http://10.157.24.76:1111/'
    elif env == 'qa2':
        url = 'http://10.157.46.144:1111/'
    # elif env == 'prd':
    #     url = 'http://10.157.32.29:1111/'
    else:
        print('请输入正确的运行环境！')
        return None
    try :
        Response = requests.get(url)
        if Response.status_code == 200:
            return Response.text
        return None
    except RequestException as e:
        print('Error: ',e)


def get_services_ip(html):
    if html != None:
        html = etree.HTML(html)
        services = html.xpath('//*/body/div/table/tbody/tr/td[1]/b/text()')
        ip = html.xpath('//*/body/div/table/tbody/tr/td[4]/a[1]/@href')[:]
        iplen = len(ip)
        for i in range(iplen):
            results = urlsplit(ip[i])
            ip[i] = results.scheme + ':' + results.netloc
        services_ip = dict(zip(services,ip))
        return services_ip

def get_service_ip(service,services_ip):
    service = service.upper()
    if service == None or service == '':
        return '输入的service不存在或不符合要求'
    for key in services_ip.keys():
        if service in str(key):
            ip = services_ip.get(key)
    return ip

def main(service,env='stage'):
    html = get_html(env)
    services = get_services_ip(html)
    ip = get_service_ip(service,services)
    print(ip)
    return ip



if __name__ == '__main__':
    main('myacc')




