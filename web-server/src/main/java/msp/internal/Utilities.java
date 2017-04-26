package msp.internal;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

import msp.data.Movie;

public class Utilities {
	
	public static Map<String, Movie> moviesReleased = new HashMap<>();
	public static Map<String, Movie> movies = new HashMap<>();
	
	public static void readPredictionsReleased(int model){
		
		String csvFile = null;
		switch(model){
			case 0: csvFile = "knn-predictions-released.csv"; break;
			case 1: csvFile = "forests-predictions-released.csv"; break;
			case 2: csvFile = "logistic-predictions-released.csv"; break;
			case 3: csvFile = "linear-predictions-released.csv"; break;
		}
        String line = "";
        try (BufferedReader br = new BufferedReader(new FileReader(csvFile))) {

        	br.readLine(); //skip headers
            while ((line = br.readLine()) != null) {
                String[] movieInfo = line.split(",");
                if(movieInfo.length != 4){
                	continue;
                }
                
                Movie m = new Movie(movieInfo[1], movieInfo[0]);
            	m.scores[model] = Double.parseDouble(movieInfo[2]);
                m.actualScore = movieInfo[3];
                if(!moviesReleased.containsKey(m.link)){
                	moviesReleased.put(m.link, m);
                } else {
                	if(moviesReleased.get(m.link).scores[model] == -1){
                		moviesReleased.get(m.link).scores[model] = m.scores[model];
                	} else {
                		moviesReleased.get(m.link).scores[model] = (moviesReleased.get(m.link).scores[model] + m.scores[model])/2;
                	}
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
	}
	
	public static void readPredictions(int model){
		
		String csvFile = null;
		switch(model){
			case 0: csvFile = "knn-predictions.csv"; break;
			case 1: csvFile = "forests-predictions.csv"; break;
			case 2: csvFile = "logistic-predictions.csv"; break;
			case 3: csvFile = "linear-predictions.csv"; break;
		}
        String line = "";
        try (BufferedReader br = new BufferedReader(new FileReader(csvFile))) {

        	br.readLine(); //skip headers
            while ((line = br.readLine()) != null) {
                String[] movieInfo = line.split(",");
                if(movieInfo.length != 3){
                	continue;
                }
                
                Movie m = new Movie(movieInfo[1], movieInfo[0]);
            	m.scores[model] = Double.parseDouble(movieInfo[2]);
                if(!movies.containsKey(m.link)){
                	movies.put(m.link, m);
                } else {
                	if(movies.get(m.link).scores[model] == -1){
                		movies.get(m.link).scores[model] = m.scores[model];
                	} else {
                		movies.get(m.link).scores[model] = (movies.get(m.link).scores[model] + m.scores[model])/2;
                	}
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
	}
}
