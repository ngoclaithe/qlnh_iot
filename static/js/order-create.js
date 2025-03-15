document.addEventListener('DOMContentLoaded', function() {
    const menuItems = document.querySelectorAll('.menu-item');
    const searchInput = document.getElementById('search-menu');
    const cartItemsContainer = document.getElementById('cart-items');
    const totalAmountElement = document.getElementById('total-amount');
    let cartItems = [];
    
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        
        menuItems.forEach(item => {
            const itemName = item.querySelector('.menu-item-name').textContent.toLowerCase();
            const itemDesc = item.querySelector('.menu-item-description').textContent.toLowerCase();
            
            if (itemName.includes(searchTerm) || itemDesc.includes(searchTerm)) {
                item.style.display = 'flex';
            } else {
                item.style.display = 'none';
            }
        });
    });
    
    document.querySelectorAll('.add-item-btn').forEach(button => {
        button.addEventListener('click', function() {
            const menuItem = this.closest('.menu-item');
            const itemId = menuItem.dataset.id;
            const itemName = menuItem.querySelector('.menu-item-name').textContent;
            const itemPrice = parseFloat(menuItem.querySelector('.menu-item-price').dataset.price);
            
            const existingItem = cartItems.find(item => item.id === itemId);
            
            if (existingItem) {
                existingItem.quantity += 1;
            } else {
                cartItems.push({
                    id: itemId,
                    name: itemName,
                    price: itemPrice,
                    quantity: 1,
                    note: ''
                });
            }
            
            updateCart();
        });
    });
    
    function updateCart() {
        if (cartItems.length === 0) {
            cartItemsContainer.innerHTML = '<div class="empty-cart">Giỏ hàng trống</div>';
            totalAmountElement.textContent = '0 VNĐ';
            document.getElementById('total-amount-input').value = 0;
            return;
        }
        
        cartItemsContainer.innerHTML = '';
        let total = 0;
        
        cartItems.forEach(item => {
            const itemTotal = item.price * item.quantity;
            total += itemTotal;
            
            const cartItemElement = document.createElement('div');
            cartItemElement.className = 'cart-item';
            cartItemElement.innerHTML = `
                <div class="cart-item-details">
                    <div class="cart-item-name">${item.name}</div>
                    <div>${item.price.toLocaleString()} VNĐ x ${item.quantity}</div>
                    <input type="text" class="note-input" placeholder="Ghi chú" value="${item.note}" data-id="${item.id}">
                    <input type="hidden" name="item_ids[]" value="${item.id}">
                    <input type="hidden" name="quantities[]" value="${item.quantity}">
                    <input type="hidden" name="notes[]" value="${item.note}">
                </div>
                <div class="cart-item-actions">
                    <input type="number" class="quantity-input" value="${item.quantity}" min="1" data-id="${item.id}">
                    <button type="button" class="remove-item-btn" data-id="${item.id}">Xóa</button>
                </div>
            `;
            
            cartItemsContainer.appendChild(cartItemElement);
        });
        
        totalAmountElement.textContent = total.toLocaleString() + ' VNĐ';
        document.getElementById('total-amount-input').value = total;
        
        setupCartEventListeners();
    }
    
    function setupCartEventListeners() {
        
        document.querySelectorAll('.quantity-input').forEach(input => {
            input.addEventListener('change', function() {
                const itemId = this.dataset.id;
                const newQuantity = parseInt(this.value);
                
                if (newQuantity < 1) {
                    this.value = 1;
                    return;
                }
                
                const cartItem = cartItems.find(item => item.id === itemId);
                if (cartItem) {
                    cartItem.quantity = newQuantity;
                    updateCart();
                }
            });
        });
        
        document.querySelectorAll('.remove-item-btn').forEach(button => {
            button.addEventListener('click', function() {
                const itemId = this.dataset.id;
                cartItems = cartItems.filter(item => item.id !== itemId);
                updateCart();
            });
        });
        
        document.querySelectorAll('.note-input').forEach(input => {
            input.addEventListener('input', function() {
                const itemId = this.dataset.id;
                const note = this.value;
                
                const cartItem = cartItems.find(item => item.id === itemId);
                if (cartItem) {
                    cartItem.note = note;
                    
                    const noteInput = document.querySelector(`input[name="notes[]"][value="${cartItem.note}"]`);
                    if (noteInput) {
                        noteInput.value = note;
                    }
                }
            });
        });
    }
    
    updateCart();
    
    document.querySelectorAll('.category-btn').forEach(button => {
        button.addEventListener('click', function() {
            const category = this.dataset.category;
            
            document.querySelectorAll('.category-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            this.classList.add('active');
            
            menuItems.forEach(item => {
                if (category === 'all' || item.dataset.category === category) {
                    item.style.display = 'flex';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });
    
    document.querySelector('form').addEventListener('submit', function(event) {
        if (cartItems.length === 0) {
            event.preventDefault();
            alert('Vui lòng thêm ít nhất một món vào đơn hàng!');
        }
    });
    
    document.querySelector('.search-btn').addEventListener('click', function() {
        const searchTerm = searchInput.value.toLowerCase();
        
        menuItems.forEach(item => {
            const itemName = item.querySelector('.menu-item-name').textContent.toLowerCase();
            const itemDesc = item.querySelector('.menu-item-description').textContent.toLowerCase();
            
            if (itemName.includes(searchTerm) || itemDesc.includes(searchTerm)) {
                item.style.display = 'flex';
            } else {
                item.style.display = 'none';
            }
        });
    });
});