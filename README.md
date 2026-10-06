# gramide-java

An independent Java **core source reader** for gramide, version 0.1.0.
The package depends only on gramide v0.2.11. It supplies a byte-preserving
lexer, a recursive grammar, a committed compiled table, symbol rules, its
own CLI, and a small positive/negative regression corpus.

This is not a complete Java 25 parser or a compiler validation gate. It
advertises `tokens`, `parse`, `outline`, `symbols`, `tags`, and `map`.
It deliberately does **not** advertise `check` or `symbols-recovered`.
`symbols` requires a strict parse. The host's `parse` and `outline` commands
may recover damaged code, with diagnostics and ERROR nodes. Recovered output
is useful for navigation, not evidence that the source is valid Java.

## Covered core

- Package/import declarations, including static and wildcard imports
- Classes, interfaces, annotation interfaces, enums, records, nested types,
  modifiers and annotations; superclass/interface lists and permits clauses
- Generic type parameters, intersection bounds, qualified and nested generic
  type applications, wildcard extends/super arguments, arrays and varargs
- Fields with multiple declarators, methods, generic methods, constructors,
  compact record constructors, initializer blocks and annotation defaults
- Blocks, local declarations, if/else, while/do, traditional and enhanced for,
  return/throw/break/continue, labels, old-style switch labels, assert,
  synchronized, try/catch/finally, resource lists and multi-catch
- Precedence-aware arithmetic/boolean/bitwise/comparison expressions,
  assignment, ternaries, shifts, prefix/postfix operators, calls, field and
  index access, casts, lambdas, method references, constructor/array creation,
  diamond creation, anonymous class bodies and qualified enclosing-instance
  expressions such as `Outer.this.clear()`
- UTF-8 identifiers and original byte ranges, non-nesting comments, ordinary
  strings, character literals, text blocks, decimal/binary/octal/hex numbers,
  decimal and hexadecimal floating-point forms

## Deliberate limits

- Java Unicode-escape preprocessing is not implemented. Escaped identifiers,
  escaped keywords/delimiters and Unicode escapes that change lexical structure
  are unsupported. Escape spellings inside literal bodies are retained;
  they are not a substitute for Java's pre-tokenization translation
- Identifier category tables are pinned to Unicode **15.0.0**, generated from
  Python's Unicode database, not the current JDK's Character tables. Ignorable
  ASCII controls in identifiers and characters introduced later are unsupported
- Modules, Java 25 compact compilation units/instance main methods, preview
  features, switch expressions/arrow cases and patterns, record patterns,
  type-use annotations and receiver parameters are not covered
- Non-sealed spelling, intersection casts, primitive/array class literals and
  generic inner-class creation requiring type arguments on multiple segments
  are outside the tested core
- This is syntax-oriented: declaration placement/order, modifier legality,
  constructor/type-name equality, varargs placement, l-values, expression-
  statement restrictions, resource validity, numeric overflow and semantic
  escape values are not compiler-validated
- `>` is tokenized individually so nested generics work. Joined shift and
  `>=` operators do not currently require byte adjacency
- Symbol names are lexical. Package declarations are not prepended to class
  names; nested named types are. Constructors use `Type.Type`. Field ranges
  inherit the declaration prefix and end at that declarator, before `;`.
  Record components are parameters, not synthesized fields/accessors. No
  implicit members are invented. Anonymous-class methods have no generated
  anonymous-owner identity and remain under the enclosing named type
- A javac parse-only oracle checks the positive and malformed fixtures. It
  does not type-check source or prove representative-repository acceptance.
  The checked-in corpus proves these examples, not complete Java conformance

## Build and verify

Run from this package directory with Almide 0.62.0 or a compatible compiler
and Java 17+ with the `jdk.compiler` module for the fixture oracle:

```sh
almide build cli/main.almd -o gramide_java
./gramide_java symbols fixtures/valid/model.java
./gramide_java outline fixtures/valid/statements.java
./gramide_java gen-table > src/table.almd
ci/check.sh
```

`ci/check.sh` type-checks, runs the Almide tests, rebuilds the CLI, verifies
that `gen-table` exactly reproduces the committed table, and checks the
fixture manifest. `ci/verify.py` checks every expected symbol name and byte/
line span, exercises the reading commands, and requires every malformed
fixture to fail strict symbols without JSON output. The tests also compare
dynamic grammar and committed-table trees and check Unicode/comment/literal
edge cases. `ci/generate_unicode.py` reproduces the category data when run
with Python's Unicode 15.0.0 database.

## Sources

Original implementation informed by the [Java Language Specification,
Java SE 25](https://docs.oracle.com/javase/specs/jls/se25/html/index.html),
particularly lexical structure, classes/interfaces, statements and
expressions. No third-party parser grammar was copied.

Unicode category facts in `src/unicode.almd` derive from the
[Unicode 15.0.0 Character Database](https://www.unicode.org/Public/15.0.0/ucd/UnicodeData.txt)
via Python 3.12 `unicodedata`. They are redistributed with the full
`LICENSE-UNICODE` notice. The generator refuses any different database version.

Source line endings are LF or CRLF. Lone CR is refused in strict mode because
the pinned engine uses LF-based document line counts; this prevents inconsistent
complete symbol ranges for older-Mac or control-bearing source files.

## Repository contract

This repository owns this language package and its tests. `src/mod.almd` exports
`definition()` using the shared gramide package API. The `gramide-cli` repository
composes it as a git dependency; no grammar source is vendored into the CLI.
`bash ci/check.sh` runs the complete package gate with an explicit test entry
point, avoiding recursive parallel compiler fan-out. CI pins Almide and Rust
in `.github/workflows/quality.yml`.
