FROM python:3.9-slim-buster

WORKDIR /app

# Sao chép các file và thư mục liên quan
COPY client.py /app/client.py
COPY server.crt /app/server.crt

# Cài đặt các gói phụ thuộc Python
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Chạy ứng dụng
CMD [ "python", "./client.py" ]