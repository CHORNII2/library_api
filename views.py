from flask import jsonify, request
from . import app
from .models import Book
from .schemas import BookSchema
from marshmallow import ValidationError

books = []
book_schema = BookSchema()
next_id = 1

@app.route("/books", methods=["GET"])
def get_books():
    return jsonify([book.to_dict() for book in books]), 200

@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((b for b in books if b.id == book_id), None)
    if book:
        return jsonify(book.to_dict()), 200
    return jsonify({"error": "Book not found"}), 404

@app.route("/books", methods=["POST"])
def add_book():
    global next_id
    try:
        book_data = request.get_json()
        validated_data = book_schema.load(book_data)
        book = Book(id=next_id, **validated_data)
        books.append(book)
        next_id += 1
        return jsonify(book.to_dict()), 201
    except ValidationError as err:
        return jsonify(err.messages), 400

@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    global books
    book = next((b for b in books if b.id == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    books = [b for b in books if b.id != book_id]
    return jsonify({"message": "Book deleted"}), 200
