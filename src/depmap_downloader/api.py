# -*- coding: utf-8 -*-

"""Main code."""

from functools import lru_cache
from pathlib import Path
from typing import Optional

import pystow
import requests

__all__ = [
    "URL",
    "get_downloads_table",
    "crispr_gene_dependencies_url",
    "ensure_crispr_gene_dependencies",
    "get_achilles_gene_dependencies_url",
    "ensure_achilles_gene_dependencies",
]

URL = "https://depmap.org/portal/download/api/downloads"


@lru_cache(1)
def get_downloads_table():
    """Get the full downloads table from the secret API."""
    return requests.get(URL).json()


DEPMAP_MODULE = pystow.module("bio", "depmap")
ACHILLES_NAME = "Achilles_gene_dependency.csv"
CRISPR_NAME = "CRISPR_gene_dependency.csv"


@lru_cache(1)
def get_latest() -> str:
    """Get the latest release name."""
    latest = next(release for release in get_downloads_table() if release["isLatest"])
    return latest["releaseName"]


def _help_download(name: str, version: Optional[str] = None) -> str:
    if version is None:
        version = get_latest()
    for download in get_downloads_table()["table"]:
        if download["fileName"] == name and download["releaseName"] == version:
            return download["downloadUrl"]
    raise ValueError


def crispr_gene_dependencies_url(version: Optional[str] = None) -> str:
    """Get the CRISPR gene dependencies file URL."""
    return _help_download(CRISPR_NAME, version=version)


def ensure_crispr_gene_dependencies(version: Optional[str] = None, force: bool = False) -> Path:
    """Ensure the CRISPR gene dependencies file is downloaded."""
    if version is None:
        version = get_latest()
    return DEPMAP_MODULE.ensure(
        version,
        url=crispr_gene_dependencies_url(version=version),
        force=force,
        name=CRISPR_NAME,
    )


def get_achilles_gene_dependencies_url(version: Optional[str] = None) -> str:
    """Get the Achilles gene dependencies file URL."""
    return _help_download(ACHILLES_NAME, version=version)


def ensure_achilles_gene_dependencies(version: Optional[str] = None, force: bool = False) -> Path:
    """Ensure the Achilles gene dependencies file is downloaded."""
    if version is None:
        version = get_latest()
    return DEPMAP_MODULE.ensure(
        version,
        url=get_achilles_gene_dependencies_url(version=version),
        name=ACHILLES_NAME,
        force=force,
    )
