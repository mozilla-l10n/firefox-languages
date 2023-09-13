# Curated list of native languages for Firefox UI

This repository hosts a set of scripts, JSON files, and HTML pages used to
generate and manage a list of native names for languages to use in Firefox UI
(see [bug 1481729](https://bugzilla.mozilla.org/show_bug.cgi?id=1481729))

## Updating or adding locales

### Extract information from builds, CLDR and Transvision

To add missing locales, use `scripts/generate_list.py`. This script retrieves
the list of locales included in builds of Firefox Desktop and Firefox for
Android, extracts the information for each locale from CLDR, and extracts
translations from Transvision.

It’s expected to see some errors reported, for example:

```
Error retrieving translations for ca-valencia
https://transvision.flod.org/api/v1/entity/gecko_strings/?id=toolkit/toolkit/intl/languageNames.ftl:language-name-ca-valencia
```

This is because the language name is not defined in `languageNames.ftl`.

The script includes a couple of mappings:
* `locale_map`: this is used to map a Mozilla code to a CLDR code (e.g. `fy-NL`
  to `fy`).
* `transvision_map`: this is used to map a Transvision code to a code used in
  `languageNames.ftl` (e.g. `bn-BD` to `bn`).

The script will only update `output/languages.json`.

### Update curated names

If a new locale has been added, the curated language name needs to be manually
added to `output/languages_curated.json`.

### Generate HTML output

Run `scripts/convert_to_html.py` to generate HTML files used in GitHub pages.
The updated files will be stored in the `docs` folder.
