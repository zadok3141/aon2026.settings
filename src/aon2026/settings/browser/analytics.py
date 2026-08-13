"""Environment-gated web-statistics viewlets.

The GA snippet lives in the ZODB (Site control panel -> plone.webstats_js /
plone.webstats_head_js), and dev/test databases are seeded from production
backups — so the production tag rides in with every restore. These overrides
consult the runtime environment instead of trusting the database:

- AON_SITE_ENV == "production": render the registry value as stock Plone does.
- anything else (including unset — e.g. a bare test run): suppress the
  registry value and render AON_WEBSTATS_JS / AON_WEBSTATS_HEAD_JS instead,
  which default to empty. A test server can carry its own tag there.

AON_SITE_ENV is injected by the deployment's instance configuration
(buildout ``environment-vars`` in the aon2026 repo's rollout configs).

Ported from oag2026.settings (task/ga-env-gate, 2026-08-13).
"""

from plone.app.layout.analytics.view import AnalyticsHeadViewlet
from plone.app.layout.analytics.view import AnalyticsViewlet

import os


class EnvGateMixin:
    """Render the registry value only in production; else the env fallback."""

    fallback_env_var = "AON_WEBSTATS_JS"

    @property
    def webstats_js(self):
        if os.environ.get("AON_SITE_ENV") == "production":
            return super().webstats_js
        return os.environ.get(self.fallback_env_var, "")


class EnvGatedAnalyticsViewlet(EnvGateMixin, AnalyticsViewlet):
    """Footer webstats viewlet (plone.analytics), production-gated."""


class EnvGatedAnalyticsHeadViewlet(EnvGateMixin, AnalyticsHeadViewlet):
    """Head webstats viewlet (plone.analytics.head), production-gated."""

    fallback_env_var = "AON_WEBSTATS_HEAD_JS"
