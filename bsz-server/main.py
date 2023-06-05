# coding:utf-8
import json
import subprocess
from urllib.parse import urlparse
import random
import math

import redis
import uvicorn
from fastapi import FastAPI, Request, Header, Response

from get_before_data import get_before_site
from pv import pv
from uv import ip_in_and_conter_out

from env import r, PROD_HOSTS, TEST_HOSTS

app = FastAPI(docs_url=None, redoc_url=None)

@app.get("/busuanzi")
def root(request: Request,
         referer: str = Header(None),
         jsonpCallback: str = ""
         ):
    if not referer:
        return Response(content="Powered by: FastAPI + Redis", media_type="text/plain")
    client_host = request.client.host
    url_res = urlparse(referer)
    host = url_res.netloc
    path = url_res.path

    if host in PROD_HOSTS or PROD_HOSTS=='public':
        # Only access redis if actually visited from production domain
        site_uv, site_pv, page_pv = access_redis(host, path, client_host)
    elif host in TEST_HOSTS:
        # For website development/testing, generate some random fake view counts.
        site_pv = random.randrange(1000,1000000)
        site_uv = math.floor(site_pv/random.randrange(2,6))
        page_pv = math.floor(site_pv/random.randrange(15,100))
    else:
        return Response(content='Invalid domain: host your own service with https://github.com/omltcat/busuanzi-docker')

    dict_data = {
        "site_uv": site_uv,
        "page_pv": page_pv,
        "site_pv": site_pv,
        "version": 2.4
    }
    data_str = "try{" + jsonpCallback + "(" + json.dumps(dict_data) + ");}catch(e){}"
    print(data_str)
    return Response(content=data_str, media_type="application/javascript")

def access_redis(host, path, client_host):
    if "index" in path:
        path = path.split("index")[0]
    site_uv_before = r.get("live_site:%s" % host)
    if not site_uv_before:
        site_uv_before = get_before_site(host)
    else:
        site_uv_before = int(site_uv_before.decode())
    site_uv = ip_in_and_conter_out(host, client_host) + site_uv_before
    page_pv, site_pv = pv(host, path)
    return site_uv, site_pv, page_pv


if __name__ == "__main__":
    # print("chmod redis")
    # subprocess.run(chmod_redis, shell=True)
    # print("start redis")
    # subprocess.Popen(start_redis, shell=True)
    # print("start uvicorn")
    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="info", proxy_headers=True, forwarded_allow_ips="*")
