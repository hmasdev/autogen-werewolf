FROM python:3.11
COPY . /workspace
WORKDIR /workspace
RUN pip install -e .
CMD /bin/bash
