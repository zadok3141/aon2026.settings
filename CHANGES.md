# Changelog

## 1.0.2 (unreleased)


- Update docs (CLAUDE.md, .knowledge.yml) for the site domain rename
  audit.oag.net -> intranet.ao.parliament.nz.


## 1.0.1 (2026-08-31)

- Seed `docs/backlog.org` (ID prefix `ANS`) and declare the project's
  knowledge-program topics in `.knowledge.yml`. First item ANS-1: audit the
  package for lingering `oag.parliament.nz` / `oag.govt.nz` references left
  over from the 2026-08 domain migration (one known hit in
  `profiles/default/actions.xml`).

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
