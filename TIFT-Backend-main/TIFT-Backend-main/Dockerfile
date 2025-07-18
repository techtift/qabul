FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y \
        libreoffice \
        libreoffice-writer \
        fonts-dejavu-core \
        fontconfig \
        libxrender1 \
        libxext6 \
        libgl1-mesa-glx \
        libsm6 \
        libxrandr2 \
        libxcb1 \
        xfonts-base \
        xfonts-75dpi && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/media

WORKDIR /app/

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000