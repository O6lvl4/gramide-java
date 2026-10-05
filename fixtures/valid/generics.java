import java.util.*;
public interface Repository<K, V> extends AutoCloseable {
    Map<K, List<V>> read(List<? extends K> keys);
    void write(Map<? super K, ? extends List<V>> values) throws Exception;
}
abstract class Generic {
    protected abstract <T extends Comparable<T>> T choose(T left, T right);
    public Object make() { return new Runnable() { public void run() {} }; }
    public Class<?> type() { return String.class; }
    public long number() { return 0xFFL + 0b1010 + 077 + 1_000L; }
    public double floating() { return 1.25e-2 + 0x1.fp3; }
}
