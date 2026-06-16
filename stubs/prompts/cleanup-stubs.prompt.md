# Task

Clean up and fix `.pyi` files in `stubs/merged` without changing the public API.

# Rules

1. Do not modify types that were obtained from monkeytype.
2. Do not change the public API.
3. Do not add new functions, classes, or exports.
4. Do not remove existing functions, classes, or exports.

# Incomplete

1. Never use `_typeshed.Incomplete`.
2. Remove all imports of `_typeshed.Incomplete`.
3. If a better type can be determined from existing code or monkeytype output, use that type.
4. Replace every occurrence of `Incomplete` with `Any`.
5. Add any required imports.

# Validation
1. The resulting `.pyi` file must be syntactically valid Python.
2. The resulting `.pyi` file must be compatible with Pyright.
