import json
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from image_inbox import approve_draft, draft_source, iter_images
from knowledge_index import build_index


ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "vault"
WEB = ROOT / "web"
DRAFTS = VAULT / "00_inbox" / "_source_drafts"


def safe_project_path(value):
    path = (ROOT / value).resolve()
    if ROOT not in path.parents and path != ROOT:
        raise ValueError("path escapes project root")
    return path


def read_text_file(value):
    path = safe_project_path(value)
    return path.read_text(encoding="utf-8")


def list_drafts():
    if not DRAFTS.exists():
        return []
    return [
        {"path": path.relative_to(ROOT).as_posix(), "name": path.name}
        for path in sorted(DRAFTS.glob("*.md"))
    ]


def api_status():
    records, errors, warnings = build_index()
    counts = {"source": 0, "card": 0, "skill": 0, "bundle": 0}
    for record in records:
        counts[record.get("type", "")] = counts.get(record.get("type", ""), 0) + 1
    return {
        "counts": counts,
        "drafts": len(list_drafts()),
        "inbox_images": len(list(iter_images())),
        "errors": errors,
        "warnings": warnings,
    }


def api_index(kind=None):
    records, errors, warnings = build_index()
    if kind:
        records = [record for record in records if record.get("type") == kind]
    return {"records": records, "errors": errors, "warnings": warnings}


def api_inbox_images():
    return [
        {"path": path.relative_to(ROOT).as_posix(), "name": path.name}
        for path in iter_images()
    ]


def json_response(handler, payload, status=200):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(data)))
    handler.end_headers()
    handler.wfile.write(data)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        try:
            if parsed.path == "/api/status":
                return json_response(self, api_status())
            if parsed.path == "/api/index":
                return json_response(self, api_index(query.get("type", [None])[0]))
            if parsed.path == "/api/drafts":
                return json_response(self, {"drafts": list_drafts()})
            if parsed.path == "/api/inbox-images":
                return json_response(self, {"images": api_inbox_images()})
            if parsed.path == "/api/file":
                return json_response(self, {"text": read_text_file(query["path"][0])})
            return self.serve_static(parsed.path)
        except Exception as exc:
            return json_response(self, {"error": str(exc)}, status=500)

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
            if self.path == "/api/draft-image":
                path = draft_source(payload["path"])
                return json_response(self, {"path": path.relative_to(ROOT).as_posix()})
            if self.path == "/api/approve-draft":
                path = approve_draft(payload["path"])
                return json_response(self, {"path": path.relative_to(ROOT).as_posix()})
            return json_response(self, {"error": "unknown endpoint"}, status=404)
        except Exception as exc:
            return json_response(self, {"error": str(exc)}, status=500)

    def serve_static(self, path):
        if path == "/":
            path = "/index.html"
        file_path = (WEB / path.lstrip("/")).resolve()
        if WEB not in file_path.parents and file_path != WEB:
            self.send_error(403)
            return
        if not file_path.exists():
            self.send_error(404)
            return
        data = file_path.read_bytes()
        content_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format, *args):
        return


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 8765), Handler)
    print("Prajnavex web UI: http://127.0.0.1:8765")
    server.serve_forever()


if __name__ == "__main__":
    main()
