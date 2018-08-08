#! /usr/bin/env python3

import os
import json


def main():
    script_folder = os.path.abspath(os.path.dirname(__file__))

    # Curated list

    # Read JSON data
    file_name = os.path.join(
        script_folder, os.path.pardir, 'output', 'languages_curated.json')
    with open(file_name) as inputfile:
        curated_data = json.load(inputfile)

    # Read HTML template
    file_name = os.path.join(
        script_folder, os.path.pardir, 'templates', 'curated.html')
    with open(file_name) as inputfile:
        template = inputfile.read()

    tbl_content = []
    for locale_code, language_name in curated_data.items():
        tbl_content.append('''
        <tr>
            <td>{}</td>
            <td>{}</td>
        </tr>'''.format(locale_code, language_name))

    # Write HTML output
    template = template.replace('%TABLEBODY%', '\n'.join(tbl_content))
    file_name = os.path.join(
        script_folder, os.path.pardir, 'docs', 'index.html')
    with open(file_name, 'w') as outputfile:
        outputfile.write(template)

    # Complete analysis list

    # Read JSON data
    file_name = os.path.join(
        script_folder, os.path.pardir, 'output', 'languages.json')
    with open(file_name) as inputfile:
        complete_data = json.load(inputfile)

    # Read HTML template
    file_name = os.path.join(
        script_folder, os.path.pardir, 'templates', 'complete.html')
    with open(file_name) as inputfile:
        template = inputfile.read()

    tbl_content = []
    for locale_code, locale_data in complete_data.items():
        tbl_content.append('''
        <tr>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
        </tr>'''.format(
            'Yes' if locale_data['cldr-available'] else 'No',
            locale_code,
            locale_data['cldr-name'],
            locale_data['transform-type'],
            locale_data['transformed-name'],
            locale_data['mozilla-name']))

    # Write HTML output
    template = template.replace('%TABLEBODY%', '\n'.join(tbl_content))
    file_name = os.path.join(
        script_folder, os.path.pardir, 'docs', 'complete.html')
    with open(file_name, 'w') as outputfile:
        outputfile.write(template)


if __name__ == '__main__':
    main()
