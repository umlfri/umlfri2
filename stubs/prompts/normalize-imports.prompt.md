# Task

Normalize imports in all `.pyi` files in `stubs/merged`.

# Rules

1. Do not change any types, function signatures, or class members.
2. Do not change the public API.
3. Remove all unused imports.
4. Remove duplicate imports.
5. Merge imports from the same module into a single import statement.
6. Use only single-line imports.
7. Never use multi-line imports.
8. Remove redundant aliases such as `X as X`.
9. Preserve the existing import style unless it violates the rules above.
10. If both relative and absolute imports are possible, prefer the style already used in the file.
11. The resulting `.pyi` file must be syntactically valid Python.
12. The resulting `.pyi` file must be compatible with Pyright.
