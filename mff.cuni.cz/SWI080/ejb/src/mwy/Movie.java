package mwy;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;

// Declares an entity bean by annotation
@Entity
public class Movie  {

	// Persistent fields (not persistent would be annotated by @Transient)
	private int id;

	private String title;

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
	public Movie() {
	}

	// More useful constructor
	public Movie(String title) {
		this.title = title;
	}

	// Getter / setters for other fields
	public String getTitle() {
		return title;
	}

	public void setTitle(String title) {
		this.title = title;
	}
}
