# coding:utf-8
import redis
from env import r

def ip_in_and_conter_out(site_name, ip):
    r.sadd("site_uv:%s" % site_name, ip)
    site_uv = r.scard("site_uv:%s" % site_name)
    r.expire("site_uv:%s" % site_name, 60 * 60 * 24 * 30)
    r.expire("live_site:%s" % site_name, 60 * 60 * 24 * 30)
    return site_uv
