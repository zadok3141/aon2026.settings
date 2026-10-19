from aon2026.settings.setuphandlers.session import SESSION_PROPERTIES
from aon2026.settings.upgrades.session import configure_session_lifetime


class TestSessionUpgrade:
    def test_upgrade_sets_session_properties(self, portal):
        """The 1003 -> 1004 step moves a site off Plone's defaults (AN-52)."""
        session = portal.acl_users.session
        session.manage_changeProperties(
            timeout=7200, refresh_interval=3600, cookie_lifetime=0, secure=False
        )
        configure_session_lifetime(portal.portal_setup)
        for name, value in SESSION_PROPERTIES.items():
            assert session.getProperty(name) == value

    def test_upgrade_installs_refresh_support(self, portal, installer):
        """The step installs Session refresh support where it is missing."""
        installer.uninstall_product("plone.session")
        assert installer.is_product_installed("plone.session") is False
        configure_session_lifetime(portal.portal_setup)
        assert installer.is_product_installed("plone.session") is True
