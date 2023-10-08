// Replace the existing code that defines the books array with an AJAX request

const bookContainer = document.getElementById("book-container");
const cartButton = document.getElementById("cart-button");
const cartCount = document.getElementById("cart-count");


let cartItems = 0;

async function fetchBooks() {
    try {
        let lowerLimit = 12; // Set your lower limit
        let upperLimit = 24; // Set your upper limit
        const response = await fetch(`/api/books?lower_limit=${lowerLimit}&upper_limit=${upperLimit}`);

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const books = await response.json();

        for (const book of books) {
            const bookEntry = document.createElement("div");
            bookEntry.className = "book-entry";

            bookEntry.innerHTML = `
                <img src="${book.image}" alt="${book.title}">
                <div class="ratings">
                    ${getStarRatingHTML(book.ratings)}
                </div>
                <p>Price: ${book.price}</p>
                ${book.stock > 0 ? `<p>${book.stock} in stock</p>` : '<p class="availability">Out of Stock</p>'}
                ${book.stock > 0 ? '<button class="add-to-cart">Add to Cart</button>' : ''}
            `;

            const addToCartButton = bookEntry.querySelector(".add-to-cart");
            if (addToCartButton) {
                addToCartButton.addEventListener("click", () => {
                    if (book.stock > 0) {
                        cartItems++;
                        cartCount.textContent = cartItems;
                        book.stock--;
                        if (book.stock === 0) {
                            bookEntry.querySelector(".availability").textContent = "Out of Stock";
                            addToCartButton.remove();
                        }
                    } else {
                        alert("This book is out of stock and cannot be added to the cart.");
                    }
                });
            }

            bookContainer.appendChild(bookEntry);
        }
    } catch (error) {
        console.error('Error fetching book data:', error);
    }
}

fetchBooks();


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
            fetchBooks()
            // console.log(lowerLimit)
            // console.log(upperLimit)
            // lowerLimit += 12
            // upperLimit += 12
            // console.log(lowerLimit)
            // console.log(upperLimit)
        })