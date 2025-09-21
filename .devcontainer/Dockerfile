# Base Debian image for devcontainers features
FROM mcr.microsoft.com/devcontainers/base:bookworm

# Install make (and build tools for native Python deps)
RUN apt-get update && \
    apt-get install -y --no-install-recommends make build-essential && \
    rm -rf /var/lib/apt/lists/*