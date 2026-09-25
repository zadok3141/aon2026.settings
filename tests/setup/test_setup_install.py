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
        assert profile_last_version(f"{PACKAGE_NAME}:default") == "1002"

    def test_easyform_max_filesize(self, portal):
        """The site-wide easyform upload limit is 25 MB (OT-7, 2026-09-16)."""
        from plone import api

        assert api.portal.get_registry_record("easyform.max_filesize") == 25_000_000

    def test_audit_office_site_action(self, portal):
        """The site action points at the Audit Office site (ANS-1, 2026-09-25)."""
        site_actions = portal.portal_actions.site_actions
        assert "audit-office" in site_actions.objectIds()
        action = site_actions["audit-office"]
        assert action.title == "The Audit Office website"
        assert action.url_expr == "string:https://ao.parliament.nz/"
        assert action.visible is True

    def test_no_placeholder_site_action(self, portal):
        """The 'New website goes here' placeholder is gone (ANS-1, 2026-09-25)."""
        site_actions = portal.portal_actions.site_actions
        assert "New website goes here" not in site_actions.objectIds()
