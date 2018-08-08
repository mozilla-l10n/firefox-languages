#! /usr/bin/env python3

import json
import os
from collections import OrderedDict
from urllib.request import urlopen


# This array is used to map a Mozilla code to CLDR, e.g.
# 'es-ES': 'es'
locale_map = {
    'bn-BD': 'bn',
    'en-US': 'en',
    'es-ES': 'es',
    'fy-NL': 'fy',
    'ga-IE': 'ga',
    'gu-IN': 'gu',
    'hi-IN': 'hi',
    'hy-AM': 'hy',
    'ja-JP-mac': 'ja',
    'nb-NO': 'nb',
    'ne-NP': 'ne',
    'nn-NO': 'nn',
    'pa-IN': 'pa',
    'pt-BR': 'pt',
    'sv-SE': 'sv',
    'zh-CN': 'zh-Hans',
    'zh-TW': 'zh-Hant',
}

# Map Firefox locales to locale code in languageNames.properties
transvision_map = {
    'bn-BD': 'bn',
    'bn-IN': 'bn',
    'en-CA': 'en',
    'en-GB': 'en',
    'en-US': 'en',
    'en-ZA': 'en',
    'es-AR': 'es',
    'es-CL': 'es',
    'es-ES': 'es',
    'es-MX': 'es',
    'fy-NL': 'fy',
    'ga-IE': 'ga',
    'ga-IE': 'ga',
    'gu-IN': 'gu',
    'hi-IN': 'hi',
    'hy-AM': 'hy',
    'ja-JP-mac': 'ja',
    'nb-NO': 'nb',
    'ne-NP': 'be',
    'nn-NO': 'nn',
    'pa-IN': 'pa',
    'pt-BR': 'pt',
    'pt-PT': 'pt',
    'sv-SE': 'sv',
    'zh-CN': 'zh',
    'zh-TW': 'zh',
}


def getShippingLocales():
    # Get the list of locales shipping in Firefox
    base = 'https://hg.mozilla.org/mozilla-central/raw-file/default/{}'
    locales_urls = [
        base.format('browser/locales/all-locales'),
        base.format('mobile/android/locales/all-locales'),
    ]

    shipping_locales = []
    for locales_url in locales_urls:
        try:
            with urlopen(locales_url) as response:
                output = response.readlines()
                for locale in output:
                    locale = locale.rstrip().decode()
                    shipping_locales.append(locale)
        except Exception as e:
            print(e)

    shipping_locales = list(set(shipping_locales))
    if 'en-US' not in shipping_locales:
        shipping_locales.append('en-US')
    shipping_locales.sort()

    return shipping_locales


def main():
    # Get the list of supported locales in Firefox and Firefox for Android
    shipping_locales = getShippingLocales()

    # Path to this script and node modules
    script_folder = os.path.abspath(os.path.dirname(__file__))
    node_folder = os.path.join(script_folder, os.path.pardir, 'node_modules')

    transvision_api = 'https://transvision.mozfr.org/api/v1/entity/' \
                      'gecko_strings/?id=toolkit/chrome/global/' \
                      'languageNames.properties:{}'

    languages = OrderedDict()
    for locale in shipping_locales:
        cldr_locale = locale_map.get(locale, locale)
        cldr_path_names = os.path.join(
            node_folder, 'cldr-localenames-full', 'main', cldr_locale)

        # Initialize data structure for this language
        languages[locale] = {
            'cldr-available': True,
            'cldr-name': '---',
            'mozilla-name': '---',
            'transform-type': '---',
            'transformed-name': '---',
        }

        # Get translation from Transvision
        try:
            url = transvision_api.format(transvision_map.get(locale, locale))
            with urlopen(url) as response:
                json_data = json.load(response)
                if locale in json_data:
                    languages[locale]['mozilla-name'] = json_data[locale]
        except Exception as e:
            print('Error retrieving translations for {}'.format(locale))
            print(url)
            print(e)

        # Check if a folder for this locale exists in CLDR
        if not os.path.isdir(cldr_path_names):
            languages[locale]['cldr-available'] = False
            continue

        '''
        Read transform from CLDR. Possible values are
        - 'titlecase-firstword': title case
        - 'no-change': no change from the language name
        '''
        transform_file = os.path.join(
            node_folder, 'cldr-misc-full', 'main', cldr_locale,
            'contextTransforms.json')

        if os.path.isfile(transform_file):
            with open(transform_file) as data_file:
                try:
                    json_data = json.load(data_file)
                    languages[locale]['transform-type'] = (
                        json_data['main']
                                 [cldr_locale]['contextTransforms']
                                 ['languages']['uiListOrMenu'])
                except Exception:
                    print('Transform not available for {}'.format(locale))

        # Read language name from CLDR
        language_file = os.path.join(cldr_path_names, 'languages.json')
        if os.path.isfile(language_file):
            with open(language_file) as data_file:
                try:
                    json_data = json.load(data_file)
                    languages[locale]['cldr-name'] = (
                        json_data['main']
                                 [cldr_locale]['localeDisplayNames']
                                 ['languages'][cldr_locale])
                except Exception as e:
                    print('CLDR name not available for {}'.format(locale))

        # Apply text transformation
        language_name = languages[locale]['cldr-name']
        if (languages[locale]['transform-type'] == 'titlecase-firstword' and
                language_name != '---'):
            languages[locale]['transformed-name'] = language_name.capitalize()
        else:
            languages[locale]['transformed-name'] = language_name

    file_name = os.path.join(script_folder, os.path.pardir,
                             'output', 'languages.json')
    with open(file_name, 'w') as output_file:
        json.dump(languages, output_file, ensure_ascii=False,
                  indent=2, sort_keys=True)


if __name__ == '__main__':
    main()
