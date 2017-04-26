package msp.data;

public class Movie {

	public String link;
	public String name;
	public String actualScore = "N/A";
	public double[] scores = null;
	
	public Movie(String link, String name){
		this.link = link;
		this.name = name;
		this.scores = new double[]{-1, -1, -1, -1};
	}
	
	@Override
	public String toString() {
		return this.name + " (" + this.link + ")";
	}
}
