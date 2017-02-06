import fresh_tomatoes
import movie
#entrypoint of the programm as well as the generation of the model types.
#stores different movie objects in a list and outputs them via a fresh tomato modul1
def main():
    movies = [] #list for movies
    #initialisation of movie inception
    inception = movie.Movie("Inception",
                            "https://alexhorakdesign.files.wordpress.com/2013/04/inception-layout.jpg%3Fw=621",
                            "https://www.youtube.com/watch?v=YoHD9XEInc0")
    
    movies.append(inception) #append inception to the movielist
    

    #initialisation of movie red1
    red1 = movie.Movie("Retired Extremly Dangerous",
                            "https://janwrites03.files.wordpress.com/2012/06/red-movie-poster1.jpg",
                            "https://www.youtube.com/watch?v=qMvPWytJ740")
    movies.append(red1) #append red1 to the movielist
    

    #initialisation of movie red2
    red2 = movie.Movie("Retired Extremly Dangerous 2",
                            "https://lh3.googleusercontent.com/GTOPqoeukzi71ZJg4GBKlhTzJBAaXi-hu8Z79t4jnWoDXWYtm1AB_vtaWW8TPjQheS6Wnw=w300",
                            "https://www.youtube.com/watch?v=QsBOrSnqdFI")
    movies.append(red2) #append red2 to the movielist
    
    #send the data to the fresh_tomato module
    fresh_tomatoes.open_movies_page(movies)
    
main(); #call of the main method
