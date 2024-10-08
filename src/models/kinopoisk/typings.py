class FilmData:
    def __init__(self, title: str, rating: str, img_url: str, director:  str):
        self.title = title
        self.rating = rating
        self.img_url = img_url
        self.director = director

    def __str__(self):
        return f'Title: {self.title}\nRating: {self.rating}\nImage URL: {self.img_url}\nDirector: {self.director}'
