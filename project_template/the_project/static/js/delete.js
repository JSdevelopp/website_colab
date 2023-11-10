async function deleteFromCart(bookId) {
    try {
        const response = await fetch('/remove_from_cart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                bookId: bookId // Pass the book's ID to identify the book to delete
            })
        });

        if (!response.ok) {
            throw new Error('Failed to remove book from cart');
        }

        const data = await response.json();
        console.log(data.message);

        // Remove the book from the cart based on its ID
        const index = cart.findIndex((book) => book.id === bookId);
        if (index !== -1) {
            cart.splice(index, 1);
        }

        // Update the cart display after removing the book
        displayCart(cart);
    } catch (error) {
        console.error('Error:', error);
    }
}

// Add event listener for Delete buttons
cartContainer.addEventListener("click", (event) => {
    if (event.target.classList.contains("delete-from-cart")) {
        const item = event.target.parentNode;
        const bookId = item.dataset.bookId; // Get the book ID

        // Call the deleteFromCart function with the book's ID
        deleteFromCart(bookId);
    }
});