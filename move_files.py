import os
import shutil

root_dir = r"c:\Users\User\Desktop\fas foood"
webapp_dir = os.path.join(root_dir, "webapp")
php_bot_dir = os.path.join(root_dir, "php-bot")

def move_contents(src_dir, dest_dir):
    if not os.path.exists(src_dir):
        return
    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)
        
        if os.path.exists(dest_path):
            if os.path.isdir(dest_path):
                # Merge directories (like images/)
                move_contents(src_path, dest_path)
                try:
                    os.rmdir(src_path)
                except:
                    pass
                continue
            else:
                print(f"Skipping {item} because it already exists in root.")
                continue
                
        shutil.move(src_path, dest_path)
    
    # Try to remove the now empty directory
    try:
        os.rmdir(src_dir)
        print(f"Removed empty directory: {src_dir}")
    except OSError:
        pass

print("Moving webapp files to root...")
move_contents(webapp_dir, root_dir)

print("✅ Barcha WebApp fayllari 1 ta papkaga (root) ko'chirildi! Endi 'php-bot' papkasini o'zingiz o'chirib tashlashingiz mumkin.")
