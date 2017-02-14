FROM library/python:latest
ADD pollution.py bin/pollution.py
RUN pip install beautifulsoup4
RUN pip install requests

ARG POLL_PASS
ENV POLLUTION_PASS $POLL_PASS
RUN echo $POLL_PASS

CMD python bin/pollution.py