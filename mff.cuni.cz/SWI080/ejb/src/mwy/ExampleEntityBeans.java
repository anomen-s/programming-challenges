package mwy;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

import javax.ejb.Stateful;
import javax.ejb.Stateless;
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import javax.persistence.PersistenceContextType;
import javax.persistence.Query;

// Denotes stateful session bean by annotation
@Stateful
public class ExampleEntityBeans implements ExampleEntities {

	// Annotation for automatic EntityManager dependency injection by container
	// unitName specifies the name of the persistence unit (declared in
	// persistence.xml)
	@PersistenceContext(unitName = "movie-unit", type = PersistenceContextType.EXTENDED)
	private EntityManager entityManager;

	// Adds a new director instance
	public int addDirector(String name) {
		// Creates a new entity instance with given name
		Director d = new Director(name);
		// Makes the instance managed and persistent.
		entityManager.persist(d);
		// Returns the auto-assigned primary key of the instance
		return d.getId();
	}

	// Adds a new movie instance of given name and director specified by primary
        // key
	public int addMovie(String name, int idDirector) {
		// Creates a new entity instance with given name
		Movie movie = new Movie(name);
		// Makes the instance managed and persistent.
		entityManager.persist(movie);
		// Obtains director instance with the given primary key
		Director d = entityManager.find(Director.class, idDirector);
		// Creates the director->movie relationship
		d.addMovie(movie);
		// Returns the auto-assigned primary key of the movie instance
		return movie.getId();
	}

	// Obtains a textual list of all directors
	public List<String> getDirectors() {
		// Creates a query using the Persistence Query language
		Query query = entityManager.createQuery("SELECT d from Director as d");
		// Creates an empty list with reserved size
		List<String> lst = new ArrayList<String>(query.getResultList().size());
		// Fill the list with directors' names
		for (Director d : (List<Director>) query.getResultList()) {
			lst.add(d.getName());
		}
		return lst;
	}

	// Obtains a textual list of all directors and their movies
	public List<String> getDirectorsWithMovies() {
		// Creates a query using the Persistence Query language
		Query query = entityManager.createQuery("SELECT d from Director as d");
		// Creates an empty list with reserved size
		List<String> lst = new ArrayList<String>();
		// Fill the list
		for (Director d : (List<Director>) query.getResultList()) {
			// Get all movies of the director
			Collection<Movie> movies = d.getMovies();
			for (Movie m : movies) {
				lst.add(d.getName() + ": " + m.getTitle());
			}
		}
		return lst;
	}
}
