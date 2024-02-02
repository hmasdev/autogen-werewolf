FROM python:3.11
COPY . /workspace
WORKDIR /workspace
RUN pip install -r requirements.txt
CMD /bin/bash
