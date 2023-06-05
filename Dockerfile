FROM python:3.9.5-alpine
WORKDIR /bsz-server
ADD ./bsz-server /bsz-server
# RUN pip install -i http://mirrors.tencentyun.com/pypi/simple --trusted-host mirrors.tencentyun.com --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt
ENV REDIS_HOST bsz-redis
ENV REDIS_PORT 6379
ENV REDIS_DB 0
ENV PROD_HOSTS public
ENV TEST_HOSTS localhost
ENV GET_BEFORE true
ENTRYPOINT ["python3", "main.py"]
EXPOSE 8080
CMD ["/bin/sh"]