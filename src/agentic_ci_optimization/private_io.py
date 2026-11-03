"""Keep raw and derived provider evidence out of source-controlled directories."""
import json
import os
from pathlib import Path


def _private_target(raw):
    path = Path(raw).expanduser().absolute()
    parent = path.parent.resolve(strict=True)
    if not parent.is_dir():
        raise ValueError("output parent is not a directory")
    if path.exists() or path.is_symlink():
        raise ValueError("refuse to overwrite evidence")
    cursor = parent
    while True:
        if (cursor / ".git").exists():
            raise ValueError("evidence output must be outside Git worktrees")
        if cursor == cursor.parent:
            break
        cursor = cursor.parent
    return parent / path.name


def write_private_json(path, payload):
    target = _private_target(path)
    fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, sort_keys=True, indent=2)
            stream.write("\n")
    except BaseException:
        target.unlink(missing_ok=True)
        raise
    return target


def read_json(path):
    with open(path, encoding="utf-8") as stream:
        return json.load(stream)
