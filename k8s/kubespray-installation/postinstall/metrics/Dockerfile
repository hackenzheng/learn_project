FROM ubuntu:16.04
RUN apt-get update && apt-get install -y python3.5 python3-pip
RUN pip3 install --upgrade pip kubernetes -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
RUN mkdir -p /workdir
ADD metrics.py /workdir/metrics.py
WORKDIR /workdir
CMD ["python3", "metrics.py"]
