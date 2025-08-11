class Book:
    def __init__(self, title, author, rating=None, tropes=None, status=None):
        self.title = title
        self.author = author
        self.rating = rating
        self.tropes = tropes if tropes is not None else []
        self.status = status