package demo.model;
import java.util.List;
import java.util.ArrayList;
/** A UTF-8 source fixture: 日本語 */
@Deprecated
public class Box<T extends Number & Comparable<T>> implements Iterable<T> {
    private final List<T> values = new ArrayList<>();
    public Box(T value) { values.add(value); }
    public T first() { return values.get(0); }
    public <U> U map(U value) throws Exception { return value; }
    public int sum(int start) {
        int total = start;
        for (int i = 0; i < values.size(); i++) { total += i; }
        for (T item : values) { if (item == null) continue; }
        while (total < 10) total++;
        do { total--; } while (total > 10);
        return total;
    }
    public static class Nested { public int value; }
}
interface View<T> { T first(); default boolean empty() { return false; } }
record Pair<T>(T first, T second) implements java.io.Serializable {}
enum Color { RED, GREEN, BLUE; public String label() { return this.toString(); } }
