# =========================================================
# 1. AŞAMA: FRONTEND DERLEME (VUE 3)
# =========================================================
FROM node:20-alpine AS frontend-builder
WORKDIR /frontend

# Sadece package.json dosyalarını kopyalayıp bağımlılıkları yüklüyoruz
COPY frontend/package*.json ./
RUN npm install

# Tüm frontend kaynak kodlarını kopyalayıp üretim derlemesini alıyoruz
COPY frontend/ ./
RUN npm run build

# =========================================================
# 2. AŞAMA: BACKEND & ÇALIŞMA ORTAMI (FASTAPI)
# =========================================================
FROM python:3.11-slim
WORKDIR /app

# Python kütüphanelerinin kurulumu için gerekli sistem araçları
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 🌟 DOĞRU YOL: backend klasörünün altındaki requirements.txt dosyasını alıyoruz
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 🌟 DOĞRU YOL: backend klasörünün içindeki tüm backend kodlarını kopyalıyoruz
COPY backend/ ./

# 1. Aşamada üretilen 'dist' klasörünü otomatik olarak buraya kopyalıyoruz
COPY --from=frontend-builder /frontend/dist ./dist

# Dış dünyaya açılacak port
EXPOSE 8000

ENV BONNA_ADMIN_PASSWORD=admin1234
ENV BONNA_JWT_SECRET=bonna-secure-dynamic-node-crypto-key-2026

# Uygulamayı başlatıyoruz
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]