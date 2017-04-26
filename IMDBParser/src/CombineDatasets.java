import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class CombineDatasets {

	public static void main(String[] args) {

		List<Movie> movies = new ArrayList<Movie>();
		Map<String, String> facebookLikes = getFBLikesMap(movies);
        
        List<Movie> scrapedMovies = new ArrayList<>();
        for(int year = 2016; year >= 2006; year--){	
			scrapedMovies.addAll(MovieDetailsParser.load(year+"-details"));
        }
        
        Map<String, Movie> combinedMovieList = new HashMap<>();
        for(Movie m : movies){
        	String link = m.movieImdbLink.lastIndexOf("/") == -1 ? m.movieImdbLink : m.movieImdbLink.substring(0, m.movieImdbLink.lastIndexOf("/"));
        	m.movieImdbLink = link;
        	if(!combinedMovieList.containsKey(link)){
        		combinedMovieList.put(link, m);
        	}
        }
        for(Movie m : scrapedMovies){
        	String link = m.movieImdbLink.lastIndexOf("/") == -1 ? m.movieImdbLink : m.movieImdbLink.substring(0, m.movieImdbLink.lastIndexOf("/"));
        	link = "http://www.imdb.com"+link;
        	m.movieImdbLink = link;
        	m.castTotalFacebookLikes = "0";
        	if(facebookLikes.containsKey(m.directorName)){
        		m.directorFacebookLikes = facebookLikes.get(m.directorName);
        	}
        	if(!m.actor1Name.equals("") && facebookLikes.containsKey(m.actor1Name)){
        		m.actor1FacebookLikes = facebookLikes.get(m.actor1Name);
        		m.castTotalFacebookLikes = String.valueOf(Integer.parseInt(m.castTotalFacebookLikes) + Integer.parseInt(m.actor1FacebookLikes));
        	}
        	if(m.actor2Name != null && !m.actor2Name.equals("") && facebookLikes.containsKey(m.actor2Name)){
        		m.actor2FacebookLikes = facebookLikes.get(m.actor2Name);
        		m.castTotalFacebookLikes = String.valueOf(Integer.parseInt(m.castTotalFacebookLikes) + Integer.parseInt(m.actor2FacebookLikes));
        	}
        	if(m.actor3Name != null && !m.actor3Name.equals("") && facebookLikes.containsKey(m.actor3Name)){
        		m.actor3FacebookLikes = facebookLikes.get(m.actor3Name);
        		m.castTotalFacebookLikes = String.valueOf(Integer.parseInt(m.castTotalFacebookLikes) + Integer.parseInt(m.actor3FacebookLikes));
        	}
        	
        	if(!combinedMovieList.containsKey(link)){
        		combinedMovieList.put(link, m);
        	}
        }
        
        ExportData.export("15k_movies_new.csv", new ArrayList<>(combinedMovieList.values()), true);
	}
	
	public static Map<String, String> getFBLikesMap(List<Movie> movies){
		
		Map<String, String> facebookLikes = new HashMap<>();
		
		String csvFile = "movie_metadata.csv";
        String line = "";
        try (BufferedReader br = new BufferedReader(new FileReader(csvFile))) {

        	br.readLine(); //skip headers
            while ((line = br.readLine()) != null) {
                String[] movieInfo = line.split(",");
                if(movieInfo.length != 28){
                	continue;
                }
                /*
                 0color,1director_name,2num_critic_for_reviews,3duration,4director_facebook_likes,
                 5actor_3_facebook_likes,6actor_2_name,7actor_1_facebook_likes,8gross,9genres,
                 10actor_1_name,11movie_title,12num_voted_users,13cast_total_facebook_likes,14actor_3_name,
                 15facenumber_in_poster,16plot_keywords,17movie_imdb_link,18num_user_for_reviews,19language,
                 20country,21content_rating,22budget,23title_year,24actor_2_facebook_likes,25imdb_score,26aspect_ratio,27movie_facebook_likes
                 */
                MovieV2 movie = new MovieV2();
                movie.directorName = movieInfo[1];
                movie.duration = movieInfo[3];
                movie.directorFacebookLikes = movieInfo[4];
                movie.actor3FacebookLikes = movieInfo[5];
                movie.actor2Name = movieInfo[6];
                movie.actor1FacebookLikes = movieInfo[7];
                movie.gross = movieInfo[8];
                movie.genres = Arrays.asList(movieInfo[9].split("\\|"));
                movie.actor1Name = movieInfo[10];
                movie.movieTitle = movieInfo[11];
                movie.castTotalFacebookLikes = movieInfo[13];
                movie.actor3Name = movieInfo[14];
                movie.facenumberInPoster = movieInfo[15];
                movie.plotKeywords = movieInfo[16];
                movie.movieImdbLink = movieInfo[17];
                movie.contentRating = movieInfo[21];
                movie.budget = movieInfo[22];
                movie.titleYear = movieInfo[23];
                movie.actor2FacebookLikes = movieInfo[24];
                movie.imdbScore = movieInfo[25];
                movie.movieFacebookLikes = movieInfo[27];
                movies.add(movie);
                
                facebookLikes.put(movie.directorName, movie.directorFacebookLikes);
                facebookLikes.put(movie.actor1Name, movie.actor1FacebookLikes);
                facebookLikes.put(movie.actor2Name, movie.actor2FacebookLikes);
                facebookLikes.put(movie.actor3Name, movie.actor3FacebookLikes);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        
        return facebookLikes;
	}
}
