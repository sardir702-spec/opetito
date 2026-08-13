import json
import os
from datetime import datetime

class Database:
    def __init__(self):
        self.db_file = "database_state.json"
        self.webapp_products_file = "products.json"
        self.load_data()

    def load_data(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    self.users = data.get("users", {})
                    self.products = data.get("products", [])
                    self.orders = data.get("orders", [])
                    self.carts = data.get("carts", {})
                    self.admins = data.get("admins", [])
                    self.couriers = data.get("couriers", [])
                    self.admin_contact = data.get("admin_contact", {"name": "Fast Food Admin", "phone": "+998 90 123 45 67", "username": "@admin"})
                    self.categories = data.get("categories", ["🍔 Burgerlar", "🌯 Lavashlar", "🥤 Ichimliklar", "🍟 Sneklar", "🍰 Shirinliklar"])
                    self.admin_accounts = data.get("admin_accounts", [{"login": "admin", "password": "123", "name": "Asosiy Admin"}])
                    self.admin_sessions = data.get("admin_sessions", {})
                except:
                    self._init_default()
        else:
            self._init_default()
        self.export_webapp_products()

    def _init_default(self):
        self.users = {}
        self.products = [
            {"id": 1, "name": "Burger", "category": "Burgerlar", "description": "Mazali mol go'shtidan", "price": 25000, "is_active": 1, "emoji": "🍔", "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=500&q=80"},
            {"id": 2, "name": "Cheeseburger", "category": "Burgerlar", "description": "Ikki hissa pishloqli", "price": 28000, "is_active": 1, "emoji": "🍔", "image": "https://images.unsplash.com/photo-1586190848861-99aa4a171e90?auto=format&fit=crop&w=500&q=80"},
            {"id": 3, "name": "Lavash klassik", "category": "Lavashlar", "description": "Tovuq go'shti bilan", "price": 23000, "is_active": 1, "emoji": "🌯", "image": "https://images.unsplash.com/photo-1626804475297-41609ea26daeb?auto=format&fit=crop&w=500&q=80"},
            {"id": 4, "name": "Lavash special", "category": "Lavashlar", "description": "Mol go'shti bilan", "price": 26000, "is_active": 1, "emoji": "🌯", "image": "https://images.unsplash.com/photo-1626804475297-41609ea26daeb?auto=format&fit=crop&w=500&q=80"},
            {"id": 5, "name": "Kola 0.5", "category": "Ichimliklar", "description": "Muzdek Coca-Cola", "price": 7000, "is_active": 1, "emoji": "🥤", "image": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?auto=format&fit=crop&w=500&q=80"}
        ]
        self.orders = []
        self.carts = {}
        self.admins = []
        self.couriers = []
        self.admin_contact = {"name": "Fast Food Admin", "phone": "+998 90 123 45 67", "username": "@admin"}
        self.categories = ["🍔 Burgerlar", "🌯 Lavashlar", "🥤 Ichimliklar", "🍟 Sneklar", "🍰 Shirinliklar"]
        self.admin_accounts = [{"login": "admin", "password": "123", "name": "Asosiy Admin"}]
        self.admin_sessions = {}
        self.save_data()

    def save_data(self):
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump({
                "users": getattr(self, 'users', {}),
                "products": getattr(self, 'products', []),
                "orders": getattr(self, 'orders', []),
                "carts": getattr(self, 'carts', {}),
                "admins": getattr(self, 'admins', []),
                "couriers": getattr(self, 'couriers', []),
                "admin_contact": getattr(self, 'admin_contact', {"name": "Fast Food Admin", "phone": "+998 90 123 45 67", "username": "@admin"}),
                "categories": getattr(self, 'categories', ["🍔 Burgerlar", "🌯 Lavashlar", "🥤 Ichimliklar", "🍟 Sneklar", "🍰 Shirinliklar"]),
                "admin_accounts": getattr(self, 'admin_accounts', [{"login": "admin", "password": "123", "name": "Asosiy Admin"}]),
                "admin_sessions": getattr(self, 'admin_sessions', {})
            }, f, ensure_ascii=False, indent=4)

    def export_webapp_products(self):
        active_products = [p for p in self.products if p.get('is_active', 1)]
        cats = getattr(self, 'categories', ["🍔 Burgerlar", "🌯 Lavashlar", "🥤 Ichimliklar", "🍟 Sneklar", "🍰 Shirinliklar"])
        data_obj = {
            "categories": cats,
            "products": active_products
        }
        
        dir_name = os.path.dirname(self.webapp_products_file)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        
        with open(self.webapp_products_file, 'w', encoding='utf-8') as f:
            json.dump(data_obj, f, ensure_ascii=False, indent=4)

    async def connect(self):
        print("JSON bazasi ishga tushdi")

    async def close(self):
        self.save_data()

    async def add_user(self, telegram_id, fullname, phone=None, lang="uz"):
        telegram_id_str = str(telegram_id)
        if telegram_id_str not in self.users:
            self.users[telegram_id_str] = {
                "id": len(self.users) + 1,
                "telegram_id": telegram_id,
                "fullname": fullname,
                "phone": phone,
                "lang": lang,
                "registered_at": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            self.save_data()

    async def set_user_lang(self, telegram_id, lang):
        telegram_id_str = str(telegram_id)
        if telegram_id_str in self.users:
            self.users[telegram_id_str]['lang'] = lang
            self.save_data()

    async def get_user(self, telegram_id):
        return self.users.get(str(telegram_id))
        
    async def get_all_users(self):
        return list(self.users.values())

    async def add_admin(self, admin_id):
        if admin_id not in self.admins:
            self.admins.append(admin_id)
            self.save_data()

    async def get_admins(self):
        return self.admins
        
    async def get_admin_contact(self):
        return getattr(self, 'admin_contact', {"name": "Fast Food Admin", "phone": "+998 90 123 45 67", "username": "@admin"})
        
    async def update_admin_contact(self, name, phone, username):
        self.admin_contact = {"name": name, "phone": phone, "username": username}
        self.save_data()
        
    async def get_categories(self):
        return getattr(self, 'categories', ["🍔 Burgerlar", "🌯 Lavashlar", "🥤 Ichimliklar", "🍟 Sneklar", "🍰 Shirinliklar"])
        
    async def add_category(self, cat):
        if cat not in self.categories:
            self.categories.append(cat)
            self.save_data()
            
    async def remove_category(self, cat):
        if cat in self.categories:
            self.categories.remove(cat)
            self.save_data()
            self.export_webapp_products()

    async def get_admin_accounts(self):
        return getattr(self, 'admin_accounts', [])
        
    async def add_admin_account(self, login, password, name):
        self.admin_accounts.append({"login": login, "password": password, "name": name})
        self.save_data()
        
    async def remove_admin_account(self, login):
        self.admin_accounts = [a for a in self.admin_accounts if a['login'] != login]
        self.save_data()
        
    async def set_admin_session(self, user_id, login):
        if not hasattr(self, 'admin_sessions'): self.admin_sessions = {}
        self.admin_sessions[str(user_id)] = login
        if user_id not in self.admins:
            self.admins.append(user_id)
        self.save_data()
        
    async def get_admin_session(self, user_id):
        if not hasattr(self, 'admin_sessions'): return "Noma'lum Admin"
        return self.admin_sessions.get(str(user_id), "Asosiy Admin")

    async def get_products(self):
        return [p for p in self.products if p.get('is_active', 1)]

    async def add_product(self, name, description, price, category="Boshqa", image=""):
        product_id = 1
        if self.products:
            product_id = max(p['id'] for p in self.products) + 1
            
        self.products.append({
            "id": product_id,
            "name": name,
            "category": category,
            "description": description,
            "price": price,
            "is_active": 1,
            "emoji": "🍽",
            "image": image if image else "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=500&q=80"
        })
        self.save_data()
        self.export_webapp_products()
        
    async def toggle_product(self, product_id):
        for p in self.products:
            if p["id"] == product_id:
                p["is_active"] = 0 if p.get("is_active", 1) == 1 else 1
                break
        self.save_data()
        self.export_webapp_products()

    async def edit_product(self, product_id, new_price, new_image, new_name=None, new_desc=None):
        for p in self.products:
            if p["id"] == product_id:
                p["price"] = new_price
                if new_image:
                    p["image"] = new_image
                if new_name:
                    p["name"] = new_name
                if new_desc:
                    p["description"] = new_desc
        self.save_data()
        self.export_webapp_products()
        
    async def delete_product(self, product_id):
        self.products = [p for p in self.products if p["id"] != product_id]
        self.save_data()
        self.export_webapp_products()

    async def get_couriers(self):
        return getattr(self, 'couriers', [])

    async def add_courier(self, telegram_id, fullname, phone):
        if not hasattr(self, 'couriers'): self.couriers = []
        c_id = 1 if not self.couriers else max(c['id'] for c in self.couriers) + 1
        new_courier = {
            "id": c_id,
            "telegram_id": telegram_id,
            "fullname": fullname,
            "phone": phone,
            "registered_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.couriers.append(new_courier)
        self.save_data()
        return new_courier

    async def delete_courier(self, courier_id):
        if hasattr(self, 'couriers'):
            self.couriers = [c for c in self.couriers if c['id'] != courier_id]
            self.save_data()

    async def create_order(self, user_id, total_price, location, phone, items, order_type="Oddiy", room_table=None, comment=""):
        order_id = 1
        if self.orders:
            order_id = max(o['id'] for o in self.orders) + 1
            
        self.orders.append({
            "id": order_id,
            "user_id": user_id,
            "total_price": total_price,
            "location": location,
            "phone": phone,
            "status": "Yangi",
            "items": items,
            "order_type": order_type,
            "room_table": room_table,
            "comment": comment,
            "courier_id": None,
            "created_at": datetime.now().strftime('%d.%m.%Y %H:%M')
        })
        self.save_data()
        return order_id

    async def get_user_orders(self, user_id, limit=10):
        user_orders = [o for o in self.orders if o["user_id"] == user_id]
        return list(reversed(user_orders))[:limit]
        
    async def get_user_stats(self, user_id):
        user_orders = [o for o in self.orders if o["user_id"] == user_id and o["status"] != "Bekor qilingan"]
        total_spent = sum(o["total_price"] for o in user_orders)
        return {
            "order_count": len(user_orders),
            "total_spent": total_spent
        }

    async def get_dashboard_stats(self):
        today_str = datetime.now().strftime('%d.%m.%Y')
        today_orders = [o for o in self.orders if o.get('created_at', '').startswith(today_str)]
        
        total_revenue = sum(o.get('total_price', 0) for o in self.orders if o.get('status') not in ["Bekor qilingan", "Archivlangan"])
        today_revenue = sum(o.get('total_price', 0) for o in today_orders if o.get('status') not in ["Bekor qilingan", "Archivlangan"])
        
        return {
            "products": len([p for p in getattr(self, 'products', []) if p.get('is_active', 1)]),
            "orders": len(getattr(self, 'orders', [])),
            "users": len(getattr(self, 'users', {})),
            "today_orders": len(today_orders),
            "total_revenue": total_revenue,
            "today_revenue": today_revenue
        }

    async def update_order_status(self, order_id, status):
         for o in self.orders:
             if o["id"] == order_id:
                 o["status"] = status
                 break
         self.save_data()

    async def reset_revenue(self):
        for o in self.orders:
            if o['status'] not in ["Bekor qilingan"]:
                o['status'] = "Archivlangan"
        self.save_data()
