import webbrowser


def open_browser_url(url: str) -> str | None:
    """Open a URL in the default web browser."""
    try:
        webbrowser.open(url)
    except Exception as e:
        return f"Failed to open browser: {str(e)}. Open the URL manually {url}"
