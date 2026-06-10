uv run --python=3.11 --with monkeytype monkeytype list-modules |
    ForEach-Object {
        $path = "stubs\monkeytype\" + ($_.Replace('.', '\')) + ".pyi"
        New-Item -ItemType Directory -Force (Split-Path $path) | Out-Null
        uv run --python=3.11 --with monkeytype monkeytype stub $_ | Set-Content $path
    }
