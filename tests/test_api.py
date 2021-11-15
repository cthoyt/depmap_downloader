# -*- coding: utf-8 -*-

"""Test the API."""

import unittest

from depmap_downloader import get_achilles_gene_dependencies_url


class TestAPI(unittest.TestCase):
    """Test the API."""

    def test_get_achilles(self):
        """Test getting the achilles URL."""
        url = get_achilles_gene_dependencies_url(version="DepMap Public 21Q4")
        self.assertEqual("https://ndownloader.figshare.com/files/31315828", url)
