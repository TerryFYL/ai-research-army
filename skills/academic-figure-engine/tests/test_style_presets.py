"""Regression tests for style_presets.create_style_template.

The documented contract of create_style_template is a .mplstyle file that
matplotlib.style.use() loads correctly. These tests assert that contract:
the generated file must apply the colorblind-friendly color cycle and the
full base style when loaded.
"""

import os
import sys

import matplotlib

matplotlib.use("Agg")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import matplotlib.pyplot as plt

from style_presets import OKABE_ITO_COLORS, create_style_template, get_base_style


def test_create_style_template_creates_usable_mplstyle(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    create_style_template("publication.mplstyle")

    template = tmp_path / "publication.mplstyle"
    assert template.exists()

    base = get_base_style()
    with plt.style.context(str(template)):
        rc = matplotlib.rcParams
        # The palette must actually load. '#' starts a comment in .mplstyle
        # files, so emitting '#RRGGBB' silently drops the whole cycler line.
        assert rc["axes.prop_cycle"].by_key()["color"] == OKABE_ITO_COLORS
        # List values must serialize comma-separated, not as Python reprs
        # (a repr like "['Arial', ...]" loads as garbage font names).
        assert rc["font.sans-serif"] == base["font.sans-serif"]
        # Scalar and boolean values must round-trip.
        assert rc["font.size"] == base["font.size"]
        assert rc["savefig.dpi"] == base["savefig.dpi"]
        assert rc["axes.spines.top"] == base["axes.spines.top"]
