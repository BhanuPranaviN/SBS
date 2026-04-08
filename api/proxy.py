import json
from http import HTTPStatus
from urllib import request as urllib_request

LAMBDA_URL = "https://uoizku3cbwixvtrnwldz7g5xvq0owbrt.lambda-url.ap-south-1.on.aws/"


def _response(status_code, body, content_type="application/json", extra_headers=None):
    headers = [
        ("Content-Type", content_type),
        ("Access-Control-Allow-Origin", "*"),
        ("Access-Control-Allow-Methods", "GET,POST,OPTIONS"),
        ("Access-Control-Allow-Headers", "Content-Type"),
        ("Content-Length", str(len(body))),
    ]
    if extra_headers:
        headers.extend(extra_headers)
    try:
        reason = HTTPStatus(status_code).phrase
    except ValueError:
        reason = "OK"
    return f"{status_code} {reason}", headers, [body]


def _proxy(method, query_string, body=b"", content_type="application/json"):
    target_url = LAMBDA_URL
    if query_string:
        target_url += "?" + query_string

    headers = {"Content-Type": content_type}
    request = urllib_request.Request(target_url, data=body if method == "POST" else None, method=method, headers=headers)

    with urllib_request.urlopen(request, timeout=30) as response:
        payload = response.read()
        content_type = response.headers.get("Content-Type", "application/json")
        return _response(response.status, payload, content_type)


def app(environ, start_response):
    method = environ.get("REQUEST_METHOD", "GET").upper()
    query_string = environ.get("QUERY_STRING", "")

    try:
        if method == "OPTIONS":
            status, headers, body = _response(200, b"")
            start_response(status, headers)
            return body

        if method == "GET":
            status, headers, body = _proxy("GET", query_string)
            start_response(status, headers)
            return body

        if method == "POST":
            content_length = int(environ.get("CONTENT_LENGTH") or 0)
            body = environ["wsgi.input"].read(content_length) if content_length else b""
            content_type = environ.get("CONTENT_TYPE", "application/json")
            status, headers, response_body = _proxy("POST", query_string, body=body, content_type=content_type)
            start_response(status, headers)
            return response_body

        payload = json.dumps({"message": "Method not allowed"}).encode("utf-8")
        status, headers, body = _response(405, payload)
        start_response(status, headers)
        return body

    except urllib_request.HTTPError as exc:
        payload = exc.read()
        status, headers, body = _response(exc.code, payload, exc.headers.get("Content-Type", "application/json") if exc.headers else "application/json")
        start_response(status, headers)
        return body
    except Exception as exc:
        payload = json.dumps({"message": "Proxy request failed", "error": str(exc)}).encode("utf-8")
        status, headers, body = _response(502, payload)
        start_response(status, headers)
        return body
