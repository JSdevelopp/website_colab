// Array of book objects
const books = [
    {
        image: "https://prodimage.images-bn.com/pimages/9781544512273_p0_v8_s1200x630.jpg",
        title: "Can't Hurt Me",
        ratings: 5,
        price: "$19.99",
        stock: 5,
    },
    {
        image: "book2.jpg",
        title: "Book Title 2",
        ratings: 4,
        price: "$14.99",
        stock: 3,
    },
    // Add more books as needed
];

// Get the book container element
const bookContainer = document.getElementById("book-container");
const cartButton = document.getElementById("cart-button");
const cartCount = document.getElementById("cart-count");

let cartItems = 0;

// Loop through each book and create book entries
for (const book of books) {
    const bookEntry = document.createElement("div");
    bookEntry.className = "book-entry";

    bookEntry.innerHTML = `
        <img src="${book.image}" alt="${book.title}">
        <h3>${book.title}</h3>
        <div class="ratings">
            ${getStarRatingHTML(book.ratings)}
        </div>
        <p>Price: ${book.price}</p>
        <p class="availability">${book.stock > 0 ? 'In Stock <span class="checkmark">&#10003;</span>' : 'Out of Stock'}</p>
        ${book.stock > 0 ? '<button class="add-to-cart">Add to Cart</button>' : ''}
    `;

    const addToCartButton = bookEntry.querySelector(".add-to-cart");
    if (addToCartButton) { // Check if the button exists (for books in stock)
        addToCartButton.addEventListener("click", () => {
            if (book.stock > 0) {
                cartItems++;
                cartCount.textContent = cartItems;
                book.stock--; // Decrease the stock after adding to cart
                if (book.stock === 0) {
                    bookEntry.querySelector(".availability").textContent = "Out of Stock"; // Update availability message
                    addToCartButton.remove(); // Remove "Add to Cart" button
                }
            } else {
                alert("This book is out of stock and cannot be added to the cart.");
            }
        });
    }

    bookContainer.appendChild(bookEntry);
}

// Function to generate star rating HTML
function getStarRatingHTML(ratings) {
    const star = '<span class="star">&#9733;</span>';
    return star.repeat(ratings);
}

// Pagination
//Define the current page and the total number of pages
let currentPage = 1;
const totalPages = 20; // Total number of pages we will have

// Get a reference to the "Next" button
const nextButton = document.getElementById("next-button");

// Add an event listener to the "Next button"
nextButton.addEventListener("click", () => {
    if (currentPage < totalPages) {
        currentPage++;
        window.location.href = "page-one.html"; // Navigate to the next page
    }
});