FROM django:latest
ENV PYTHON_VERSION 3.6.5
RUN mkdir /trigrams
WORKDIR /trigrams
ADD . /trigrams
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["/bin/bash", "/trigrams/init.sh"]
ENTRYPOINT ["/bin/bash", "/trigrams/run.sh"]