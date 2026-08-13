# "Fast Food" Telegram Bot va WebApp Loyihasi Uchun Texnik Zadacha (TZ)

## 1. Loyiha haqida umumiy ma'lumot
**Loyiha nomi:** Fast Food Bot & WebApp
**Maqsad:** Mijozlarga kafe ichida, binodagi xonalarda yoki masofaviy (uyga) fast-food mahsulotlarini buyurtma qilishni osonlashtiruvchi Telegram bot va ichki WebApp (Mini App) tizimini ishlab chiqish va boshqarish.
**Asosiy platformalar:** 
- Telegram Bot (foydalanuvchi, kuryer va admin interfeyslari uchun)
- Telegram WebApp (HTML/CSS/JS dagi qulay va vizual menyu orqali savatga mahsulot qo'shish uchun)
- Lokal JSON Ma'lumotlar bazasi (`database_state.json`)

---

## 2. Loyiha arxitekturasi va fayllar tuzilmasi
Loyiha asosan Python dagi **Aiogram 3.x** kutubxonasida qurilgan va quyidagi qismlardan iborat:
- `main.py` — Botning asosiy boshqaruv mantiqi, barcha xabar (message) va tugmalar (callback_query) handleri joylashgan.
- `database.py` — JSON bazaga ulanish, CRUD (yaratish, o'qish, yangilash, o'chirish) amaliyotlari va WebApp uchun `products.json` ni eksport qilish funksiyalari.
- `config.py` — Loyiha sozlamalari (Tokenlar, Adminlar IDsi, parollar).
- `webapp/` — Telegram ichida ochiladigan Mini WebApp uchun frontend (HTML, JS, CSS).

---

## 3. Ma'lumotlar bazasi (Database) tuzilmasi
Ma'lumotlar bazasi sifatida lokal JSON fayl (`database_state.json`) ishlatiladi. Unda quyidagi jadvallar/obyektlar yig'iladi:
- **`users`**: Ro'yxatdan o'tgan foydalanuvchilar (ID, ism, telefon).
- **`products`**: Mahsulotlar ro'yxati (ID, nomi, kategoriyasi, ta'rifi, narxi, rasmi, aktiv/noaktiv holati).
- **`categories`**: Mahsulot toifalari (Burgerlar, Lavashlar, Ichimliklar va h.k).
- **`orders`**: Buyurtmalar tarixi va holati (Kutish, Tayyorlanmoqda, Bekor qilingan va h.k).
- **`admins` & `admin_accounts`**: Tizim adminlari (Login, Parol, Ismi) va ularning sessiyalari.
- **`couriers`**: Yetkazib beruvchilar (Kuryerlar) ro'yxati (ID, Telegram ID, ism, telefon).

---

## 4. Tizimdagi rollar (Foydalanuvchilar qatlami)

Loyiha 3 xil foydalanuvchi qatlamiga bo'lingan:
1. **Mijoz (Oddiy foydalanuvchi)**
2. **Admin (Tizim boshqaruvchisi)**
3. **Kuryer (Yetkazib beruvchi)**

---

## 5. Modullar va ularning ishlash jarayonlari (Flow)

### 5.1. Mijoz (Foydalanuvchi) Moduli
Botga kirgan oddiy mijoz uchun imkoniyatlar:
- **/start komandasi:** Foydalanuvchi botga kiradi, bazaga saqlanadi. Asosiy menyu ko'rinadi.
- **Buyurtma turi tanlash:** Mijozga 2 ta asosiy yo'nalish taklif qilinadi:
  1. `🏢 Kafe + Bino`: Kafeda ekanligi yoki binodagi xonalarga buyurtma berishi. Bunda "🚪 Xona" yoki "🍽 Kafe" raqami so'raladi.
  2. `🛵 Masofaviy`: Uyga yetkazib berish. Manzil keyinroq so'raladi.
- **WebApp Menyu:** Joylashuv tanlangach, mijozga WebApp ochiladigan "🍔 Menyu" tugmasi taqdim etiladi. Mijoz bu yerda o'ziga yoqgan taomlarni savatga qo'shadi va "Checkout" (Sotib olish) ni bosadi.
- **Telefon va Manzil tasdiqlash:** WebApp yopilgach, bot qabul qilingan tovarlarni hisoblaydi va mijozdan Kontaktini tasdiqlashni, so'ngra (agar masofaviy bo'lsa) Geolokatsiyasini (Manzilini) va qo'shimcha izohni so'raydi.
- **Buyurtmani yakunlash:** Barcha ma'lumot kiritilgach, buyurtma bazaga yoziladi va **Adminlarga** tasdiqlash uchun yuboriladi.
- **Kabinetim:** Mijoz o'zining jami xaridlari sonini, qancha pul sarflaganini hamda oxirgi 5 ta buyurtmasining joriy holatini ko'rishi mumkin.

### 5.2. Kuryer Moduli
Kuryerlar tizimga maxsus parol orqali qabul qilinadi.
- **Ro'yxatdan o'tish:** Mijoz asosiy menyudan "📦 Kuryer bo'lish" ni tanlab, maxfiy parolni (`1155`) kiritadi. Agar to'g'ri bo'lsa, ism-familiyasi va raqamini kiritib Kuryerlar ro'yxatiga (ID bilan) tushadi.
- **Buyurtma qabul qilish:** Admin masofaviy buyurtmani kuryerga yuborganda, Kuryerga lokatsiya, mijozning raqami, mahsulotlar ro'yxati va umumiy summa kelib tushadi. U shu ma'lumotlar asosida taomni yetkazib beradi.

### 5.3. Admin Moduli (Boshqaruv Paneli)
Admin paneli maxsus komanda (`/admin`) orqali ochiladi. Agar ID ro'yxatda bo'lmasa, maxsus Login va Parol so'raladi (Tizimda Superadmin va qo'shimcha adminlar bo'lishi mumkin).
Admin imkoniyatlari:
1. **Yangi Buyurtmalarni tasdiqlash/bekor qilish:** 
   - Yangi buyurtma admin botiga kelganda `✅ Qabul qilish` va `❌ Bekor qilish` tugmalari chiqadi. 
   - Agar Qabul qilsa va u "Masofaviy" bo'lsa, adminga qo'shimcha `🚚 Kuryerga berish` tugmasi chiqadi va admin Kuryer ID sini kiritish orqali buyurtmani tayinlashi mumkin.
2. **Kategoriyalar va Menyuni boshqarish:** 
   - `🏷 Kategoriyalar`: Yangi kategoriya qo'shish yoki o'chirish.
   - `➕ MENU qo'shish`: WebApp ga chiqadigan taomni qo'shish (Nomi, kategoriyasi, rasmi, narxi). Baza bu o'zgarishni avtomat `webapp/products.json` ga yozadi.
   - `📝 O'chirish / Tahrirlash`: Mahsulotlarni faol / nofaol qilib qo'yish.
3. **Statistika va Xodimlar:**
   - `👥 Foydalanuvchilar`: Barcha mijozlarni ko'rish.
   - `🚚 Kuryerlar ma'lumotlari`: Kuryerlarni ko'rish va ularni tizimdan haydash (o'chirish).
   - `👨‍💻 Adminlar`: Qo'shimcha admin login/parollarini yaratish va boshqarish.
4. **Tizim sozlamalari:**
   - `⚙️ Aloqa sozlamalari`: Mijozlarga ko'rinadigan admin ism, telefon va username ma'lumotlarini o'zgartirish.
   - `📢 Reklama tarqatish`: Barcha bot foydalanuvchilariga xabar yuborish.
   - `🔄 Balansni nolga tushirish`: Jami daromadlarni arxivga o'tkazish (yangi kun / oy hisobi uchun).

---

## 6. Texnik qadamlar va jarayonlar ketma-ketligi (FSM - Finite State Machine)
Bot foydalanuvchi ma'lumotlarini qadamba-qadam qabul qilish uchun **FSMContext** (Holatlar mashinasi) dan foydalanadi:
- `OrderFlow`: Xona/Stol raqamini kutish -> Telefon kutish -> Manzil kutish -> Izoh kutish.
- `CourierReg`: Parol kutish -> Ism kutish -> Telefon kutish.
- `AdminLogin`: Login kutish -> Parol kutish.
- `AddProduct`: Mahsulot nomi, turi, ta'rifi, narxi, rasmi kabilar ketma-ket kiritiladi.

## 7. WebApp Integratsiyasi jarayoni
1. Admin bot orqali MENU ga mahsulot qo'shadi.
2. `database.py` dagi `export_webapp_products()` funksiyasi ishga tushib, bazadagi mahsulotlarni `webapp/products.json` fayliga yozadi.
3. Mijoz botdagi `🍔 Menyu` tugmasini bosganda Telegram ichida HTML sahifa (WebApp) ochiladi.
4. WebApp dagi `app.js` fayli `products.json` ni o'qib, chiroyli dizaynda taomlarni ekranga chiqaradi.
5. Mijoz xarid tugatgach, JS kodi tanlangan narsalar va ularning sonini olib, `Telegram.WebApp.sendData()` orqali yana botga JSON formatda jo'natadi.
6. Bot u ma'lumotlarni qabul qilib olib savatni hisoblaydi va buyurtmani rasmiylashtiradi.
