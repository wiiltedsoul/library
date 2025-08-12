class Book:
    def __init__(self, title, author, rating=None, tropes=None, status=None, platform=None):
        self.title = title
        self.author = author
        self.rating = rating
        self.tropes = tropes if tropes is not None else []
        self.status = status
        self.plat = platform
    
    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "rating": self.rating,
            "tropes": self.tropes,
            "status": self.status,
            "platform": self.plat
        }