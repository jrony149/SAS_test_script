FROM python:3
ADD src src
COPY . /
  
RUN chmod +x /run.sh

CMD ["/run.sh"]
