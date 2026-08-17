"""Tests für die gzip-Datei-Auslieferung mit ETag/If-None-Match → 304."""

from __future__ import annotations

import gzip
import json

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from app.api.gzip_files import file_etag, gzip_json_file_response, gzip_uncompressed_size


@pytest.fixture()
def gz_file(tmp_path):
    path = tmp_path / "artifact.json.gz"
    payload = {"hello": "welt", "n": 42}
    with gzip.open(path, "wt", encoding="utf-8") as fh:
        json.dump(payload, fh)
    return str(path), payload


@pytest.fixture()
def client(gz_file):
    path, _ = gz_file
    app = FastAPI()

    @app.get("/artifact")
    def artifact(request: Request):
        return gzip_json_file_response(request, path, etag='"da-test1"',
                                       download_name="artifact.json")

    # TestClient dekomprimiert Content-Encoding: gzip transparent
    return TestClient(app)


def test_200_with_etag_and_gzip_headers(client, gz_file):
    _, payload = gz_file
    r = client.get("/artifact")
    assert r.status_code == 200
    assert r.headers["etag"] == '"da-test1"'
    assert r.headers["cache-control"] == "no-cache"
    assert "x-uncompressed-length" in r.headers
    assert r.json() == payload


def test_matching_if_none_match_yields_304_without_body(client):
    r = client.get("/artifact", headers={"If-None-Match": '"da-test1"'})
    assert r.status_code == 304
    assert r.content == b""
    assert r.headers["etag"] == '"da-test1"'


def test_weak_and_list_etags_match(client):
    r = client.get("/artifact", headers={"If-None-Match": 'W/"da-test1"'})
    assert r.status_code == 304
    r = client.get("/artifact", headers={"If-None-Match": '"anders", "da-test1"'})
    assert r.status_code == 304


def test_stale_etag_yields_200(client):
    r = client.get("/artifact", headers={"If-None-Match": '"da-alt"'})
    assert r.status_code == 200


def test_uncompressed_size_and_file_etag(gz_file):
    path, payload = gz_file
    assert gzip_uncompressed_size(path) == len(json.dumps(payload).encode())
    etag = file_etag(path)
    assert etag.startswith('"f-') and etag.endswith('"')
