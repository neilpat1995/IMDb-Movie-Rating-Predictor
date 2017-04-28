// Databricks notebook source
val imdb = sqlContext.table("imdb_info2")
val imdb2 = sqlContext.table("imdb_more_movies")

// Constants and pre-configuration
val COMBINED_10000_DATA_TABLE = "combined_10000_dataset"
val combined_data = sqlContext.table(COMBINED_10000_DATA_TABLE)

val imdb_full = imdb.union(imdb2)
display(imdb_full.select("*"))


// COMMAND ----------

val time_score = imdb_full.select($"duration",$"imdb_score").orderBy($"duration").filter(_ != null)
display(time_score)


// COMMAND ----------

val directorFB_score = imdb_full.select($"director_facebook_likes",$"imdb_score").orderBy($"director_facebook_likes").filter(_ != null)
display(directorFB_score)

// COMMAND ----------

val director_score = imdb_full.select($"director_name",$"imdb_score").filter(_ != null)
display(director_score)

// COMMAND ----------

val director_fb_score = imdb_full.select($"director_name",$"director_facebook_likes",$"imdb_score").filter(_ != null)
display(director_fb_score)

// COMMAND ----------

val face_score = imdb_full.select($"facenumber_in_poster",$"imdb_score").filter(_ != null)
display(face_score)

// COMMAND ----------

val content_rating_score = imdb_full.select($"content_rating",$"imdb_score").filter(_ != null)
display(content_rating_score)

// COMMAND ----------

val budget_score = imdb_full.select($"budget",$"imdb_score").filter(_ != null)//.orderBy($"budget")
display(budget_score)

// COMMAND ----------

val fblikes_score = imdb_full.select($"movie_facebook_likes",$"imdb_score").filter(_ != null)//.orderBy($"movie_facebook_likes")
display(fblikes_score)

//(2-D: #4) Genre to rating
val genre_rating = combined_data.filter($"genres".isNotNull && $"imdb_score".isNotNull).select($"genres", $"imdb_score").orderBy($"genres")
display(genre_rating)

//(2-D: #9) Actor 1 to rating
val actor1_score = combined_data.filter($"actor_1_name".isNotNull && $"imdb_score".isNotNull).select($"actor_1_name",$"imdb_score").orderBy($"actor_1_name")
display(actor1_score)

//(2-D: #10) Actor 1 FB likes to rating
val actor1_fb_likes_score = combined_data.filter($"actor_1_facebook_likes".isNotNull && $"imdb_score".isNotNull).select($"actor_1_facebook_likes",$"imdb_score").orderBy($"actor_1_facebook_likes")
display(actor1_fb_likes_score)

//(2-D: #11) Total cast FB likes to rating
val total_cast_likes_rating = combined_data.filter($"cast_total_facebook_likes".isNotNull && $"imdb_score".isNotNull).select($"cast_total_facebook_likes", $"imdb_score").orderBy($"cast_total_facebook_likes")
display(total_cast_likes_rating)

//(3-D: #1) Budget and FB movie likes to rating
val budget_fb_movie_likes_rating = combined_data.filter($"budget".isNotNull && $"movie_facebook_likes".isNotNull && $"imdb_score".isNotNull).select($"budget",$"movie_facebook_likes", $"imdb_score").orderBy($"budget", $"movie_facebook_likes")
display(budget_fb_movie_likes_rating)

//(3-D: #2) Director name and facebook likes to rating
val director_name_likes_rating = combined_data.filter($"director_name".isNotNull && $"director_facebook_likes".isNotNull && $"imdb_score".isNotNull).select($"director_name", $"director_facebook_likes", $"imdb_score").orderBy($"director_name", $"director_facebook_likes")
display(director_name_likes_rating)

//(3-D: #3) Genre and content rating to rating
val genre_content_rating_to_rating = combined_data.filter($"genres".isNotNull && $"content_rating".isNotNull && $"imdb_score".isNotNull).select($"genres",$"content_rating", $"imdb_score").orderBy($"genres", $"content_rating")
display(genre_content_rating_to_rating)

