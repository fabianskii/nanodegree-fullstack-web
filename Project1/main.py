import fresh_tomatoes
import movie

def main():
    movies = []
    inception = movie.Movie("Inception",
                            "https://alexhorakdesign.files.wordpress.com/2013/04/inception-layout.jpg%3Fw=621",
                            "https://www.youtube.com/watch?v=YoHD9XEInc0")
    movies.append(inception)
    red1 = movie.Movie("Retired Extremly Dangerous",
                            "https://janwrites03.files.wordpress.com/2012/06/red-movie-poster1.jpg",
                            "https://www.youtube.com/watch?v=qMvPWytJ740")
    movies.append(red1)

    red2 = movie.Movie("Retired Extremly Dangerous 2",
                            "https://lh3.googleusercontent.com/GTOPqoeukzi71ZJg4GBKlhTzJBAaXi-hu8Z79t4jnWoDXWYtm1AB_vtaWW8TPjQheS6Wnw=w300",
                            "https://www.youtube.com/watch?v=QsBOrSnqdFI")
    movies.append(red2)
    
    fresh_tomatoes.open_movies_page(movies)
    
main();
