from textwrap import dedent


def missing_dependency_message(error: ModuleNotFoundError, install_command: str) -> str:
    return dedent(
        f"""
        Missing Python package: `{error.name}`.

        Install the required dependencies with:

        ```bash
        {install_command}
        ```
        """
    ).strip()
