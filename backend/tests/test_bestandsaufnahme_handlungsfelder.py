"""Tests zu den Handlungsfeldern der Bestandsaufnahme (T-1170, Vorhaben T-1160)."""
from app.data import catalog
from app.data.kang_handlungsfelder import handlungsfeld_fuer_risiko
from app.services.bestandsaufnahme_handlungsfelder import handlungsfelder_im_katalog
from app.services.bestandsaufnahme_markdown import bestandsaufnahme_markdown
from app.services.bestandsaufnahme_service import bestandsaufnahme_aus_daten


def test_alle_felder_des_katalogs_stehen_drin():
    erwartet = [(c["code"], f["code"]) for c in catalog.KANG_CLUSTERS for f in c["fields"]]
    assert [(x["cluster"], x["feld"]) for x in handlungsfelder_im_katalog()] == erwartet
    assert len(erwartet) == 17


def test_status_folgt_den_risiken():
    belegt = {handlungsfeld_fuer_risiko(r["code"]) for r in catalog.RISKS}
    for x in handlungsfelder_im_katalog():
        im = (x["cluster"], x["feld"]) in belegt
        assert (x["status"] == "im Katalog") == im
        assert bool(x["risiken"]) == im


def test_jedes_risiko_landet_in_genau_einem_feld():
    alle = [c for x in handlungsfelder_im_katalog() for c in x["risiken"]]
    assert sorted(alle) == sorted(r["code"] for r in catalog.RISKS)


def test_markdown_hat_abschnitt_einmal_mit_allen_labels():
    t = bestandsaufnahme_markdown(
        {"kommune_id": 1, "name": "X", "groessen": bestandsaufnahme_aus_daten([], {})}
    )
    assert t.count("## Handlungsfelder") == 1
    assert "schätzt sie selbst ein" in t
    assert all(x["label"] in t for x in handlungsfelder_im_katalog())
