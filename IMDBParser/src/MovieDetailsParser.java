import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.ArrayList;
import java.util.List;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class MovieDetailsParser {

	public static void main(String[] args) {

		//parseMovieDetails();
	}
	
	private static void parseMovieDetails(){
		
		String imdbBaseUrl = "http://www.imdb.com";
		for(int year = 2016; year >= 2006; year--){
			List<Movie> movies = MovieListParser.load(year+"-list");
			List<Movie> allMovies = new ArrayList<>();
			for(Movie movie : movies){
				try {
					//File input = new File("backup_details.html");
					//Document doc = Jsoup.parse(input, "UTF-8");
					Document doc = Jsoup.connect(imdbBaseUrl+movie.movieImdbLink).get();
					Elements credits = doc.select("div.credit_summary_item");
					for(Element credit : credits){
						Element detail = credit.select("span").first();
						if(detail.attr("itemprop").equals("director")){
							movie.directorName = detail.select("span.itemprop").first().text();
						}
						if(detail.attr("itemprop").equals("actors")){
							movie.actor1Name = detail.select("span.itemprop").first().text();
							try{
								movie.actor2Name = credit.select("span").get(2).select("span.itemprop").first().text();
								movie.actor3Name = credit.select("span").get(4).select("span.itemprop").first().text();
							} catch (Exception npe){ }
						}
					}
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
					
					Element poster = doc.select("div.poster").first();
					try{
						movie.posterLink = poster.select("img").first().attr("src");
					} catch (Exception npe){ }
					
					allMovies.add(movie);
					
					//Thread.sleep(100);
				} catch (Exception e) {
					System.out.println(year + ", " + movie.movieTitle + ", " + movie.movieImdbLink);
					e.printStackTrace();
				}
			}
			
			save(allMovies, year+"-details");
		}
	}
	
	private static void save(List<Movie> movies, String filename){
		try(ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream("resources/details/" + filename + ".ser"))){
			oos.writeObject(movies);
		} catch(Exception ex){
			System.err.println(ex.getMessage());
		}
	}
	
	protected static List<Movie> load(String filename){
		
		List<Movie> movies = null;
		try(ObjectInputStream ois = new ObjectInputStream(new FileInputStream("resources/details/" + filename + ".ser"))){
			movies = (List<Movie>) ois.readObject();
		} catch(Exception ex){
			System.err.println(ex.getMessage());
		}
		return movies;
	}
}
