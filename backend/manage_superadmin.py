import sys
from database import SessionLocal, UserDB

def main():
    db = SessionLocal()
    try:
        print("\n==================================================")
        print("👑 BONNACLOUD SUPER ADMIN YÖNETİM PANELİ (CLI) 👑")
        print("==================================================\n")
        
        users = db.query(UserDB).all()
        if not users:
            print("Sistemde kayıtlı kullanıcı bulunamadı.")
            return
        
        # Kullanıcıları listele
        print(f"{'ID':<5} | {'İsim':<25} | {'E-posta':<35} | {'Süper Admin mi?':<12}")
        print("-" * 85)
        for u in users:
            status = "EVET ✅" if u.is_superadmin else "HAYIR ❌"
            print(f"{u.id:<5} | {u.name or '-':<25} | {u.email:<35} | {status:<12}")
        
        print("\n" + "-" * 85)
        user_input = input("\nSüper Admin yetkisini değiştirmek (Açmak/Kapatmak) istediğiniz kullanıcının ID'sini yazın (Çıkış için Enter): ").strip()
        
        if not user_input:
            print("İşlem iptal edildi.")
            return
        
        try:
            user_id = int(user_input)
        except ValueError:
            print("Hata: Geçersiz bir sayısal ID girdiniz.")
            return
        
        target_user = db.query(UserDB).filter(UserDB.id == user_id).first()
        if not target_user:
            print(f"Hata: ID {user_id} olan bir kullanıcı bulunamadı.")
            return
        
        # Durumu tersine çevir (Toggle)
        target_user.is_superadmin = not target_user.is_superadmin
        
        # String tabanlı rol alanını eşitle
        if target_user.is_superadmin:
            target_user.role = "superadmin"
        else:
            if target_user.role_rel and target_user.role_rel.is_admin:
                target_user.role = "admin"
            else:
                target_user.role = "customer"

        db.commit()
        
        new_status = "SÜPER ADMİN YAPILDI ✅" if target_user.is_superadmin else "SÜPER ADMİN YETKİSİ ALINDI ❌"
        print(f"\nBaşarılı! {target_user.email} kullanıcısı {new_status}.\n")
        
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()