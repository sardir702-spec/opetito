import os
import zipfile

def zip_project():
    root_dir = r"c:\Users\User\Desktop\fas foood"
    zip_path = os.path.join(root_dir, "project_to_upload.zip")
    
    allowed_extensions = ['.py', '.json', '.html', '.css', '.js', '.md', '.txt', '.jpg', '.png']
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(root_dir):
            if '__pycache__' in root or '.git' in root:
                continue
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in allowed_extensions or file == "Procfile":
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, root_dir)
                    zipf.write(file_path, arcname)
                    print(f"Added {arcname}")
                    
    print(f"\n✅ ZIP fayl tayyor: {zip_path}")

if __name__ == "__main__":
    zip_project()
