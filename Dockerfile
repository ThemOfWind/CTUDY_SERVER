# base
FROM harbor.hudy.co.kr/builder/python-builder:v3.8

# dir copy
COPY ./backend_v2/ /home/workspace/

# worker dir 설정
RUN mkdir -p /home/workspace/logs
WORKDIR /home/workspace/

# python 패키지 설치
RUN pip install --upgrade pip
RUN pip install -r /home/workspace/requirements.txt

# port 설정
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
EXPOSE 8000
RUN chmod 777 /home/workspace/server.sh

# run command 설정
ENTRYPOINT ["/bin/bash", "-c", "/home/workspace/server.sh"]

