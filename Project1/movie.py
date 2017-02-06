class Movie:
   def __init__ (self, title, arturl, trailerurl):
   	"""
   	Describes the structure and attributes of a Movie object.
   	@type Movie
   	@param self the object itself
   	@title the movie title
   	@acturl the poster image url of the movie
   	@trailerurl a link to a trailer
   	"""
        self.title = title
        self.poster_image_url = arturl
        self.trailer_youtube_url = trailerurl
        
