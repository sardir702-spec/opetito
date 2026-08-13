let tg = window.Telegram.WebApp;
tg.expand();
tg.ready();

// Yangi zamonaviy dizayn ranglari
tg.setHeaderColor('#F8F9FA');
tg.setBackgroundColor('#F8F9FA');

const urlParams = new URLSearchParams(window.location.search);
const lang = urlParams.get('lang') || 'uz';
const user_id = urlParams.get('user_id');
const isTelegramWebApp = window.Telegram && window.Telegram.WebApp && window.Telegram.WebApp.initData !== "";

const t = {
    uz: {
        all: "Barchasi",
        add: "Qo'shish",
        checkout: "Savatga o'tish",
        sum: "so'm",
        loading_error: "Maxsulotlarni yuklashda xatolik",
        banner_title: "🔥 Olovli Ta'm",
        banner_subtitle: "Siz izlagan maza va sifat!",
        contact_admin: "Admin bilan aloqa",
        search: "Mahsulot qidirish..."
    },
    ru: {
        all: "Все",
        add: "Добавить",
        checkout: "Перейти в корзину",
        sum: "сум",
        loading_error: "Ошибка при загрузке товаров",
        banner_title: "🔥 Огненный Вкус",
        banner_subtitle: "Тот самый вкус и качество!",
        contact_admin: "Связь с админом",
        search: "Поиск товаров..."
    },
    en: {
        all: "All",
        add: "Add",
        checkout: "Go to cart",
        sum: "sum",
        loading_error: "Error loading products",
        banner_title: "🔥 Fiery Taste",
        banner_subtitle: "The taste and quality you seek!",
        contact_admin: "Contact Admin",
        search: "Search products..."
    }
};

function getText(key) {
    return t[lang][key] || t['uz'][key];
}

document.getElementById('banner_title').innerText = getText('banner_title');
document.getElementById('banner_subtitle').innerText = getText('banner_subtitle');
const adminBtn = document.getElementById('contact_admin_btn');
if (adminBtn) {
    adminBtn.innerHTML = `<i class="fa-solid fa-shield-halved"></i> ${getText('contact_admin')}`;
}
const searchInput = document.getElementById('searchInput');
if (searchInput) {
    searchInput.placeholder = getText('search');
}

let products = [];
let cart = {};
let currentCategory = getText('all');

async function loadProducts() {
    try {
        let res = await fetch(`products.json?t=${new Date().getTime()}`);
        let data = await res.json();
        products = data.products || [];
        window.allCategories = data.categories || [];
        renderTabs();
        renderProducts();
    } catch(e) {
        console.error(getText('loading_error'), e);
    }
}

function formatPrice(price) {
    return price.toLocaleString('ru-RU');
}

function renderTabs() {
    const tabsContainer = document.getElementById("category-tabs");
    if(!tabsContainer) return;
    
    tabsContainer.innerHTML = `<div class="tab ${currentCategory === getText('all') ? 'active' : ''}" onclick="filterCategory('${getText('all')}')">${getText('all')}</div>`;
    
    let categories = window.allCategories || [...new Set(products.map(p => p.category))];
    categories.forEach(cat => {
        let activeClass = currentCategory === cat ? 'active' : '';
        tabsContainer.innerHTML += `<div class="tab ${activeClass}" onclick="filterCategory('${cat}')">${cat}</div>`;
    });
}

function filterCategory(category) {
    currentCategory = category;
    tg.HapticFeedback.selectionChanged();
    renderTabs();
    renderProducts();
}

let searchQuery = "";

function searchProducts() {
    searchQuery = document.getElementById('searchInput').value.toLowerCase();
    renderProducts();
}

function renderProducts() {
    const container = document.getElementById("products");
    container.innerHTML = "";
    
    let filtered = products.filter(p => {
        let matchCategory = (currentCategory === getText('all') || p.category === currentCategory);
        let matchSearch = p.name.toLowerCase().includes(searchQuery);
        return matchCategory && matchSearch;
    });
    
    filtered.forEach(p => {
        let qty = cart[p.id] || 0;
        let card = document.createElement('div');
        card.className = "card";
        
        let actionsHtml = qty === 0 
            ? `<button class="btn" onclick="add(${p.id})"><i class="fa-solid fa-bag-shopping"></i> ${getText('add')}</button>`
            : `<div class="controls">
                 <button class="btn-icon" onclick="remove(${p.id})">-</button>
                 <span class="qty">${qty}</span>
                 <button class="btn-icon" onclick="add(${p.id})">+</button>
               </div>`;
               
        card.innerHTML = `
            <i class="fa-regular fa-heart card-heart"></i>
            <div class="card-img-container" onclick="openModal('${p.image}')">
                <img src="${p.image}" alt="${p.name}">
            </div>
            <div class="card-info">
                <h3>${p.name}</h3>
                <p>${p.description}</p>
                <span class="price">${formatPrice(p.price)} ${getText('sum')}</span>
            </div>
            <div class="actions" id="actions-${p.id}">${actionsHtml}</div>
        `;
        container.appendChild(card);
    });
    
    updateMainButton();
}

function getActionsHtml(id, qty) {
    let p = products.find(x => x.id == id);
    if(qty === 0) {
        return `<button class="btn" onclick="add(${p.id})"><i class="fa-solid fa-bag-shopping"></i> ${getText('add')}</button>`;
    } else {
        return `<div class="controls">
                 <button class="btn-icon" onclick="remove(${p.id})">-</button>
                 <span class="qty">${qty}</span>
                 <button class="btn-icon" onclick="add(${p.id})">+</button>
               </div>`;
    }
}

function updateProductUI(id) {
    let qty = cart[id] || 0;
    let actionsContainer = document.getElementById(`actions-${id}`);
    if(actionsContainer) {
        actionsContainer.innerHTML = getActionsHtml(id, qty);
    }
    updateMainButton();
}

function add(id) {
    if(!cart[id]) cart[id] = 0;
    cart[id]++;
    tg.HapticFeedback.impactOccurred('light');
    updateProductUI(id);
}

function remove(id) {
    if(cart[id]) {
        cart[id]--;
        if(cart[id] === 0) delete cart[id];
        tg.HapticFeedback.impactOccurred('light');
    }
    updateProductUI(id);
}

function updateMainButton() {
    let total = 0;
    let count = 0;
    for(let id in cart) {
        let p = products.find(x => x.id == parseInt(id));
        total += p.price * cart[id];
        count += cart[id];
    }
    
    let btnText = `${getText('checkout')} (${formatPrice(total)} ${getText('sum')})`;
    
    if(count > 0) {
        if(isTelegramWebApp) {
            tg.MainButton.text = btnText;
            tg.MainButton.color = '#FF8A00';
            tg.MainButton.show();
        } else {
            const bar = document.getElementById('web-checkout-bar');
            const btn = document.getElementById('web-checkout-btn');
            if(bar && btn) {
                bar.style.display = 'flex';
                btn.innerText = btnText;
            }
        }
    } else {
        if(isTelegramWebApp) {
            tg.MainButton.hide();
        } else {
            const bar = document.getElementById('web-checkout-bar');
            if(bar) bar.style.display = 'none';
        }
    }
}

function handleCheckout() {
    let orderItems = [];
    for(let id in cart) {
        let p = products.find(x => x.id == parseInt(id));
        orderItems.push({ id: p.id, name: p.name, price: p.price, quantity: cart[id] });
    }
    
    if (!user_id) {
        alert("Telegram User ID topilmadi. Iltimos bot orqali kiring.");
        return;
    }
    
    let btn = document.getElementById('web-checkout-btn');
    let oldText = "";
    if (isTelegramWebApp) {
        tg.MainButton.text = "⏳ Yuklanmoqda...";
    } else {
        oldText = btn.innerText;
        btn.innerText = "⏳ Yuklanmoqda...";
        btn.disabled = true;
    }
    
    fetch('/api/checkout', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ user_id: parseInt(user_id), items: orderItems })
    })
    .then(res => res.json())
    .then(data => {
        if(data.status === 'ok') {
            if (isTelegramWebApp) {
                tg.close();
            } else {
                alert("✅ Buyurtma qabul qilindi! Endi botda davom ettiramiz.");
                window.location.href = "https://t.me/snovb_bot";
            }
        } else {
            alert("Xatolik: " + (data.message || ''));
        }
    })
    .catch(e => {
        alert("Xatolik yuz berdi: " + e.message);
    })
    .finally(() => {
        if (isTelegramWebApp) {
            let total = 0;
            for(let id in cart) {
                let p = products.find(x => x.id == parseInt(id));
                total += p.price * cart[id];
            }
            tg.MainButton.text = `${getText('checkout')} - ${total.toLocaleString('ru-RU')} ${getText('sum')}`;
        } else {
            btn.innerText = oldText;
            btn.disabled = false;
        }
    });
}

if(isTelegramWebApp) {
    tg.MainButton.onClick(handleCheckout);
} else {
    document.getElementById('web-checkout-btn').addEventListener('click', handleCheckout);
}

function openModal(imgSrc) {
    const modal = document.getElementById('image-modal');
    const img = document.getElementById('zoomed-img');
    if (modal && img) {
        img.src = imgSrc;
        modal.classList.add('show');
    }
}

function closeModal() {
    const modal = document.getElementById('image-modal');
    if (modal) {
        modal.classList.remove('show');
    }
}

loadProducts();
