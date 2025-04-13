FROM python:3.11-slim
COPY . /workspace
WORKDIR /workspace
RUN pip install uv
RUN uv venv \
    && uv sync \
    && uv pip install pip
ENTRYPOINT ["uv", "run"]
CMD /bin/bash
