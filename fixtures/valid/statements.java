class Worker {
    private int count = 0, limit = 3;
    private String café = "hello \\ world";
    private char mark = '\n';
    private String block = """
        class Invisible { }
        東京
        """;
    public Worker() { this(1); }
    public Worker(int start) { this.count = start; }
    public int run() {
        Runnable callback = () -> { count++; };
        java.util.function.Function<Integer,Integer> add = x -> x + 1;
        int[] numbers = new int[] {1, 2, 3};
        try (Resource input = open()) {
            synchronized (this) { callback.run(); }
        } catch (FirstException | SecondException error) { throw error; }
        finally { count = 0; }
        switch (count) { case 0: count++; break; default: return -1; }
        assert count >= 0 : "negative";
        return (count << 1) + (count >> 1);
    }
}
@interface Label { String value() default "x"; }
record Position(int x, int y) { public Position { if (x < 0) throw new IllegalArgumentException(); } }
class 東京 { public String 挨拶() { return "こんにちは"; } }
