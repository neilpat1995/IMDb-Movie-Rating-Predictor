package msp.web;

import javax.annotation.PostConstruct;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;

import msp.internal.Utilities;

@Controller
public class WebController {

	@PostConstruct
	public void init(){
		for(int i = 0; i < 4; i++){
			Utilities.readPredictionsReleased(i);
			Utilities.readPredictions(i);
		}
	}
	
    @RequestMapping("/")
    public String index(Model model) {
    	model.addAttribute("movies", Utilities.movies.values());
    	model.addAttribute("moviesReleased", Utilities.moviesReleased.values());
        return "index";
    }
}
