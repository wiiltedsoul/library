# book.py
class Book:
    # Add 'series_name=None' and 'series_order=None' to the __init__ parameters
    def __init__(self, title, author, rating=None, tropes=None, status=None, platform=None, length_value=None, length_unit=None, dnf_reason=None, isbn=None, series_name=None, series_order=None):
        self.title = title
        self.author = author
        self.rating = rating
        self.tropes = tropes if tropes is not None else []
        self.status = status
        self.plat = platform
        self.length_value = length_value
        self.length_unit = length_unit
        self.dnf_reason = dnf_reason
        self.isbn = isbn
        self.series_name = series_name    # <--- New attribute here!
        self.series_order = series_order  # <--- New attribute here!

    def to_dict(self):
        # Converts the Book object into a dictionary suitable for JSON serialization
        return {
            "title": self.title,
            "author": self.author,
            "rating": self.rating,
            "tropes": self.tropes,
            "status": self.status,
            "platform": self.plat,
            "length_value": self.length_value,
            "length_unit": self.length_unit,
            "dnf_reason": self.dnf_reason,
            "isbn": self.isbn,
            "series_name": self.series_name,
            "series_order": self.series_order
        }