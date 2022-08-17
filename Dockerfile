FROM python:3.8
ENV PATH /usr/local/bin:$PATH
WORKDIR /app
ADD . /app
# -i https://mirrors.aliyun.com/pypi/simple/
RUN pip install -r  require.txt -i httpsg://pypi.douban.com/simple/
CMD python run.py
