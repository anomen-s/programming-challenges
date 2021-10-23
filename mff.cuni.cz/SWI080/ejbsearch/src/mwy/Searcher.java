package mwy;

public interface Searcher
{
	public static final int DISTANCE_INFINITE = -1;
	public int getDistance (int nodeFrom, int nodeTo);
	public int addNode();
	public void connectNodes(int nodeFrom, int nodeTo);
}
