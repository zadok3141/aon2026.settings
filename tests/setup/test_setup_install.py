from aon2026.settings import PACKAGE_NAME


class TestSetupInstall:
    def test_addon_installed(self, installer):
        """Test if aon2026.settings is installed."""
        assert installer.is_product_installed(PACKAGE_NAME) is True

    def test_browserlayer(self, browser_layers):
        """Test that IBrowserLayer is registered."""
        from aon2026.settings.interfaces import IBrowserLayer

        assert IBrowserLayer in browser_layers

    def test_latest_version(self, profile_last_version):
        """Test latest version of default profile."""
        assert profile_last_version(f"{PACKAGE_NAME}:default") == "1001"

    def test_easyform_max_filesize(self, portal):
        """The site-wide easyform upload limit is 25 MB (OT-7, 2026-09-16)."""
        from plone import api

        assert api.portal.get_registry_record("easyform.max_filesize") == 25_000_000
