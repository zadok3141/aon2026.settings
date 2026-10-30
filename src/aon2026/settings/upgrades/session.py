from aon2026.settings.setuphandlers.session import configure_session
from plone import api
from plone.base.utils import get_installer


def configure_session_lifetime(setup_tool):
    """Upgrade 1003 -> 1004: Session refresh support and the session values.

    Both intranet instances were set this way by hand on 2026-10-19 (AN-52),
    so on those sites this step changes nothing.
    """
    portal = api.portal.get()
    installer = get_installer(portal)
    if not installer.is_product_installed("plone.session"):
        installer.install_product("plone.session")
    configure_session(portal)
