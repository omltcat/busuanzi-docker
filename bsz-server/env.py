import os
import redis

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT'))
REDIS_DB = int(os.getenv('REDIS_DB'))
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

PROD_HOSTS = os.getenv('PROD_HOSTS').split(',')
TEST_HOSTS = os.getenv('TEST_HOSTS').split(',')
GET_BEFORE = os.getenv('GET_BEFORE').lower() in ('true', '1', 't')