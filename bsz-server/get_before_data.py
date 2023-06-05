# coding:utf-8
import time
import redis
import requests
from env import r, GET_BEFORE

def get_before_site(host):
    if GET_BEFORE:
        url = "https://busuanzi.ibruce.info/busuanzi?jsonpCallback=BusuanziCallback_777487655111"
        payload = {}
        headers = {
            'Referer': "https://" + host + "/",
            'Cookie': 'busuanziId=89D15D1F66D2494F91FB315545BF9C2A'
        }
        response = None
        TIMES = 0
        while not response:
            response = requests.request("GET", url, headers=headers, data=payload)
            print("首次连接，正在从不蒜子官网拉取数据")
            if TIMES > 30:
                response = 'try{BusuanziCallback_777487655111({"site_uv":0,"page_pv":0,"version":2.4,"site_pv":0});}catch(e){}'
            time.sleep(1)
            TIMES += 1
        str_2_dict = eval(response.text[34:][:-13])
        site_uv = str_2_dict["site_uv"]
        page_pv = str_2_dict["page_pv"]
        site_pv = str_2_dict["site_pv"]
    else:
        site_uv = 0
        page_pv = 0
        site_pv = 0
        print("首次连接，初始化访问量")

    r.set("live_site:%s" % host, site_uv, ex=60 * 60 * 24 * 30)
    r.set("page_pv:%s:/" % host, page_pv)
    r.set("site_pv:%s" % host, site_pv, ex=60 * 60 * 24 * 30)
    print("写入新网址数据成功")
    print("网址: %s" % host)
    print("全站访问人数:%s" % site_uv)
    print("首页访问量:%s" % page_pv)
    print("全站访问量:%s" % site_pv)
    return site_uv

def get_before_page(host, path):
    if GET_BEFORE:
        url = "https://busuanzi.ibruce.info/busuanzi?jsonpCallback=BusuanziCallback_777487655111"
        payload = {}
        headers = {
            'Referer': "https://" + host + path,
            'Cookie': 'busuanziId=89D15D1F66D2494F91FB315545BF9C2A'
        }
        response = None
        TIMES = 0
        while not response:
            response = requests.request("GET", url, headers=headers, data=payload)
            print("无页面数据，从不蒜子拉取")
            if TIMES > 30:
                response = 'try{BusuanziCallback_777487655111({"site_uv":0,"page_pv":0,"version":2.4,"site_pv":0});}catch(e){}'
            time.sleep(1)
            TIMES += 1
        str_2_dict = eval(response.text[34:][:-13])
        page_pv = str_2_dict["page_pv"]
    else:
        page_pv = 0
        print("无页面数据，初始化访问量 " + path)
    
    r.set("page_pv:%s:%s" % (host, path), page_pv)
    print("写入新页面数据成功")
    print("页面: " + host + path)
    print("页面访问量:%s" % page_pv)
    return page_pv
