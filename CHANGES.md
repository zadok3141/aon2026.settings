# Changelog

## 1.0.2 (unreleased)

- Add `area` to the HTML filter's valid tags (`plone.valid_tags`, appended
  with `purge="False"` so Plone's defaults stay), so image-map hotspots in
  intranet content survive saving in TinyMCE (profile 1002 -> 1003, upgrade
  step re-imports the registry). `map` was already in the default list; only
  `area` was missing (ANS-2).

- Replace the `New website goes here` placeholder site action with
  `audit-office` — "The Audit Office website", pointing at
  `https://ao.parliament.nz/` (profile 1001 -> 1002, upgrade step re-imports
  `actions`). Backported from production, which had already been corrected by
  hand; the profile was the stale copy. `remove="True"` clears the placeholder
  from sites that installed the older profile. Completes the package's half of
  the 2026-08 domain migration (ANS-1): the audit found one other
  `oag.parliament.nz` mention, in this changelog's 1.0.1 entry, which is
  history and is kept deliberately.

- Set the site-wide easyform upload limit (`easyform.max_filesize`) to
  25,000,000 bytes and declare `collective.easyform` as a package and
  profile dependency (profile 1000 -> 1001, upgrade step re-imports the
  registry). Postfix `message_size_limit` on the host must be at least
  35 MB to match, or form mail is lost silently at commit.

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
