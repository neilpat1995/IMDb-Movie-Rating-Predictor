import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;
import java.util.Arrays;
import java.util.List;

public class ExportData {

	private static final char DEFAULT_SEPARATOR = ',';
	private static final String title = "director_name,duration,director_facebook_likes,actor_3_facebook_likes,"
			+ "actor_2_name,actor_1_facebook_likes,gross,genres,actor_1_name,movie_title,"
			+ "cast_total_facebook_likes,actor_3_name,facenumber_in_poster,plot_keywords,movie_imdb_link,"
			+ "content_rating,budget,title_year,actor_2_facebook_likes,imdb_score,movie_facebook_likes";

	public static void main(String[] args){

		/*
		List<Movie> scrapedMovies = new ArrayList<>();
        for(int year = 2016; year >= 2006; year--){	
			scrapedMovies.addAll(MovieDetailsParser.load(year+"-details"));
        }
		export("2006-2016_additional_movies.csv", scrapedMovies, false);
		*/
	}
	
	public static void export(String filename, List<Movie> movies, boolean separateGenres){
		try {
			FileWriter writer = new FileWriter(filename);
			writeLine(writer, Arrays.asList(title.split(",")));

			for(Movie movie : movies){
				String duration = movie.duration;
				duration = duration.contains("min") ? duration.substring(0, duration.indexOf(' ')) : "";
				String gross = movie.gross;
				gross = (gross != null) ? gross.replaceAll(",", "") : "";
				try {
					Integer.parseInt(gross);
				} catch (Exception nfe) {
					gross = "";
				}
				String budget = movie.budget;
				budget = (budget != null) ? budget.replaceAll(",", "") : "";
				if(budget.equals("Budget:")){
					budget = "";
				}
				String movieLink = movie.movieImdbLink.contains("http://www.imdb.com") ? movie.movieImdbLink : "http://www.imdb.com"+movie.movieImdbLink;
				movie.movieTitle = movie.movieTitle.replaceAll("[^\\x00-\\x7F]","");
				if(movie instanceof MovieV2){
					MovieV2 movieV2 = (MovieV2) movie;
					if(separateGenres){
						for(String genre : movieV2.genres){
							writeLine(writer, Arrays.asList(movieV2.directorName, duration, movieV2.directorFacebookLikes, movieV2.actor3FacebookLikes, 
									movieV2.actor2Name, movieV2.actor1FacebookLikes, gross, genre, movieV2.actor1Name, movieV2.movieTitle,
									movieV2.castTotalFacebookLikes, movieV2.actor3Name, movieV2.facenumberInPoster, movieV2.plotKeywords, movieLink,
									movieV2.contentRating, budget, movieV2.titleYear, movieV2.actor2FacebookLikes, movieV2.imdbScore, movieV2.movieFacebookLikes));
						}
					} else {
						writeLine(writer, Arrays.asList(movieV2.directorName, duration, movieV2.directorFacebookLikes, movieV2.actor3FacebookLikes, 
								movieV2.actor2Name, movieV2.actor1FacebookLikes, gross, String.join("|", movieV2.genres), movieV2.actor1Name, movieV2.movieTitle,
								movieV2.castTotalFacebookLikes, movieV2.actor3Name, movieV2.facenumberInPoster, movieV2.plotKeywords, movieLink,
								movieV2.contentRating, budget, movieV2.titleYear, movieV2.actor2FacebookLikes, movieV2.imdbScore, movieV2.movieFacebookLikes));
					}
				} else {
					if(separateGenres){
						for(String genre : movie.genres){
							writeLine(writer, Arrays.asList(movie.directorName, duration, movie.directorFacebookLikes, movie.actor3FacebookLikes, 
									movie.actor2Name, movie.actor1FacebookLikes, gross, genre, movie.actor1Name, movie.movieTitle,
									movie.castTotalFacebookLikes, movie.actor3Name, movie.facenumberInPoster, "", movieLink,
									movie.contentRating, budget, movie.titleYear, movie.actor2FacebookLikes, movie.imdbScore, movie.movieFacebookLikes));
						}
					} else {
						writeLine(writer, Arrays.asList(movie.directorName, duration, movie.directorFacebookLikes, movie.actor3FacebookLikes, 
								movie.actor2Name, movie.actor1FacebookLikes, gross, String.join("|", movie.genres), movie.actor1Name, movie.movieTitle,
								movie.castTotalFacebookLikes, movie.actor3Name, movie.facenumberInPoster, "", movieLink,
								movie.contentRating, budget, movie.titleYear, movie.actor2FacebookLikes, movie.imdbScore, movie.movieFacebookLikes));
					}
				}
			}

			writer.flush();
			writer.close();
		} catch (Exception e){
			e.printStackTrace();
		}
	}

	private static void writeLine(Writer w, List<String> values) throws IOException {
		writeLine(w, values, DEFAULT_SEPARATOR, ' ');
	}

	private static String followCVSformat(String value) {

		if(value == null){
			value = "";
		}
		value = value.replaceAll(",", " ");
		String result = value;
		if (result.contains("\"")) {
			result = result.replace("\"", "\"\"");
		}
		return result;
	}

	private static void writeLine(Writer w, List<String> values, char separators, char customQuote) throws IOException {

		boolean first = true;

		if (separators == ' ') {
			separators = DEFAULT_SEPARATOR;
		}

		StringBuilder sb = new StringBuilder();
		for (String value : values) {
			if (!first) {
				sb.append(separators);
			}
			if (customQuote == ' ') {
				sb.append(followCVSformat(value));
			} else {
				sb.append(customQuote).append(followCVSformat(value)).append(customQuote);
			}

			first = false;
		}
		sb.append("\n");
		w.append(sb.toString());
	}
}
