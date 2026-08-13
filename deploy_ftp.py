import ftplib
import os

FTP_HOST = "31.184.242.14" # Yoki "sdr.yangi-jadid.uz"
FTP_USER = "s0065"
FTP_PASS = "W#RdX9a6UhBr"

def upload_dir(ftp, local_dir, remote_dir):
    try:
        ftp.mkd(remote_dir)
    except:
        pass
    
    ftp.cwd(remote_dir)
    
    for item in os.listdir(local_dir):
        local_path = os.path.join(local_dir, item)
        if os.path.isfile(local_path):
            print(f"Uploading {local_path} to {item}...")
            with open(local_path, 'rb') as f:
                ftp.storbinary(f'STOR {item}', f)
        elif os.path.isdir(local_path):
            print(f"Creating directory {item}...")
            upload_dir(ftp, local_path, item)
            ftp.cwd("..")

def main():
    print("Connecting to FTP...")
    ftp = ftplib.FTP()
    ftp.connect(FTP_HOST, 21, timeout=30)
    ftp.login(FTP_USER, FTP_PASS)
    ftp.set_pasv(True)
    
    print("Connected. Uploading files...")
    ftp.cwd("/www/sdr.yangi-jadid.uz")
    
    root_dir = r"c:\Users\User\Desktop\fas foood"
    
    # Upload PHP va asosiy Python fayllarni
    allowed_extensions = ['.py', '.json', '.html', '.css', '.js', '.md', '.txt']
    for item in os.listdir(root_dir):
        local_path = os.path.join(root_dir, item)
        if os.path.isfile(local_path):
            ext = os.path.splitext(item)[1]
            if ext in allowed_extensions or item == "Procfile":
                print(f"Uploading {item}...")
                with open(local_path, 'rb') as f:
                    ftp.storbinary(f'STOR {item}', f)
                
    # Upload images
    images_dir = os.path.join(root_dir, 'images')
    if os.path.exists(images_dir):
        print("Uploading images directory...")
        upload_dir(ftp, images_dir, "images")
            
    print("Upload complete! Barcha yangi kodlar serverga muvaffaqiyatli yuklandi.")
    ftp.quit()

if __name__ == "__main__":
    main()
