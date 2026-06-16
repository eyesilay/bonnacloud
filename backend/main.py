import os
import io
import json
import zipfile
import mimetypes
import urllib.parse
import requests
from typing import List, Optional
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from jose import JWTError, jwt
import bcrypt

from database import SessionLocal, UserDB, RoleDB, Base, engine

# =========================================================
# 🛡️ VERİTABANI ŞEMALARI
# =========================================================
class RoleRequest(BaseModel):
    name: str
    allowedFolders: List[dict] = []

class UserCreateRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str
    role_id: Optional[int] = None
    isActive: bool = True

class UserUpdateRequest(BaseModel):
    name: str
    email: str
    password: Optional[str] = None
    role: str
    role_id: Optional[int] = None
    isActive: bool = True

class ZipDownloadRequest(BaseModel):
    paths: List[str]

class LoginRequest(BaseModel):
    email: str
    password: str

class CDNConfigUpdateRequest(BaseModel):
    storageName: str
    storagePassword: str
    pullZoneUrl: str
    region: str

# =========================================================
# ALTYAPI VE GÜVENLİK AYARLARI
# =========================================================
os.makedirs("/app/data", exist_ok=True)
Base.metadata.create_all(bind=engine)

SECRET_KEY = os.getenv("BONNA_JWT_SECRET", "bonna-secure-dynamic-node-crypto-key-2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 180 

security_bearer = HTTPBearer()

# ⚡ LIGHTNING CACHE ENGINE STATS (RAM Önbellek Yapısı)
GLOBAL_FILE_INDEX = []
LAST_INDEX_TIME = None
CACHE_DURATION_MINUTES = 5

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try: return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except: return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security_bearer), db: Session = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None: raise HTTPException(status_code=401, detail="Geçersiz oturum anahtarı.")
    except JWTError: raise HTTPException(status_code=401, detail="Oturum doğrulaması başarısız.")
    
    user = db.query(UserDB).filter(UserDB.email == email).first()
    if not user: raise HTTPException(status_code=401, detail="Kullanıcı sistemde bulunamadı.")
    if not user.is_active: raise HTTPException(status_code=403, detail="Hesabınız dondurulmuştur.")
    return user

def init_db():
    try:
        with engine.connect() as conn:
            try: conn.execute(text("ALTER TABLE users ADD COLUMN failed_login_attempts INTEGER DEFAULT 0;")); conn.commit()
            except: pass
            try: conn.execute(text("ALTER TABLE users ADD COLUMN lockout_until DATETIME;")); conn.commit()
            except: pass
            try: conn.execute(text("ALTER TABLE users ADD COLUMN role_id INTEGER REFERENCES roles(id);")); conn.commit()
            except: pass
    except Exception as e: print(f"Database sync alert: {e}")

    db = SessionLocal()
    try:
        admin_role = db.query(RoleDB).filter(RoleDB.name == "Yönetici (Admin)").first()
        if not admin_role:
            admin_role = RoleDB(name="Yönetici (Admin)", allowed_folders=[{"id": "", "name": "Tüm Sunucu", "allowed": True}])
            db.add(admin_role)
            db.commit()
            db.refresh(admin_role)

        admin = db.query(UserDB).filter(UserDB.role == "admin").first()
        if not admin:
            raw_password = os.getenv("BONNA_ADMIN_PASSWORD", "admin")
            new_admin = UserDB(name="Sistem Yöneticisi", email="admin@bonnacloud.com", password=get_password_hash(raw_password), role="admin", role_id=admin_role.id, is_active=True)
            db.add(new_admin)
            db.commit()
        elif admin and not admin.role_id:
            admin.role_id = admin_role.id
            db.commit()
    finally: db.close()

init_db()

app = FastAPI(title="Bonna Cloud Engine")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"], expose_headers=["Content-Disposition"])

CONFIG_FILE = "/app/data/cdn_config.json"
DEFAULT_CONFIG = {"BUNNY_STORAGE_NAME": "bonna-api-test", "BUNNY_STORAGE_PASSWORD": "password", "BUNNY_PULL_ZONE_URL": "url", "BUNNY_REGION": ""}

def load_cdn_config():
    if os.path.exists(CONFIG_FILE):
        try: return json.load(open(CONFIG_FILE, "r"))
        except: return DEFAULT_CONFIG
    return DEFAULT_CONFIG

def save_cdn_config(config_data):
    with open(CONFIG_FILE, "w") as f: json.dump(config_data, f)

def get_bunny_base_url():
    cfg = load_cdn_config()
    storage_name = cfg.get("BUNNY_STORAGE_NAME")
    region = cfg.get("BUNNY_REGION")
    region_prefix = f"{region}." if region else ""
    return f"https://{region_prefix}storage.bunnycdn.com/{storage_name}"

def clean_path(p: str) -> str:
    if not p: return ""
    return p.strip("/")

# ROLE API
@app.get("/api/roles")
def get_roles(db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    if current_user.role != "admin": raise HTTPException(status_code=403, detail="Yetkiniz yok.")
    return [{"id": r.id, "name": r.name, "allowedFolders": r.allowed_folders or []} for r in db.query(RoleDB).all()]

@app.post("/api/roles")
def create_role(payload: RoleRequest, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    if current_user.role != "admin": raise HTTPException(status_code=403, detail="Yetkiniz yok.")
    if db.query(RoleDB).filter(RoleDB.name == payload.name).first(): raise HTTPException(status_code=400, detail="Bu isimde bir rol zaten mevcut.")
    db.add(RoleDB(name=payload.name, allowed_folders=payload.allowedFolders))
    db.commit()
    return {"message": "Rol başarıyla oluşturuldu."}

@app.put("/api/roles/{role_id}")
def update_role(role_id: int, payload: RoleRequest, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    if current_user.role != "admin": raise HTTPException(status_code=403, detail="Yetkiniz yok.")
    role = db.query(RoleDB).filter(RoleDB.id == role_id).first()
    if not role: raise HTTPException(status_code=404, detail="Rol bulunamadı.")
    role.name = payload.name; role.allowed_folders = payload.allowedFolders
    db.commit()
    return {"message": "Rol başarıyla güncellendi."}

@app.delete("/api/roles/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    if current_user.role != "admin": raise HTTPException(status_code=403, detail="Yetkiniz yok.")
    role = db.query(RoleDB).filter(RoleDB.id == role_id).first()
    if not role: raise HTTPException(status_code=404, detail="Rol bulunamadı.")
    db.query(UserDB).filter(UserDB.role_id == role_id).update({UserDB.role_id: None})
    db.delete(role)
    db.commit()
    return {"message": "Rol başarıyla silindi."}

# KULLANICI API
@app.get("/api/users")
def get_users(db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    if current_user.role != "admin": raise HTTPException(status_code=403, detail="Yetkiniz yok.")
    return [{"id": u.id, "name": u.name, "email": u.email, "role": u.role, "role_id": u.role_id, "role_name": u.role_rel.name if u.role_rel else "Rol Atanmamış", "isActive": u.is_active} for u in db.query(UserDB).all()]

@app.post("/api/users")
def create_user(payload: UserCreateRequest, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    if current_user.role != "admin": raise HTTPException(status_code=403, detail="Yetkiniz yok.")
    if db.query(UserDB).filter(UserDB.email == payload.email).first(): raise HTTPException(status_code=400, detail="Bu e-posta adresi kullanımda.")
    db.add(UserDB(name=payload.name, email=payload.email, password=get_password_hash(payload.password), role=payload.role, role_id=payload.role_id, is_active=payload.isActive))
    db.commit()
    return {"message": "Kullanıcı başarıyla oluşturuldu."}

@app.put("/api/users/{user_id}")
def update_user(user_id: int, payload: UserUpdateRequest, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    if current_user.role != "admin": raise HTTPException(status_code=403, detail="Yetkiniz yok.")
    target_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not target_user: raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")
    target_user.name = payload.name; target_user.email = payload.email; target_user.role = payload.role; target_user.role_id = payload.role_id; target_user.is_active = payload.isActive
    if payload.password: target_user.password = get_password_hash(payload.password)
    db.commit()
    return {"message": "Kullanıcı başarıyla güncellendi."}

@app.delete("/api/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    if current_user.role != "admin": raise HTTPException(status_code=403, detail="Yetkiniz yok.")
    target_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not target_user: raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")
    if target_user.id == current_user.id: raise HTTPException(status_code=400, detail="Kendi hesabınızı silemezsiniz.")
    db.delete(target_user)
    db.commit()
    return {"message": "Kullanıcı başarıyla silindi."}

@app.post("/api/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.email == payload.email).first()
    if not user or not user.is_active: raise HTTPException(status_code=401, detail="Giriş başarısız.")
    if not verify_password(payload.password, user.password): raise HTTPException(status_code=401, detail="Giriş başarısız.")
    token = create_access_token(data={"sub": user.email, "role": user.role}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"id": user.id, "name": user.name or "Sistem Yöneticisi", "email": user.email, "role": user.role, "role_id": user.role_id, "allowedFolders": user.allowed_folders if user.allowed_folders else [], "isActive": user.is_active, "token": token}

@app.get("/api/cdn")
def get_cdn_settings(current_user: UserDB = Depends(get_current_user)):
    if current_user.role != "admin": raise HTTPException(status_code=403, detail="Yetkiniz yok.")
    cfg = load_cdn_config()
    return {"storageName": cfg.get("BUNNY_STORAGE_NAME"), "storagePassword": cfg.get("BUNNY_STORAGE_PASSWORD"), "pullZoneUrl": cfg.get("BUNNY_PULL_ZONE_URL"), "region": cfg.get("BUNNY_REGION")}

@app.post("/api/cdn")
def update_cdn_settings(payload: CDNConfigUpdateRequest, current_user: UserDB = Depends(get_current_user)):
    global LAST_INDEX_TIME
    if current_user.role != "admin": raise HTTPException(status_code=403, detail="Yetkiniz yok.")
    save_cdn_config({"BUNNY_STORAGE_NAME": payload.storageName, "BUNNY_STORAGE_PASSWORD": payload.storagePassword, "BUNNY_PULL_ZONE_URL": payload.pullZoneUrl, "BUNNY_REGION": payload.region})
    LAST_INDEX_TIME = None 
    return {"message": "CDN ayarları başarıyla güncellendi."}

# PERMISSION SYSTEM
def check_hierarchical_permission(item_path: str, allowed_folders: list) -> bool:
    path_clean = clean_path(item_path)
    if not path_clean: return True
    allowed_map = {clean_path(f.get("id", "")): f.get("allowed", True) for f in allowed_folders}
    if path_clean in allowed_map: return allowed_map[path_clean] is True
    parts = path_clean.split('/')
    for i in range(len(parts) - 1, 0, -1):
        if '/'.join(parts[:i]) in allowed_map: return allowed_map['/'.join(parts[:i])] is True
    return False

# 🌟 GÜNCELLEME: TEKİL DOSYALARI BOYUTU VE ÖNİZLEME LİNKİYLE AKTARAN MOTOR
@app.get("/files")
def get_files(path: str = "", db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    clean_p = clean_path(path)
    cfg = load_cdn_config()
    allowed_folders = current_user.role_rel.allowed_folders if current_user.role_rel else []

    if current_user.role == "müşteri":
        if not allowed_folders: allowed_folders = current_user.allowed_folders or []
        # Kök dizin (Home) oluşturulurken izin verilen tekil dosyaların link ve boyutunu dinamik süz
        if not clean_p:
            allowed_entries = [f for f in allowed_folders if f.get("allowed", True) is True]
            result = []
            for f in allowed_entries:
                m_type = f.get("mimeType", "application/vnd.google-apps.folder")
                is_dir = (m_type == "application/vnd.google-apps.folder")
                item_path = clean_path(f.get("id", ""))
                
                web_link = ""
                if not is_dir:
                    web_link = f"{cfg.get('BUNNY_PULL_ZONE_URL')}/{urllib.parse.quote(item_path, safe='/')}"
                    
                result.append({
                    "id": item_path,
                    "name": f.get("name"),
                    "mimeType": m_type,
                    "size": f.get("size", 0),
                    "webViewLink": web_link
                })
            return {"files": result}
        if not check_hierarchical_permission(clean_p, allowed_folders): return {"error": "Erişim izni yok.", "files": []}

    quoted_p = urllib.parse.quote(clean_p, safe='/')
    url = f"{get_bunny_base_url()}/{quoted_p}/" if quoted_p else f"{get_bunny_base_url()}/"
    try:
        resp = requests.get(url, headers={"AccessKey": cfg.get("BUNNY_STORAGE_PASSWORD"), "accept": "application/json"}, timeout=15)
        if resp.status_code != 200: return {"files": []}
    except: raise HTTPException(status_code=502, detail="CDN Hatası.")

    result = []
    for item in resp.json():
        is_dir = item.get("IsDirectory", False)
        name = item.get("ObjectName")
        item_path = f"{clean_p}/{name}" if clean_p else name
        if current_user.role == "müşteri" and not check_hierarchical_permission(item_path, allowed_folders): continue
        mime_type = "application/vnd.google-apps.folder" if is_dir else (mimetypes.guess_type(name)[0] or "application/octet-stream")
        result.append({"id": item_path, "name": name, "mimeType": mime_type, "size": item.get("Length", 0), "webViewLink": f"{cfg.get('BUNNY_PULL_ZONE_URL')}/{urllib.parse.quote(item_path, safe='/')}" if not is_dir else ""})
    return {"files": result}

# RAM TABANLI HIZLI ARAMA MOTORU
@app.get("/api/search")
def search_files(query: str, current_user: UserDB = Depends(get_current_user)):
    global GLOBAL_FILE_INDEX, LAST_INDEX_TIME
    now = datetime.utcnow()
    if not LAST_INDEX_TIME or (now - LAST_INDEX_TIME) > timedelta(minutes=CACHE_DURATION_MINUTES):
        cfg = load_cdn_config()
        base_url = get_bunny_base_url()
        headers = {"AccessKey": cfg.get("BUNNY_STORAGE_PASSWORD"), "accept": "application/json"}
        compiled_list = []
        queue = [""]
        folders_scanned = 0

        while queue and folders_scanned < 85:
            current_path = queue.pop(0)
            folders_scanned += 1
            url = f"{base_url}/{urllib.parse.quote(current_path, safe='/')}/" if current_path else f"{base_url}/"
            try:
                resp = requests.get(url, headers=headers, timeout=10)
                if resp.status_code == 200:
                    for item in resp.json():
                        is_dir = item.get("IsDirectory", False)
                        name = item.get("ObjectName")
                        item_path = f"{current_path}/{name}" if current_path else name
                        mime_type = "application/vnd.google-apps.folder" if is_dir else (mimetypes.guess_type(name)[0] or "application/octet-stream")
                        compiled_list.append({"id": item_path, "name": name, "mimeType": mime_type, "size": item.get("Length", 0), "webViewLink": f"{cfg.get('BUNNY_PULL_ZONE_URL')}/{urllib.parse.quote(item_path, safe='/')}" if not is_dir else ""})
                        if is_dir: queue.append(item_path)
            except: pass
        GLOBAL_FILE_INDEX = compiled_list
        LAST_INDEX_TIME = datetime.utcnow()

    result_list = []
    query_lower = query.lower()
    allowed_folders = current_user.role_rel.allowed_folders if current_user.role_rel else []
    if not allowed_folders: allowed_folders = current_user.allowed_folders or []

    for item in GLOBAL_FILE_INDEX:
        item_path = item["id"]
        name = item["name"]
        if current_user.role == "müşteri" and not check_hierarchical_permission(item_path, allowed_folders): continue
        if query_lower in name.lower():
            if current_user.role == "müşteri":
                if not any(item_path == clean_path(f.get("id", "")) or item_path.startswith(clean_path(f.get("id", "")) + "/") for f in allowed_folders): continue
            result_list.append(item)
    return {"files": result_list}

@app.get("/download/file")
def download_file(path: str, current_user: UserDB = Depends(get_current_user)):
    cfg = load_cdn_config()
    url = f"{get_bunny_base_url()}/{urllib.parse.quote(clean_path(path), safe='/')}"
    try:
        resp = requests.get(url, headers={"AccessKey": cfg.get("BUNNY_STORAGE_PASSWORD")}, stream=True)
        if resp.status_code != 200: raise HTTPException(status_code=404, detail="Bulunamadı.")
        return StreamingResponse(resp.iter_content(chunk_size=8192), media_type=resp.headers.get("Content-Type", "application/octet-stream"), headers={"Content-Disposition": f"attachment; filename={urllib.parse.quote(path.split('/')[-1])}"})
    except: raise HTTPException(status_code=502, detail="CDN Hatası.")

@app.post("/download/zip")
def download_zip(payload: ZipDownloadRequest, current_user: UserDB = Depends(get_current_user)):
    cfg = load_cdn_config()
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for path in payload.paths:
            url = f"{get_bunny_base_url()}/{urllib.parse.quote(clean_path(path), safe='/')}"
            try:
                resp = requests.get(url, headers={"AccessKey": cfg.get("BUNNY_STORAGE_PASSWORD")})
                if resp.status_code == 200: zip_file.writestr(path.split("/")[-1], resp.content)
            except: pass
    zip_buffer.seek(0)
    return StreamingResponse(zip_buffer, media_type="application/zip", headers={"Content-Disposition": "attachment; filename=BonnaCloud_Export.zip"})

if os.path.isdir("dist"): app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    if full_path.startswith("api/") or full_path == "files" or full_path.startswith("download/"): return JSONResponse(status_code=404, content={"detail": "API yok"})
    index_path = os.path.join("dist", "index.html")
    if os.path.exists(index_path): return FileResponse(index_path)
    return JSONResponse(status_code=404, content={"detail": "SPA Yok"})