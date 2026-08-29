from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator


async def run_command(command: list[str]) -> AsyncIterator[str]:
    """Yield merged stdout/stderr while keeping the TUI event loop responsive."""
    process = await asyncio.create_subprocess_exec(
        *command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT
    )
    assert process.stdout is not None
    try:
        async for line in process.stdout:
            yield line.decode(errors="replace")
        result = await process.wait()
        yield f"\nProcess exited with code {result}.\n"
    finally:
        if process.returncode is None:
            process.terminate()
            await process.wait()
