import ftplib
import os

FTP_HOST = "ftpupload.net"
FTP_USER = "if0_42129168"
FTP_PASS = "2NEBtsBiGlAwB"

def upload_dir(ftp, local_dir, remote_dir):
    try:
        ftp.mkd(remote_dir)
    except:
        pass
    
    ftp.cwd(remote_dir)
    
    for item in os.listdir(local_dir):
        local_path = os.path.join(local_dir, item)
        if os.path.isfile(local_path):
            print(f"Yuklanmoqda: {item} ...")
            with open(local_path, 'rb') as f:
                ftp.storbinary(f'STOR {item}', f)
        elif os.path.isdir(local_path):
            upload_dir(ftp, local_path, item)
            ftp.cwd("..")

def sync_webapp():
    try:
        ftp = ftplib.FTP()
        ftp.connect(FTP_HOST, 21, timeout=30)
        ftp.login(FTP_USER, FTP_PASS)
        ftp.set_pasv(True)
        
        ftp.cwd("/htdocs/webapp")
        
        # Upload products.json
        local_products = "products.json"
        if os.path.exists(local_products):
            with open(local_products, 'rb') as f:
                ftp.storbinary('STOR products.json', f)
                
        # Upload images
        local_images = "images"
        if os.path.exists(local_images):
            print("Rasmlar yuklanmoqda...")
            upload_dir(ftp, local_images, "images")
            
        ftp.quit()
        print("✅ Barcha o'zgarishlar va rasmlar serverga muvaffaqiyatli yuklandi!")
        return True
    except Exception as e:
        print(f"❌ FTP Error: {e}")
        return False

if __name__ == "__main__":
    sync_webapp()
