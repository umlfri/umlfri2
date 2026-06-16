# TASKS

## Global rules for every task

- Modify only files under `stubs/merged`.
- Never delete `stubs/stubgen`, `stubs/monkeytype`, or `stubs/merged`.
- Never delete whole packages or directories.
- Do not modify runtime `.py` files.
- Do not change public API unless explicitly required by the task prompt.
- Keep the task limited to the package or package group listed in the task.
- If a file has no corresponding input from the relevant source, leave it unchanged.
- After finishing the task, stop and report what was changed.

## Package groups

- Group A: `umlfri2.application`
- Group B: `umlfri2.ufl.components`
- Group C: the rest of `umlfri2.ufl`, excluding `umlfri2.ufl.components`
- Group D: `umlfri2.qtgui`
- Group E: the rest of `umlfri2`, excluding:
  - `umlfri2.application`
  - `umlfri2.ufl`
  - `umlfri2.qtgui`

---

# Phase 1: Apply MonkeyType

## T1

Use `apply-monkeytype.prompt.md`.

Apply MonkeyType types only to Group A: `umlfri2.application`.

## T2

Use `apply-monkeytype.prompt.md`.

Apply MonkeyType types only to Group B: `umlfri2.ufl.components`.

## T3

Use `apply-monkeytype.prompt.md`.

Apply MonkeyType types only to Group C: the rest of `umlfri2.ufl`, excluding `umlfri2.ufl.components`.

## T4

Use `apply-monkeytype.prompt.md`.

Apply MonkeyType types only to Group D: `umlfri2.qtgui`.

## T5

Use `apply-monkeytype.prompt.md`.

Apply MonkeyType types only to Group E: the rest of `umlfri2`, excluding `umlfri2.application`, `umlfri2.ufl`, and `umlfri2.qtgui`.

---

# Phase 2: Normalize imports

## T6

Use `normalize-imports.prompt.md`.

Normalize imports only in Group A: `umlfri2.application`.

## T7

Use `normalize-imports.prompt.md`.

Normalize imports only in Group B: `umlfri2.ufl.components`.

## T8

Use `normalize-imports.prompt.md`.

Normalize imports only in Group C: the rest of `umlfri2.ufl`, excluding `umlfri2.ufl.components`.

## T9

Use `normalize-imports.prompt.md`.

Normalize imports only in Group D: `umlfri2.qtgui`.

## T10

Use `normalize-imports.prompt.md`.

Normalize imports only in Group E: the rest of `umlfri2`, excluding `umlfri2.application`, `umlfri2.ufl`, and `umlfri2.qtgui`.

---

# Phase 3: Cleanup stubs

## T11

Use `cleanup-stubs.prompt.md`.

Clean up stubs only in Group A: `umlfri2.application`.

## T12

Use `cleanup-stubs.prompt.md`.

Clean up stubs only in Group B: `umlfri2.ufl.components`.

## T13

Use `cleanup-stubs.prompt.md`.

Clean up stubs only in Group C: the rest of `umlfri2.ufl`, excluding `umlfri2.ufl.components`.

## T14

Use `cleanup-stubs.prompt.md`.

Clean up stubs only in Group D: `umlfri2.qtgui`.

## T15

Use `cleanup-stubs.prompt.md`.

Clean up stubs only in Group E: the rest of `umlfri2`, excluding `umlfri2.application`, `umlfri2.ufl`, and `umlfri2.qtgui`.
