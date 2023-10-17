// Replace the existing code that defines the books array with an AJAX request

const bookContainer = document.getElementById("book-container");
const cartButton = document.getElementById("cart-button");
const cartCount = document.getElementById("cart-count");


let cartItems = 0;
let lowerLimit = 0; // Set your lower limit
let upperLimit = 12; // Set your upper limit

async function fetchBooks() {
    try {
        
        const response = await fetch(`/api/books?lower_limit=${lowerLimit}&upper_limit=${upperLimit}`);

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        bookContainer.innerHTML = '';

        const books = await response.json();
        while (bookContainer.firstChild) {
            bookContainer.removeChild(bookContainer.firstChild);
        }




        for (const book of books) {
            let bookEntry = document.createElement("div");
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
                        addToCart(book)
                        async function addToCart(book) {
                            try {
                                const response = await fetch('/add_to_cart', {
                                    method: 'POST',
                                    headers: {
                                        'Content-Type': 'application/json'
                                    },

                                    body: JSON.stringify({
                                        // titles: book.titles,
                                        image: book.image,
                                        stock: book.stock,
                                        ratings: book.ratings,
                                        price: book.price
                                    })
                                });
                        
                                if (!response.ok) {
                                    throw new Error('Failed to add book to cart');
                                }
                        
                                const data = await response.json();
                                // console.log(data.message);
                            } catch (error) {
                                console.error('Error:', error);
                            }
                        }
                        // Call fetchCartData to retrieve and display the cart data
                        fetchCartData(bookEntry);
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


            // async function addToCart(book) {
            //     try {
            //         const response = await fetch('/add_to_cart', {
            //             method: 'POST',
            //             headers: {
            //                 'Content-Type': 'application/json'
            //             },
            //             body: JSON.stringify({
            //                 book_id: book.id,
            //                 title: book.title,
            //                 image: book.image,
            //                 ratings: book.ratings,
            //                 price: book.price
            //             })
            //         });
            
            //         if (!response.ok) {
            //             throw new Error('Failed to add book to cart');
            //         }
            
            //         const data = await response.json();
            //         console.log(data.message);
            //     } catch (error) {
            //         console.error('Error:', error);
            //     }
            // }









            // if (addToCartButton) {
            //     addToCartButton.addEventListener("click", () => {
            //         if (book.stock > 0) {

            //             cartItems++;
            //             cartCount.textContent = cartItems;
            //             book.stock--;
            //             if (book.stock === 0) {
            //                 bookEntry.querySelector(".availability").textContent = "Out of Stock";
            //                 addToCartButton.remove();
            //             }
            //         } else {
            //             alert("This book is out of stock and cannot be added to the cart.");
            //         }
            //     });
            // }

            bookContainer.appendChild(bookEntry);
        }

        // const next123 = document.createElement("div");
        // next123.id = "next-button";

        // const next123 = bookEntry.querySelector(".add-to-cart");
            // if (addToCartButton) {
            //     addToCartButton.addEventListener("click", () => {
            //         if (book.stock > 0) {
            //             cartItems++;
            //             cartCount.textContent = cartItems;
            //             book.stock--;
            //             if (book.stock === 0) {
            //                 bookEntry.querySelector(".availability").textContent = "Out of Stock";
            //                 addToCartButton.remove();
            //             }
            //         } else {
            //             alert("This book is out of stock and cannot be added to the cart.");
            //         }
            //     });
            // }

    } catch (error) {
        console.error('Error fetching book data:', error);
    }
}

fetchBooks();

async function fetchCartData(bookEntry) {
    try {
        const response = await fetch('/cart_data');
        
        if (!response.ok) {
            throw new Error('Failed to fetch cart data');
        }

        const session_cart = await response.json();
        
        // Process the cart data as needed
        displayCart(session_cart, bookEntry);
    } catch (error) {
        console.error('Error fetching cart data:', error);
    }
}

function displayCart(session_cart,bookEntry) {
    
    console.log(session_cart)

    for (const item of session_cart) {
        console.log("hello")
        const cartItem = document.createElement('div');
        cartItem.className = 'cart-item';
        cartItem.innerHTML = `
            <p>${item.stock}</p>
        `;
        bookEntry.appendChild(cartItem);
    }
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

        // Create "Next" button
const nextButton = document.createElement("button");
nextButton.id = "next-button";
nextButton.textContent = "Next";

// Create "Previous" button
const prevButton = document.createElement("button");
prevButton.id = "prev-button";
prevButton.textContent = "Previous";

// Append "Previous" and "Next" buttons to the container
const paginationWrapper = document.querySelector(".pagination-wrapper");
paginationWrapper.appendChild(prevButton);
paginationWrapper.appendChild(nextButton);

// Add event listeners for "Next" and "Previous" buttons
nextButton.addEventListener("click", () => {
    lowerLimit += 12;
    upperLimit += 12;
    fetchBooks();
});

prevButton.addEventListener("click", () => {
    if (lowerLimit >= 12) {
        lowerLimit -= 12;
        upperLimit -= 12;
        fetchBooks();
    }


const add_to_cart = document.createElement("button");
add_to_cart.className = "add-to-cart";
add_to_cart.addEventListener("click", () => {
        
        console.log('this is working')
    });
});