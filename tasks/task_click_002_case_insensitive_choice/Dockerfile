# Harbor v0.25.x Standardized Task Container
FROM python:3.11-slim

WORKDIR /workspace

# System dependencies
RUN apt-get update && apt-get install -y git bash curl && rm -rf /var/lib/apt/lists/*

# Clone baseline repository
RUN git clone https://github.com/pallets/click /workspace && \
    git checkout 7eb021a68430dc0702d1d0ad510617ad4ea9ad27

# Environment setup
RUN pip install --upgrade pip
RUN pip install pytest
RUN pip install -e .


# Copy task verification harness
COPY test.sh /test.sh
COPY test_feature.py /test_feature.py
RUN chmod +x /test.sh

CMD ["/test.sh"]
