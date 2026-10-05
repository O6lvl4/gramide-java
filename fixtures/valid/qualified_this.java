// Qualified enclosing-instance expressions preserve the original UTF-8 bytes.
class Outer {
    int value;
    void clear() { value = 0; }
    class Inner {
        void reset() { Outer.this.clear(); }
        Outer owner() { return Outer.this; }
        int read() { return Outer.this.value; }
        class Deep {
            Inner owner() { return Outer.Inner.this; }
        }
    }
}
class 外側 {
    class 内側 { 外側 owner() { return 外側.this; } }
}
