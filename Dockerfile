FROM python:3.8
ENV PATH /usr/local/bin:$PATH
WORKDIR /app
ADD . /app
RUN pip install -i https://pypi.douban.com/simple/ -r  require.txt
CMD python run.py
