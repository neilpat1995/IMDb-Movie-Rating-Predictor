import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

public class Movie implements Serializable {

	private static final long serialVersionUID = 1L;
	
	String movieImdbLink = "";
	String movieTitle = "";
	String titleYear = "";
	String imdbScore = "";
	String directorName = "";
	String actor1Name = "";
	String actor2Name = "";
	String actor3Name = "";
	String duration = "";
	String budget = "";
	String contentRating = "";
	List<String> genres = new ArrayList<>();
	String movieFacebookLikes = "";
	String directorFacebookLikes = "";
	String actor1FacebookLikes = "";
	String actor2FacebookLikes = "";
	String actor3FacebookLikes = "";
	String castTotalFacebookLikes = "";
	String facenumberInPoster = "";
	String gross = "";
	
	String posterLink = "";
	
	@Override
	public String toString() {
		return this.movieTitle + " (" + this.movieImdbLink + ")";
	}
}
