// === Add to Cart ===
function addToCart(name, price) {
  let cart = JSON.parse(localStorage.getItem("cart")) || [];
  const existingItem = cart.find(item => item.name === name);

  if (existingItem) {
    existingItem.qty += 1;
  } else {
    cart.push({ name: name, price: price, qty: 1 });
  }

  localStorage.setItem("cart", JSON.stringify(cart));
  alert(`${name} added to cart!`);
}

// === Display Cart (for cart.html only) ===
function displayCart() {
  const cartContainer = document.getElementById("cart-items");
  const totalElement = document.getElementById("total");
  if (!cartContainer || !totalElement) return;

  cartContainer.innerHTML = "";
  let total = 0;
  const cart = JSON.parse(localStorage.getItem("cart")) || [];

  cart.forEach((item, index) => {
    const itemDiv = document.createElement("div");

    const itemText = document.createElement("span");
    const subtotal = item.price * item.qty;
    itemText.textContent = `${item.name} x ${item.qty} = ₹${subtotal}`;

    const removeBtn = document.createElement("button");
    removeBtn.textContent = "Remove";
    removeBtn.className = "remove-btn";
    removeBtn.onclick = () => removeItem(index);

    itemDiv.appendChild(itemText);
    itemDiv.appendChild(removeBtn);
    cartContainer.appendChild(itemDiv);

    total += subtotal;
  });

  totalElement.textContent = `Total: ₹${total}`;
}

// === Remove Cart Item ===
function removeItem(index) {
  let cart = JSON.parse(localStorage.getItem("cart")) || [];

  if (cart[index].qty > 1) {
    cart[index].qty -= 1;
  } else {
    cart.splice(index, 1);
  }

  localStorage.setItem("cart", JSON.stringify(cart));
  displayCart();
}

// === Sidebar Toggle ===
function toggleSidebar() {
  const sidebar = document.getElementById("sidebar");
  if (sidebar.style.width === "250px") {
    sidebar.style.width = "0";
  } else {
    sidebar.style.width = "250px";
  }
}

// === Back to Top Button ===
window.addEventListener("scroll", () => {
  const backToTopBtn = document.getElementById("backToTop");
  if (backToTopBtn) {
    backToTopBtn.classList.toggle("show", window.scrollY > 300);
  }
});


// === Filter Products (Manual Search) ===
function filterProducts() {
  const input = document.getElementById("searchInput").value.toLowerCase();
  const products = document.querySelectorAll(".product");

  products.forEach(product => {
    const name = product.querySelector("h2").textContent.toLowerCase();
    product.style.display = name.includes(input) ? "block" : "none";
  });
}

// === Voice Search ===
function startVoiceSearch() {
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  recognition.lang = "en-IN";
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.onresult = function (event) {
    const transcript = event.results[0][0].transcript;
    document.getElementById("searchInput").value = transcript;
    filterProducts();
  };

  recognition.onerror = function (event) {
    alert("Voice search failed: " + event.error);
  };

  recognition.start();
}

// === Run on Page Load ===
document.addEventListener("DOMContentLoaded", () => {
  displayCart();

  // Add TTS to product names (optional, if you want to bind it dynamically)
  document.querySelectorAll(".product h2").forEach(h2 => {
    h2.style.cursor = "pointer";
    h2.addEventListener("click", () => speak(h2.textContent));
  });
});
