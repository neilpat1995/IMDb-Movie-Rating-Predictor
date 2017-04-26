import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class UpcomingMoviesParser {

	public static void main(String[] args) {

		//parseUpcomingMovies();

		List<Movie> upcomingMovies = new ArrayList<>();
		for(int month = 1; month < 4; month++){	
			upcomingMovies.addAll(load(month+"-list"));
        }
		//fetchMovieRatings(upcomingMovies); //for movies that have already released
        for(int month = 4; month < 10; month++){	
			upcomingMovies.addAll(load(month+"-list"));
        }
        //fetchMovieDetails(upcomingMovies);
        
        Map<String, String> facebookLikes = CombineDatasets.getFBLikesMap(new ArrayList<Movie>());
        for(Movie m : upcomingMovies){
        	m.castTotalFacebookLikes = "0";
        	if(facebookLikes.containsKey(m.directorName)){
        		m.directorFacebookLikes = facebookLikes.get(m.directorName);
        	}
        	if(!m.actor1Name.equals("") && facebookLikes.containsKey(m.actor1Name)){
        		m.actor1FacebookLikes = facebookLikes.get(m.actor1Name);
        		m.castTotalFacebookLikes = String.valueOf(Integer.parseInt(m.castTotalFacebookLikes) + Integer.parseInt(m.actor1FacebookLikes));
        	}
        	if(!m.actor2Name.equals("") && facebookLikes.containsKey(m.actor2Name)){
        		m.actor2FacebookLikes = facebookLikes.get(m.actor2Name);
        		m.castTotalFacebookLikes = String.valueOf(Integer.parseInt(m.castTotalFacebookLikes) + Integer.parseInt(m.actor2FacebookLikes));
        	}
        	if(!m.actor3Name.equals("") && facebookLikes.containsKey(m.actor3Name)){
        		m.actor3FacebookLikes = facebookLikes.get(m.actor3Name);
        		m.castTotalFacebookLikes = String.valueOf(Integer.parseInt(m.castTotalFacebookLikes) + Integer.parseInt(m.actor3FacebookLikes));
        	}
        }
        
		ExportData.export("upcoming_movies_new.csv", upcomingMovies, true);
	}
	
	private static void parseUpcomingMovies(){
		
		String imdbBaseUrl = "http://www.imdb.com";
		for(int month = 1; month < 10; month++){
			List<Movie> allMovies = new ArrayList<>();		
			String movieListUrl = imdbBaseUrl+"/movies-coming-soon/2017-0"+month+"/";
			try {
				//File input = new File("backup_upcoming.html");
				//Document doc = Jsoup.parse(input, "UTF-8");
				Document doc = Jsoup.connect(movieListUrl).get();
				Element movieList = doc.select("div.list.detail").first();
				Elements movies = movieList.select("div.list_item");
				for(Element movie : movies){
					
					Movie newMovie = new Movie();
					Element imgLink = movie.select("div.image").first();
					try{
						newMovie.posterLink = imgLink.select("img").first().attr("src");
					} catch (Exception npe){ }
					
					Element overview = movie.select("td.overview-top").first();
					Element name = overview.select("a").first();
					newMovie.movieImdbLink = name.attr("href");
					newMovie.movieTitle = name.attr("title").substring(0, name.attr("title").lastIndexOf('(')-1);
					newMovie.titleYear = "2017";
					Element details = overview.select("p.cert-runtime-genre").first();
					try{
						newMovie.contentRating = details.select("img").first().attr("title");
					} catch (Exception npe){ }
					try{
						newMovie.duration = details.select("time").first().text();
					} catch (Exception npe){ }
					Elements genres = overview.select("span");
					for(Element genre : genres){
						if(genre.attr("itemprop").equals("genre")){
							newMovie.genres.add(genre.text());
						}
					}
					Elements credits = overview.select("div.txt-block");
					for(Element credit : credits){
						Element detail = credit.select("span").first();
						if(detail != null && detail.hasAttr("itemprop")){
							if(detail.attr("itemprop").equals("director")){
								newMovie.directorName = detail.select("span").first().text();
							}
							if(detail.attr("itemprop").equals("actors")){
								newMovie.actor1Name = detail.select("span").first().text();
								try{
									newMovie.actor2Name = credit.select("span").get(2).select("span").first().text();
									newMovie.actor3Name = credit.select("span").get(4).select("span").first().text();
								} catch (Exception npe){ }
							}
						}
					}
					allMovies.add(newMovie);
				}
				
				//Thread.sleep(500);
			} catch (Exception e) {
				e.printStackTrace();
			}
			
			save(allMovies, month+"-list");
		}
	}
	
	private static void fetchMovieRatings(List<Movie> movies){
		String imdbBaseUrl = "http://www.imdb.com";
		for(Movie movie : movies){
			try {
				Document doc = Jsoup.connect(imdbBaseUrl+movie.movieImdbLink).get();
				Element rating = doc.select("div.ratingValue").first();
				movie.imdbScore = rating.select("span").first().text();
				
				//Thread.sleep(100);
			} catch (Exception e) {
				e.printStackTrace();
			}
		}
	}
	
	private static void fetchMovieDetails(List<Movie> movies){
		String imdbBaseUrl = "http://www.imdb.com";
		for(Movie movie : movies){
			try {
				Document doc = Jsoup.connect(imdbBaseUrl+movie.movieImdbLink).get();
				Element moneyInfo = doc.select("div#titleDetails").first();
				Elements moneyDetails = moneyInfo.select("div.txt-block");
				for(Element detail : moneyDetails){
					String detailText = detail.text();
					if(detail.text().contains("Budget")){
						movie.budget = detailText.substring(detailText.indexOf('$')+1, detailText.indexOf(' ', detailText.indexOf('$')));
					}
					if(detail.text().contains("Gross")){
						movie.gross = detailText.substring(detailText.indexOf('$')+1, detailText.indexOf(' ', detailText.indexOf('$')));
					}
				}
				
				//Thread.sleep(100);
			} catch (Exception e) {
				e.printStackTrace();
			}
		}
	}
	
	private static void save(List<Movie> movies, String filename){
		try(ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream("resources/upcoming/" + filename + ".ser"))){
			oos.writeObject(movies);
		} catch(Exception ex){
			System.err.println(ex.getMessage());
		}
	}
	
	protected static List<Movie> load(String filename){
		
		List<Movie> movies = null;
		try(ObjectInputStream ois = new ObjectInputStream(new FileInputStream("resources/upcoming/" + filename + ".ser"))){
			movies = (List<Movie>) ois.readObject();
		} catch(Exception ex){
			System.err.println(ex.getMessage());
		}
		return movies;
	}
}
