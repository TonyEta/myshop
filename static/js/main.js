document.addEventListener('DOMContentLoaded', function() {

    // // --- General logic for all pages (Login/Logout Simulation) ---
    // const loginForm = document.getElementById('login-form');
    // const logoutButton = document.getElementById('logout-button');
    // function checkLoginStatus() {
    //     if (localStorage.getItem('isLoggedIn') === 'true') {
    //         document.body.classList.add('user-logged-in');
    //     } else {
    //         document.body.classList.remove('user-logged-in');
    //     }
    // }
    // if (loginForm) {
    //     loginForm.addEventListener('submit', function(e) {
    //         e.preventDefault();
    //         localStorage.setItem('isLoggedIn', 'true');
    //         const nextUrl = new URLSearchParams(window.location.search).get('next');
    //         window.location.href = nextUrl || 'home.html';
    //     });
    // }
    // if (logoutButton) {
    //     logoutButton.addEventListener('click', function(e) {
    //         e.preventDefault();
    //         localStorage.removeItem('isLoggedIn');
    //         window.location.href = 'home.html';
    //     });
    // }
    // checkLoginStatus();


    // --- Logic for the Main Page (home.html) ---
    const homePageContent = document.querySelector('.main-content-grid');
    if (homePageContent) {
        // 1. Sort Options Logic
        const sortButtons = document.querySelectorAll('.sort-options .sort-button');
        sortButtons.forEach(button => {
            button.addEventListener('click', function() {
                sortButtons.forEach(btn => btn.classList.remove('active-sort'));
                this.classList.add('active-sort');
                applyFilters();
            });
        });

    const urlParams = new URLSearchParams(window.location.search);
    // Якщо в URL є хоча б якісь параметри (значить ми щось шукали або перейшли на іншу сторінку)
    if (urlParams.toString().length > 0) {
        // Знаходимо блок, де починаються фільтри та товари
        const productsSection = document.querySelector('.products-area');
        
        if (productsSection) {
            // Робимо невеличку затримку, щоб сторінка встигла відмалюватися
            setTimeout(() => {
                productsSection.scrollIntoView({ 
                    behavior: 'smooth', // Плавна анімація
                    block: 'start'      // Проскролити так, щоб верх блоку був зверху екрану
                });
            }, 100);
        }
    }

        // // 2. Pagination Logic
        // const paginationList = document.querySelector('.pagination-list');
        // if (paginationList) {
        //     const paginationLinks = paginationList.querySelectorAll('.pagination__link');
        //     paginationLinks.forEach(link => {
        //         link.addEventListener('click', function(event) {
        //             event.preventDefault();
        //             paginationLinks.forEach(lnk => lnk.classList.remove('active'));
        //             this.classList.add('active');
        //         });
        //     });
        // }

        // 3. Filter Logic (Keywords and Checkboxes)
        const keywordsList = document.querySelector('.keywords-list');
        const checkboxes = document.querySelectorAll('.checkbox-group input[type="checkbox"]');

        if (keywordsList && checkboxes.length > 0) {

            checkboxes.forEach(checkbox => {
                checkbox.addEventListener('change', function() {
                    const keyword = this.dataset.keyword;
                    if (this.checked) {
                        if (!document.querySelector(`.keyword-tag[data-keyword="${keyword}"]`)) {
                            const newTag = document.createElement('span');
                            newTag.className = 'keyword-tag';
                            newTag.setAttribute('data-keyword', keyword);
                            newTag.innerHTML = `${keyword} <i class="fa-solid fa-xmark remove-keyword-icon"></i>`;
                            keywordsList.appendChild(newTag);
                        }
                    } else {
                        const tagToRemove = document.querySelector(`.keyword-tag[data-keyword="${keyword}"]`);
                        if (tagToRemove) {
                            tagToRemove.remove();
                        }
                    }
                applyFilters();
                });
            });

            keywordsList.addEventListener('click', function(event) {
                const keywordIcon = event.target.closest('.remove-keyword-icon');
                if (keywordIcon) {
                    const keywordTag = keywordIcon.closest('.keyword-tag');
                    const keywordText = keywordTag.dataset.keyword;
                    const checkbox = document.querySelector(`.checkbox-container input[data-keyword="${keywordText}"]`);
                    if (checkbox) {
                        checkbox.checked = false;
                    }
                    keywordTag.remove();
                    applyFilters();
                }
            });
        }
    }

    // --- Function for search, filter, sort

    function applyFilters() {
    // 1. Створюємо порожній об'єкт для збору параметрів
    const params = new URLSearchParams();

    // 2. Зчитуємо значення пошуку
    const searchInput = document.querySelector('.search-input');
    if (searchInput && searchInput.value.trim() !== '') {
        params.append('search', searchInput.value.trim());
    }

    // 3. Зчитуємо активне сортування
    const activeSortButton = document.querySelector('.sort-options .active-sort');
    // Зверни увагу: ми використовуємо .dataset.sort щоб дістати data-sort
    if (activeSortButton && activeSortButton.dataset.sort) {
        params.append('sort', activeSortButton.dataset.sort);
    }

    // 4. Зчитуємо всі ВІДМІЧЕНІ чекбокси категорій
    const checkedBoxes = document.querySelectorAll('.checkbox-group input[type="checkbox"]:checked');
    checkedBoxes.forEach(checkbox => {
        // Додаємо кожен чекбокс як окремий параметр 'category'
        params.append('category', checkbox.dataset.keyword);
    });

    window.location.href = window.location.pathname + '?' + params.toString();
    }

    const searchButton = document.querySelector('.search-button');
    const searchInput = document.querySelector('.search-input');

    if (searchButton) {
        searchButton.addEventListener('click', applyFilters);
    }

    if (searchInput) {
    // Також запускаємо пошук, якщо користувач натиснув Enter у полі вводу
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                applyFilters();
            }
        });
    }

    // --- Logic for Product Detail Pages (product-*.html) ---
    const productPageContent = document.querySelector('.page-product');
    if (productPageContent) {
        // Accordion
        const accordionTitle = document.querySelector('.accordion-title');
        if (accordionTitle) {
            accordionTitle.addEventListener('click', function() {
                this.closest('.accordion-item').classList.toggle('active');
            });
        }
    }
    //     // "Add to Cart" Button and Counter
    //     const cartControls = document.querySelector('.cart-controls');
    //     if (cartControls) {
    //         const addToCartBtn = cartControls.querySelector('#add-to-cart-btn');
    //         const quantityCounter = cartControls.querySelector('#quantity-counter');
    //         const decreaseBtn = quantityCounter.querySelector('[data-action="decrease"]');
    //         const increaseBtn = quantityCounter.querySelector('[data-action="increase"]');
    //         const quantityValueSpan = quantityCounter.querySelector('.quantity-value');
    //         let quantity = 0;
    //         function updateView() {
    //             if (quantity === 0) {
    //                 addToCartBtn.classList.remove('is-hidden');
    //                 quantityCounter.classList.add('is-hidden');
    //             } else {
    //                 addToCartBtn.classList.add('is-hidden');
    //                 quantityCounter.classList.remove('is-hidden');
    //                 quantityValueSpan.textContent = `${quantity} in cart`;
    //             }
    //         }
    //         addToCartBtn.addEventListener('click', function() { quantity = 1; updateView(); });
    //         decreaseBtn.addEventListener('click', function() { if (quantity > 0) { quantity--; updateView(); } });
    //         increaseBtn.addEventListener('click', function() { quantity++; updateView(); });
    //         updateView();
    //     }
    // }

    // // --- Logic for Cart Page (cart.html) ---
    // const cartPageContent = document.querySelector('.cart-page-wrapper');
    // if (cartPageContent) {
    //     const cartItemsList = document.getElementById('cart-items-list');
    //     const cartTotalPriceElem = document.getElementById('cart-total-price');
    //     function updateCartTotal() {
    //         let total = 0;
    //         document.querySelectorAll('.cart-item').forEach(item => {
    //             const priceText = item.querySelector('[data-item-total-price]').textContent;
    //             if (priceText) {
    //                 total += parseFloat(priceText.replace('$', ''));
    //             }
    //         });
    //         if (cartTotalPriceElem) cartTotalPriceElem.textContent = `$${total.toFixed(2)}`;
    //     }
    //     if (cartItemsList) {
    //         cartItemsList.addEventListener('click', function(event) {
    //             const cartItem = event.target.closest('.cart-item');
    //             if (!cartItem) return;
    //             const quantityElem = cartItem.querySelector('.quantity-value-cart');
    //             const itemTotalElem = cartItem.querySelector('[data-item-total-price]');
    //             const basePrice = parseFloat(cartItem.dataset.price);
    //             let quantity = parseInt(quantityElem.textContent);
    //             if (event.target.closest('[data-action="increase"]')) {
    //                 quantity++;
    //             } else if (event.target.closest('[data-action="decrease"]')) {
    //                 quantity = quantity > 1 ? quantity - 1 : 0;
    //             }
    //             if (event.target.closest('[data-action="remove"]') || quantity === 0) {
    //                 cartItem.remove();
    //             } else {
    //                 quantityElem.textContent = quantity;
    //                 itemTotalElem.textContent = `$${(basePrice * quantity).toFixed(2)}`;
    //             }
    //             updateCartTotal();
    //         });
    //     }
    //     updateCartTotal();
    // }

    // --- Logic for Account and Admin Pages ---
    const accountAdminWrapper = document.querySelector('.account-page-wrapper, .admin-page-wrapper');
    if (accountAdminWrapper) {
        // Account Page Tabs
        const accountTabs = document.querySelectorAll('.account-tab');
        const tabPanes = document.querySelectorAll('.tab-pane');
        if (accountTabs.length > 0 && tabPanes.length > 0) {
            accountTabs.forEach(tab => {
                tab.addEventListener('click', function() {
                    accountTabs.forEach(item => item.classList.remove('active'));
                    tabPanes.forEach(pane => pane.classList.remove('active'));
                    const targetPane = document.querySelector(this.dataset.tabTarget);
                    this.classList.add('active');
                    if (targetPane) targetPane.classList.add('active');
                });
            });
        }

        // Admin Panel - Category Tags
        const categoryTagsContainer = document.querySelector('.category-tags');
        if (categoryTagsContainer) {
            categoryTagsContainer.addEventListener('click', function(e) {
                const clickedTag = e.target.closest('.category-tag');
                if (clickedTag) {
                    categoryTagsContainer.querySelectorAll('.category-tag').forEach(t => t.classList.remove('active'));
                    clickedTag.classList.add('active');
                }
            });
        }

        // Image Upload Simulation
        const uploadButton = document.getElementById('upload-image-btn');
        const fileInput = document.getElementById('image-upload-input');

        if (uploadButton && fileInput) {
            uploadButton.addEventListener('click', function() {
                fileInput.click();
            });

            fileInput.addEventListener('change', function(event) {
                const file = event.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    const placeholder = document.querySelector('.image-upload-placeholder');

                    reader.onload = function(e) {
                        placeholder.innerHTML = '';
                        placeholder.style.backgroundImage = `url('${e.target.result}')`;
                        placeholder.style.backgroundSize = 'cover';
                        placeholder.style.backgroundPosition = 'center';
                    }
                    reader.readAsDataURL(file);
                }
            });
        }
    }

    // const addToCartBtn = document.getElementById('add-to-cart-btn');
    // const quantityCounter = document.getElementById('quantity-counter');

    // if (addToCartBtn) {
    //     addToCartBtn.addEventListener('click', function() {
    //         // Ховаємо кнопку Add to Cart
    //         this.classList.add('is-hidden');
    //         // Показуємо лічильник
    //         if (quantityCounter) {
    //             quantityCounter.classList.remove('is-hidden');
    //             // Можна тут оновити текст лічильника, якщо потрібно
    //             const valueSpan = quantityCounter.querySelector('.quantity-value');
    //             if (valueSpan) valueSpan.innerText = '1 in cart';
    //         }
    //     });
    //     }
    // ==========================================
    // ЗВ'ЯЗОК З DJANGO БЕКЕНДОМ (КОШИК) - ОНОВЛЕНО
    // ==========================================

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Додаємо параметр 'button', щоб знати, який саме елемент видалити чи змінити
    function updateUserOrder(button, productId, action) {
        const url = '/orders/cart/update_item/'; 

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                'productId': productId,
                'action': action
            })
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.status === 'success') {
                // Шукаємо, на якій ми сторінці
                const cartItem = button.closest('.cart-item'); // Сторінка кошика
                const cartControls = button.closest('.cart-controls'); // Сторінка товару

                if (cartItem) {
                    // Логіка для сторінки КОШИКА
                    if (data.cart_item_quantity === 0) {
                        cartItem.remove();
                    } else {
                        const quantityElem = cartItem.querySelector('.quantity-value-cart');
                        const priceElem = cartItem.querySelector('[data-item-total-price]');
                        if (quantityElem) quantityElem.innerText = data.cart_item_quantity;
                        if (priceElem) priceElem.innerText = data.cart_item_costs;
                    }
                } else if (cartControls) {
                    // Логіка для сторінки ТОВАРУ
                    const addBtn = cartControls.querySelector('#add-to-cart-btn');
                    const counter = cartControls.querySelector('#quantity-counter');
                    const quantityElem = cartControls.querySelector('.quantity-value');

                    if (data.cart_item_quantity === 0) {
                        if (addBtn) addBtn.classList.remove('is-hidden');
                        if (counter) counter.classList.add('is-hidden');
                    } else {
                        if (addBtn) addBtn.classList.add('is-hidden');
                        if (counter) counter.classList.remove('is-hidden');
                        if (quantityElem) quantityElem.innerText = `${data.cart_item_quantity} in cart`;
                    }
                }

            // Оновлюємо загальну суму (тільки для кошика)
            const totalElem = document.getElementById('cart-total-price');
            if (totalElem) {
                totalElem.innerText = data.cart_total_price;
            }
        }
    });
}

    // Слухаємо всі кнопки
    const updateBtns = document.querySelectorAll('.update-cart-btn, .button--remove, .add-to-cart-button');

    updateBtns.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault(); 
            
            const productId = this.dataset.product;
            const action = this.dataset.action;
            
            // Передаємо 'this' (саму кнопку), щоб функція знала, що оновити
            updateUserOrder(this, productId, action);
        });
    });
});