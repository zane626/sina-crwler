FROM python:3.8
ENV PATH /usr/local/bin:$PATH
WORKDIR /app
ADD . /app
#RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ -r  require.txt
CMD python run.py
