FROM python:3.10-slim AS builder

WORKDIR /app
# Install C++ compiler required for llama-cpp-python
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc build-essential g++ wget \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# Install standard requirements plus llama-cpp-python
RUN pip install --no-cache-dir --user -r requirements.txt llama-cpp-python

# Download the quantized Phi-3 Mini model (4-bit quantization)
RUN mkdir -p /app/models && \
    wget -O /app/models/phi-3-mini-4k-instruct-q4.gguf \
    "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf"

# --- Stage 2: Minimal Runtime ---
FROM python:3.10-slim AS runner

WORKDIR /app
RUN groupadd -r MLOpsUser && useradd -r -g MLOpsUser MLOpsUser

# Copy installed dependencies and the downloaded model
COPY --from=builder /root/.local /home/MLOpsUser/.local
COPY --from=builder /app/models /app/models
COPY src/ /app/src/

ENV PATH=/home/MLOpsUser/.local/bin:$PATH
USER MLOpsUser

EXPOSE 8000
ENTRYPOINT ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
