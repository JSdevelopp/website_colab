@app.route('/remove_from_cart', methods=['POST'])
def deleteFromCart():
    data = request.json
    book_id = data.get('bookId')  # Retrieve the book ID from the request

    if 'cart' in session:
        cart = session['cart']

        # Find and remove the book with the matching ID from the cart
        for book in cart:
            if book.get('bookId') == book_id:
                cart.remove(book)
                session.modified = True
                return jsonify({'message': 'Book removed from cart', 'bookId': book_id})

    return jsonify({'message': 'Book not found in the cart or no cart exists'}), 404