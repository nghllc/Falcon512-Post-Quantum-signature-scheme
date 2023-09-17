FROM python:3.9-slim-buster

WORKDIR /app

# Cài đặt các gói phụ thuộc và thư viện cần thiết
RUN apt update && apt install -y postgresql libpq-dev && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# Sao chép các file và thư mục liên quan
COPY server.crt /app/server.crt
COPY server.key /app/server.key
COPY server.py /app/server.py
COPY requirements.txt /app/requirements.txt

# Cài đặt các gói phụ thuộc Python
RUN pip install --no-cache-dir -r requirements.txt

# Khai báo port mặc định
EXPOSE 9090

# Chạy ứng dụng
CMD [ "python", "./server.py" ]