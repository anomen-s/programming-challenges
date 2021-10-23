package mwy;

import java.util.List;

import javax.ejb.Remote;

// Denotes remote interface  by annotation
@Remote
public interface ExampleEntities {
	public int addDirector(String name);

	public int addMovie(String name, int idDirector);

	List<String> getDirectors();

	List<String> getDirectorsWithMovies();
}
