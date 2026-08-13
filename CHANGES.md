# Changelog

## 1.0.1 (unreleased)

- Gate the web-statistics viewlets (`plone.analytics`, `plone.analytics.head`)
  on `AON_SITE_ENV`: the registry GA snippet renders only when
  `AON_SITE_ENV=production`; other environments render `AON_WEBSTATS_JS` /
  `AON_WEBSTATS_HEAD_JS` (default empty), so a dev/test database restored
  from a production backup cannot ship the production tag. The deployment
  must set `AON_SITE_ENV=production` (buildout `environment-vars`) before
  this ships to production, or the prod tag stops rendering.

- Move the site from-address to `webmaster@ao.parliament.nz` in the registry
  profile and the comment-added content rule, matching the value applied to
  the live site by the 2026-08 email domain migration. (Recreates the change
  from the lost `feature/email-domain-ao` branch.)


## 1.0.0a0 (2026-05-25)


# Initial launch state May 2026.
