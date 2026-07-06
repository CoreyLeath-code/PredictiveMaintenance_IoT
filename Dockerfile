# ========================================================
# Stage 1: Build & Dependency Resolution
# ========================================================
FROM python:3.10-slim AS builder

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ========================================================
# Stage 2: Minimal Production Runtime
# ========================================================
FROM python:3.10-slim AS runner

WORKDIR /app
RUN groupadd -r MLOpsUser && useradd -r -g MLOpsUser MLOpsUser

# Copy installed dependencies from the builder layer
COPY --from=builder /root/.local /home/MLOpsUser/.local
COPY src/ /app/src/

ENV PATH=/home/MLOpsUser/.local/bin:$PATH
USER MLOpsUser

EXPOSE 8000
ENTRYPOINT ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
