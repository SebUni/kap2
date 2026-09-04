"""Tests für die Admin-Lese-Schnittstelle der Kontaktanfragen (Leads)."""

from __future__ import annotations

import json

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.routes.admin_leads import read_leads, router as admin_leads_router


def _write_lines(path, lines):
    with open(path, "w", encoding="utf-8") as fh:
        for line in lines:
            fh.write(line + "\n")


def test_missing_file_returns_empty_list(tmp_path):
    path = tmp_path / "leads.jsonl"
    assert read_leads(str(path)) == []


def test_newest_first(tmp_path):
    path = tmp_path / "leads.jsonl"
    _write_lines(path, [
        json.dumps({"ts": "1", "name": "erste"}),
        json.dumps({"ts": "2", "name": "zweite"}),
        json.dumps({"ts": "3", "name": "dritte"}),
    ])
    result = read_leads(str(path))
    assert [r["name"] for r in result] == ["dritte", "zweite", "erste"]


def test_limit_caps_result(tmp_path):
    path = tmp_path / "leads.jsonl"
    _write_lines(path, [json.dumps({"n": i}) for i in range(10)])
    result = read_leads(str(path), limit=3)
    assert len(result) == 3
    assert [r["n"] for r in result] == [9, 8, 7]


def test_broken_line_is_skipped(tmp_path):
    path = tmp_path / "leads.jsonl"
    _write_lines(path, [
        json.dumps({"name": "gültig-eins"}),
        "{das ist kein json",
        json.dumps({"name": "gültig-zwei"}),
    ])
    result = read_leads(str(path))
    assert len(result) == 2
    assert {r["name"] for r in result} == {"gültig-eins", "gültig-zwei"}


@pytest.fixture()
def client(tmp_path, monkeypatch):
    path = tmp_path / "leads.jsonl"
    _write_lines(path, [
        json.dumps({"ts": "1", "name": "erste"}),
        json.dumps({"ts": "2", "name": "zweite"}),
        json.dumps({"ts": "3", "name": "dritte"}),
    ])
    monkeypatch.setattr("app.api.routes.admin_leads.LEADS_FILE", str(path))

    app = FastAPI()
    app.include_router(admin_leads_router, prefix="/api/admin")
    return TestClient(app)


def test_endpoint_returns_gesamt(client):
    r = client.get("/api/admin/leads")
    assert r.status_code == 200
    data = r.json()
    assert data["gesamt"] == 3
    assert len(data["leads"]) == 3
