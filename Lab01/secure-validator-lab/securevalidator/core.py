import re
import html


def validate_email(value: str) -> bool:
    pattern = r"^[\w\.\-]+@[\w\.\-]+\.\w+$"
    return bool(re.match(pattern, value.strip()))


def validate_url(value: str) -> bool:
    pattern = r"^https?://[\w\.\-]+(:\d+)?(/[\w\.\-@:%_\+~#=/?&]*)?$"
    return bool(re.match(pattern, value.strip()))


def validate_filename(value: str) -> bool:
    if ".." in value or "/" in value or "\\" in value:
        return False
    pattern = r"^[\w\-\.]+$"
    return bool(re.match(pattern, value.strip()))


def sanitize_sql_input(value: str) -> str:
    dangerous = [
        r"'\s*OR\s*", r"'\s*AND\s*", r"--", r";", r"/\*.*?\*/",
        r"\bDROP\b", r"\bDELETE\b", r"\bINSERT\b", r"\bUPDATE\b",
        r"\bSELECT\b", r"\bUNION\b", r"\bEXEC\b", r"'",
    ]
    result = value
    for pattern in dangerous:
        result = re.sub(pattern, "", result, flags=re.IGNORECASE)
    return result.strip()


def sanitize_html_input(value: str) -> str:
    return html.escape(value)
