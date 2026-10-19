"""Session lifetime for logged-in editors (AN-52).

Plone's session plugin defaults to a 2-hour ticket and a cookie that dies with
the browser, which logged intranet editors out mid-edit. These are the values
every OAG site carries since 2026-10-19 (ao.parliament.nz since April 2026),
set by hand until this profile captured them.
"""

from plone import api


SESSION_PROPERTIES = {
    # Ticket validity in seconds. With Session refresh support installed the
    # ticket is renewed while the editor is active, so this is an idle limit.
    "timeout": 8 * 60 * 60,
    # The most often the browser re-asks the server for a renewal.
    "refresh_interval": 60 * 60,
    # Cookie expiry in days, so a browser restart keeps the login.
    "cookie_lifetime": 1,
    # Send the cookie over HTTPS only; Zope debug mode ignores this.
    "secure": True,
}


def configure_session(portal):
    """Apply SESSION_PROPERTIES to the site's session plugin."""
    portal.acl_users.session.manage_changeProperties(**SESSION_PROPERTIES)


def post_install(setup_tool):
    """Post-handler of the default profile."""
    configure_session(api.portal.get())
