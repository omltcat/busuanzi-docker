import redis
from get_before_data import get_before_page
from env import r

def pv(host, path):
    # Get before pv data for page
    page_pv_before = r.get("page_pv:%s:%s" % (host, path))
    if not page_pv_before:
        page_pv_before = get_before_page(host, path)

    page_pv = r.incr("page_pv:%s:%s" % (host, path))
    # page_pv no increase
    # r.expire("page_pv:%s:%s" % (host, path), 60 * 60 * 24 * 30)
    site_pv = r.incr("site_pv:%s" % host)
    r.expire("site_pv:%s" % host, 60 * 60 * 24 * 30)
    return page_pv, site_pv