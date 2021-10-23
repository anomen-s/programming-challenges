package mwy;

import java.util.Collection;
import java.util.HashSet;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.OneToMany;

// Declares an entity bean by annotation
@Entity
public class Director {

	// Persistent fields (not persistent would be annotated by @Transient)
	private int id;
	private String name;
    // Field for the one-to-many relationship between entities
	private Collection<Movie> movies = new HashSet<Movie>();

	// Getter and setter methods for id field
	// @Id annotation denotes primary key mapping
	// @GeneratedValue denotes automatic key assignment
	@Id @GeneratedValue(strategy=GenerationType.AUTO)
	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	// Obligatory constructor with no arguments
	public Director() {
	}

	// More useful constructor
	public Director(String name) {
		this.name = name;
	}

	// Getter / setters for other fields
	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	// Getter and setter methods for movies
	// @OneToMany annotation denotes relationship mapping
	@OneToMany public Collection<Movie> getMovies () {
		return movies;
	}
	
	public void setMovies (Collection<Movie> movies) {
		this.movies = movies;
	}

	public void addMovie(Movie movie) {
		this.movies.add(movie);
	}

}
