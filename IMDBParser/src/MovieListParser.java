import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class MovieListParser {

	public static void main(String[] args) {

		//parseMovieList();
	}
	
	private static void parseMovieList(){
		
		String imdbBaseUrl = "http://www.imdb.com";
		for(int year = 2016; year >= 2006; year--){
			List<Movie> allMovies = new ArrayList<>();		
			String movieListUrl = imdbBaseUrl+"/search/title?year="+year+"&title_type=feature&sort=moviemeter,asc&view=advanced";
			for(int page = 1; page <= 20; page++){
				try {
					//File input = new File("backup_list.html");
					//Document doc = Jsoup.parse(input, "UTF-8");
					Document doc = Jsoup.connect(movieListUrl + "&page="+page).get();
					Element movieList = doc.select("div.lister-list").first();
					Elements movies = movieList.select("div.lister-item");
					for(Element movie : movies){
						
						Element content = movie.select("div.lister-item-content").first();
						Element ref = content.select("a").first();
						String link = ref.attr("href");
						String name = ref.text();
						String rating;
						try {
							rating = content.select("div.ratings-imdb-rating").first().text();
						} catch (Exception npe){
							continue;
						}
						Element details = content.select("p.text-muted").first();
						String certificate;
						try {
							certificate = details.select("span.certificate").first().text();
						} catch (Exception npe){
							certificate = "Unrated";
						}
						String runtime;
						try {
							runtime = details.select("span.runtime").first().text();
						} catch (Exception npe){
							runtime = "";
						}
						String genre;
						try {
							genre = details.select("span.genre").first().text();
						} catch (Exception npe){
							genre = "";
						}
						List<String> genres = Arrays.asList(genre.split(", "));
						
						Movie tmp = new Movie();
						tmp.movieImdbLink = link;
						tmp.movieTitle = name;
						tmp.titleYear = year+"";
						tmp.imdbScore = rating;
						tmp.contentRating = certificate;
						tmp.duration = runtime;
						tmp.genres = genres;
						allMovies.add(tmp);
					}
					
					//Thread.sleep(500);
				} catch (Exception e) {
					System.out.println(page);
					e.printStackTrace();
				}
			}
			
			save(allMovies, year+"-list");
		}
	}
	
	private static void save(List<Movie> movies, String filename){
		try(ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream("resources/lists/" + filename + ".ser"))){
			oos.writeObject(movies);
		} catch(Exception ex){
			System.err.println(ex.getMessage());
		}
	}
	
	protected static List<Movie> load(String filename){
		
		List<Movie> movies = null;
		try(ObjectInputStream ois = new ObjectInputStream(new FileInputStream("resources/lists/" + filename + ".ser"))){
			movies = (List<Movie>) ois.readObject();
		} catch(Exception ex){
			System.err.println(ex.getMessage());
		}
		return movies;
	}
}
