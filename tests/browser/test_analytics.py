"""Environment-gated web-statistics viewlets.

The registry GA snippet (Site control panel) must only render when
AON_SITE_ENV=production — dev/test databases are restored from production
backups, so the production tag is always present in the data.
"""

from aon2026.settings.browser.analytics import EnvGatedAnalyticsHeadViewlet
from aon2026.settings.browser.analytics import EnvGatedAnalyticsViewlet
from aon2026.settings.interfaces import IBrowserLayer
from plone.app.layout.viewlets.interfaces import IHtmlHead
from plone.app.layout.viewlets.interfaces import IPortalFooter
from plone.registry.interfaces import IRegistry
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.viewlet.interfaces import IViewlet

import pytest


PROD_TAG = "<script>gtag-PRODUCTION</script>"
TEST_TAG = "<script>gtag-TEST</script>"


@implementer(IPortalFooter)
class DummyFooterManager:
    pass


@implementer(IHtmlHead)
class DummyHeadManager:
    pass


@pytest.fixture()
def prod_registry(portal):
    registry = getUtility(IRegistry)
    registry["plone.webstats_js"] = PROD_TAG
    registry["plone.webstats_head_js"] = PROD_TAG
    return registry


@pytest.fixture()
def footer_viewlet(portal):
    return EnvGatedAnalyticsViewlet(portal, portal.REQUEST, None, None)


@pytest.fixture()
def head_viewlet(portal):
    return EnvGatedAnalyticsHeadViewlet(portal, portal.REQUEST, None, None)


class TestEnvGate:
    def test_production_renders_registry_value(
        self, monkeypatch, prod_registry, footer_viewlet
    ):
        monkeypatch.setenv("AON_SITE_ENV", "production")
        assert footer_viewlet.webstats_js == PROD_TAG
        assert PROD_TAG in footer_viewlet.render()

    def test_non_production_suppresses_registry_value(
        self, monkeypatch, prod_registry, footer_viewlet
    ):
        monkeypatch.setenv("AON_SITE_ENV", "test")
        monkeypatch.delenv("AON_WEBSTATS_JS", raising=False)
        assert footer_viewlet.webstats_js == ""
        assert PROD_TAG not in footer_viewlet.render()

    def test_unset_env_suppresses_registry_value(
        self, monkeypatch, prod_registry, footer_viewlet
    ):
        monkeypatch.delenv("AON_SITE_ENV", raising=False)
        monkeypatch.delenv("AON_WEBSTATS_JS", raising=False)
        assert footer_viewlet.webstats_js == ""

    def test_non_production_env_override_tag(
        self, monkeypatch, prod_registry, footer_viewlet
    ):
        monkeypatch.setenv("AON_SITE_ENV", "test")
        monkeypatch.setenv("AON_WEBSTATS_JS", TEST_TAG)
        assert footer_viewlet.webstats_js == TEST_TAG
        assert TEST_TAG in footer_viewlet.render()

    def test_head_viewlet_production(self, monkeypatch, prod_registry, head_viewlet):
        monkeypatch.setenv("AON_SITE_ENV", "production")
        assert head_viewlet.webstats_js == PROD_TAG
        assert PROD_TAG in head_viewlet.render()

    def test_head_viewlet_non_production(
        self, monkeypatch, prod_registry, head_viewlet
    ):
        monkeypatch.setenv("AON_SITE_ENV", "test")
        monkeypatch.delenv("AON_WEBSTATS_HEAD_JS", raising=False)
        assert head_viewlet.webstats_js == ""
        assert PROD_TAG not in head_viewlet.render()

    def test_head_viewlet_env_override_tag(
        self, monkeypatch, prod_registry, head_viewlet
    ):
        monkeypatch.setenv("AON_SITE_ENV", "test")
        monkeypatch.setenv("AON_WEBSTATS_HEAD_JS", TEST_TAG)
        assert head_viewlet.webstats_js == TEST_TAG


class TestRegistration:
    """Our layer-specific registrations shadow the stock plone.app.layout ones."""

    def _lookup(self, portal, name, manager):
        request = portal.REQUEST
        alsoProvides(request, IBrowserLayer)
        view = BrowserView(portal, request)
        return getMultiAdapter((portal, request, view, manager), IViewlet, name=name)

    def test_footer_viewlet_registered(self, portal):
        viewlet = self._lookup(portal, "plone.analytics", DummyFooterManager())
        assert isinstance(viewlet, EnvGatedAnalyticsViewlet)

    def test_head_viewlet_registered(self, portal):
        viewlet = self._lookup(portal, "plone.analytics.head", DummyHeadManager())
        assert isinstance(viewlet, EnvGatedAnalyticsHeadViewlet)
