
# 🏫 TIFT Fullstack Platform

## 📖 Overview
TIFT - bu to‘liq konteynerlashtirilgan fullstack platforma bo‘lib, foydalanuvchilar bilan oson integratsiya qilish, hujjatlar bilan ishlash va Telegram orqali muloqotni yo‘...
Platforma quyidagi komponentlardan iborat:

- **Backend**: Django (REST API)
- **Frontend**: Static app (masalan, React)
- **Bot**: Telegram bot
- **Database**: PostgreSQL
- **Reverse Proxy**: Nginx (host serverda)
- **CI/CD**: GitHub + Self-hosted Runner

---

## 🧱 Project Structure

```
TIFT-Backend/
├── core/                    # Django ilovasi
├── manage.py                # Django kirish nuqtasi
├── docker-compose.yml       # Barcha xizmatlar uchun
├── Dockerfile               # Backend Dockerfile
├── requirements.txt         # Python kutubxonalari
├── .env                     # Muhit o'zgaruvchilari
├── *.docx / *.jpg / *.png   # Shablonlar va vizual fayllar
```

---

## ⚙️ Technologies Used

| Layer        | Stack                     |
|--------------|---------------------------|
| Backend      | Django, DRF               |
| Bot          | python-Aiogram-bot       |
| Database     | PostgreSQL                |
| Proxy        | Nginx                     |
| Container    | Docker, Docker Compose    |
| CI/CD        | GitHub + Self-hosted Runner |

---

## 🚀 Deployment Guide

### 1. Server Requirements
- Docker & Docker Compose
- Nginx (host serverda)
- GitHub self-hosted runner (serverda o'rnatilgan)

### 2. Clone the Repository
```bash
git clone https://github.com/your-org/tift-backend.git
cd tift-backend
```

### 3. Environment Configuration
`.env` fayl yarating yoki tayyor nusxasidan foydalaning:

```env
# This file contains the environment variables for the project
SECRET_KEY="django-insecure-d9fnkyxkwjgsm3*o99)$0w1$0l7h5!az*&9_&ys^8mup-b"
DEBUG=True
ALLOWED_HOSTS=*

# Database
POSTGRES_USER="postgres"
POSTGRES_PASSWORD="root_password"
POSTGRES_DB="tift"
POSTGRES_HOST="localhost"
POSTGRES_PORT=5432
DJANGO_SETTINGS_MODULE="backend.settings"

# Redis
BASE_URL="https://notify.eskiz.uz/api"
SMS_API_USERNAME="mhoofs3@gmail.com"
SMS_API_PASSWORD="470sfW2MltPgn0iHrKHfhPNNCb5SJiHpZWP2f"
SMS_API_ORGINATOR="4546"

MYGOV_USERNAME=tift-user
MYGOV_PASSWORD=HnAlyin4WYkFIkf
MYGOV_CONSUMER_KEY=ubeOKLqrAq5C0PcoFwBULEa
MYGOV_CONSUMER_SECRET=KfclVIckaC34l5DziwEVd8a

BOT_TOKEN="7626981123:AAFdzNKmXS5URcSwj0vVc7jCwvc3Gk"
ADMINS_ID=118061259,7472466275

MYGOV_AUTH_URL="https://rmp-iskm.egov.uz:9444/oauth2/token"
MYGOV_ADDRESS_API_URL='https://rmp-apimgw.egov.uz:8243/mvd/services/address/info/pin/v1'
MYGOV_DOCUMENT_API_URL='https://rmp-apimgw.egov.uz:8243/gcp/docrest/v1'
MYGOV_LYCEUM_GRADUATE_API_URL='https://rmp-apimgw.egov.uz:8243/minvuz/lyceumgraduate/v1'
MYGOV_DIMPLOMA_API_URL='https://rmp-apimgw.egov.uz:8243/minvuz/services/diploma/v2'
MYGOV_E_SHAHODATNOMA_API_URL='https://rmp-apimgw.egov.uz:8243/xtv/e-shahodatnoma/pinfl/v1'

```

### 4. Build and Run (Local yoki Runner orqali)
```bash
docker-compose up -d --build
```

## 🌐 Nginx Configuration (Serverda)

`/etc/nginx/sites-available/tift.conf`:
```nginx
server {
    listen 80;
    client_max_body_size 100M;
    location /static/ {
    alias /static/;
    access_log off;
    expires 30d;
    add_header Cache-Control "public, max-age=2592000";
    }

    location /media/ {
      alias /home/devuser/pro/backend/media/;
      access_log off;
      expires 30d;
      add_header Cache-Control "public, max-age=2592000";
    }

    location /api/ {
        client_max_body_size 100M;    
        proxy_pass http://backend:8000;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
        
        client_max_body_size 500M;  # Ensure large uploads work here

        proxy_connect_timeout 600;
        proxy_send_timeout 600;
        proxy_read_timeout 600;
        send_timeout 600;
    }

    location /swagger/ {
       client_max_body_size 100M;     
        proxy_pass http://backend:8000;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }

    location /admin/ {
    client_max_body_size 100M;
        proxy_pass http://backend:8000;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }

    location / {
        proxy_pass http://localhost:3000;  
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
        
        client_max_body_size 500M;  # Match /api/

        proxy_connect_timeout 600;
        proxy_send_timeout 600;
        proxy_read_timeout 600;
        send_timeout 600;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/tift.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🤖 Telegram Bot
- Bot Docker konteyner orqali ishlaydi
- Django bilan integratsiyalashgan
- Webhook sozlamalari `.env` faylda bo'ladi

---

## 🔁 CI/CD Workflow (GitHub → Server)

1. `git push` qilganda GitHub Runner ishga tushadi
2. Runner quyidagilarni bajaradi:
   ```bash
   cd /home/ubuntu/tift-backend
   git pull origin main
   docker-compose down
   docker-compose up -d --build
   ```
3. Barcha xizmatlar yangilanadi
4. Nginx static va API trafigini yo'naltiradi

---

## 🔧 Development (Local)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

---

## 📄 Additional Files

| Fayl                     | Tavsif                     |
|--------------------------|-----------------------------|
| `certificate_2025_uz.docx` | Sertifikat shabloni (UZ)     |
| `contract_2025_uz.docx`    | Kontrakt shabloni (UZ)       |
| `pechat.png`              | Muhr rasmi                   |
| `certificate_header.jpg`  | Sertifikat header rasmi      |

---

## 🧑‍💻 Author
**Nodirbek Abduraimov**  
Backend & System Developer & Project Manager
📧 [nodirbyte@gmail.com](mailto:nodirbyte@gmail.com)
