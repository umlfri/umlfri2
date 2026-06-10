$root = (Resolve-Path .).Path

$files =
    Get-ChildItem $root -Recurse -Filter *.py |
    Where-Object { $_.FullName -like "*\umlfri2\*" } |
    Where-Object { $_.Name -ne "__init__.py" } |
    ForEach-Object {
        $_.FullName.Substring($root.Length + 1).Replace('\', '.').Replace('/', '.').Replace('.py', '')
    }

$modules = uv run --python=3.11 --with monkeytype monkeytype list-modules

Compare-Object $files $modules
