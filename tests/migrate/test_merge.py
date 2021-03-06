# coding=utf8

import unittest

import l20n.format.ast as FTL
from l20n.format.parser import FTLParser
try:
    from compare_locales.parser import PropertiesParser, DTDParser
except ImportError:
    PropertiesParser = DTDParser = None

from l20n.migrate.util import parse, ftl, ftl_resource_to_json
from l20n.migrate.merge import merge_resource
from l20n.migrate.transforms import LITERAL, LITERAL_FROM


class MockContext(unittest.TestCase):
    def get_source(self, path, key):
        return self.ab_cd_legacy.get(key, None).get_val()


@unittest.skipUnless(PropertiesParser and DTDParser,
                     'compare-locales required')
class TestMergeMessages(MockContext):
    def setUp(self):
        self.en_us_ftl = parse(FTLParser, ftl('''
            title  = Downloads
            header = Your Downloads
            empty  = No Downloads
            about  = About Downloads

            open-menuitem =
                [html/label] Open

            download-state-downloading = Downloading…
        '''))

        self.ab_cd_ftl = parse(FTLParser, ftl('''
            empty = Brak pobranych plików
            about = Previously Hardcoded Value
        '''))

        ab_cd_dtd = parse(DTDParser, '''
            <!ENTITY aboutDownloads.title "Pobrane pliki">
            <!ENTITY aboutDownloads.open "Otwórz">
        ''')

        ab_cd_prop = parse(PropertiesParser, '''
            downloadState.downloading=Pobieranie…
        ''')

        self.ab_cd_legacy = {
            key: val
            for strings in (ab_cd_dtd, ab_cd_prop)
            for key, val in strings.items()
        }

        self.transforms = [
            FTL.Entity(
                FTL.Identifier('title'),
                value=LITERAL_FROM(None, 'aboutDownloads.title')
            ),
            FTL.Entity(
                FTL.Identifier('about'),
                value=LITERAL('Hardcoded Value')
            ),
            FTL.Entity(
                FTL.Identifier('open-menuitem'),
                traits=[
                    FTL.Member(
                        FTL.Keyword('label', 'html'),
                        LITERAL_FROM(None, 'aboutDownloads.open')
                    ),
                ]
            ),
            FTL.Entity(
                FTL.Identifier('download-state-downloading'),
                value=LITERAL_FROM(None, 'downloadState.downloading')
            )
        ]

    def test_merge_two_way(self):
        resource = merge_resource(
            self, self.en_us_ftl, FTL.Resource(), self.transforms,
            in_changeset=lambda x: True
        )

        self.assertEqual(
            resource.toJSON(),
            ftl_resource_to_json('''
                title = Pobrane pliki
                about = Hardcoded Value

                open-menuitem =
                    [html/label] Otwórz

                download-state-downloading = Pobieranie…
            ''')
        )

    def test_merge_three_way(self):
        resource = merge_resource(
            self, self.en_us_ftl, self.ab_cd_ftl, self.transforms,
            in_changeset=lambda x: True
        )

        self.assertEqual(
            resource.toJSON(),
            ftl_resource_to_json('''
                title = Pobrane pliki
                empty = Brak pobranych plików
                about = Previously Hardcoded Value

                open-menuitem =
                    [html/label] Otwórz

                download-state-downloading = Pobieranie…
            ''')
        )


@unittest.skipUnless(PropertiesParser and DTDParser,
                     'compare-locales required')
class TestMergeAllEntries(MockContext):
    def setUp(self):
        self.en_us_ftl = parse(FTLParser, ftl('''
            # This Source Code Form is subject to the terms of …

            # A generic comment.

            title  = Downloads
            header = Your Downloads
            empty  = No Downloads

            # A section comment.
            [[ Menu items ]]

            # A message comment.
            open-menuitem =
                [html/label] Open

            download-state-downloading = Downloading…
        '''))

        self.ab_cd_ftl = parse(FTLParser, ftl('''
            # This Source Code Form is subject to the terms of …

            empty = Brak pobranych plików
        '''))

        ab_cd_dtd = parse(DTDParser, '''
            <!ENTITY aboutDownloads.title "Pobrane pliki">
            <!ENTITY aboutDownloads.open "Otwórz">
        ''')

        ab_cd_prop = parse(PropertiesParser, '''
            downloadState.downloading=Pobieranie…
        ''')

        self.ab_cd_legacy = {
            key: val
            for strings in (ab_cd_dtd, ab_cd_prop)
            for key, val in strings.items()
        }

        self.transforms = [
            FTL.Entity(
                FTL.Identifier('title'),
                value=LITERAL_FROM(None, 'aboutDownloads.title')
            ),
            FTL.Entity(
                FTL.Identifier('open-menuitem'),
                traits=[
                    FTL.Member(
                        FTL.Keyword('label', 'html'),
                        LITERAL_FROM(None, 'aboutDownloads.open')
                    ),
                ]
            ),
            FTL.Entity(
                FTL.Identifier('download-state-downloading'),
                value=LITERAL_FROM(None, 'downloadState.downloading')
            )
        ]

    def test_merge_two_way(self):
        resource = merge_resource(
            self, self.en_us_ftl, FTL.Resource(), self.transforms,
            in_changeset=lambda x: True
        )

        self.assertEqual(
            resource.toJSON(),
            ftl_resource_to_json('''
                # This Source Code Form is subject to the terms of …

                # A generic comment.

                title = Pobrane pliki

                # A section comment.
                [[ Menu items ]]

                # A message comment.
                open-menuitem =
                    [html/label] Otwórz
                download-state-downloading = Pobieranie…

            ''')
        )

    def test_merge_three_way(self):
        resource = merge_resource(
            self, self.en_us_ftl, self.ab_cd_ftl, self.transforms,
            in_changeset=lambda x: True
        )

        self.assertEqual(
            resource.toJSON(),
            ftl_resource_to_json('''
                # This Source Code Form is subject to the terms of …

                # A generic comment.

                title = Pobrane pliki
                empty = Brak pobranych plików

                # A section comment.
                [[ Menu items ]]

                # A message comment.
                open-menuitem =
                    [html/label] Otwórz

                download-state-downloading = Pobieranie…

            ''')
        )


@unittest.skipUnless(PropertiesParser and DTDParser,
                     'compare-locales required')
class TestMergeSubset(MockContext):
    def setUp(self):
        self.en_us_ftl = parse(FTLParser, ftl('''
            # This Source Code Form is subject to the terms of …

            # A generic comment.

            title  = Downloads
            header = Your Downloads
            empty  = No Downloads

            # A section comment.
            [[ Menu items ]]

            # A message comment.
            open-menuitem =
                [html/label] Open

            download-state-downloading = Downloading…
        '''))

        ab_cd_dtd = parse(DTDParser, '''
            <!ENTITY aboutDownloads.title "Pobrane pliki">
            <!ENTITY aboutDownloads.open "Otwórz">
        ''')

        ab_cd_prop = parse(PropertiesParser, '''
            downloadState.downloading=Pobieranie…
        ''')

        self.ab_cd_legacy = {
            key: val
            for strings in (ab_cd_dtd, ab_cd_prop)
            for key, val in strings.items()
        }

        self.transforms = [
            FTL.Entity(
                FTL.Identifier('title'),
                value=LITERAL_FROM(None, 'aboutDownloads.title')
            ),
            FTL.Entity(
                FTL.Identifier('download-state-downloading'),
                value=LITERAL_FROM(None, 'downloadState.downloading')
            )
        ]

    def test_two_way_one_entity(self):
        subset = ('title',)
        resource = merge_resource(
            self, self.en_us_ftl, FTL.Resource(), self.transforms,
            in_changeset=lambda x: x in subset
        )

        self.assertEqual(
            resource.toJSON(),
            ftl_resource_to_json('''
                # This Source Code Form is subject to the terms of …

                # A generic comment.

                title = Pobrane pliki
            ''')
        )

    def test_two_way_two_entities(self):
        subset = ('title', 'download-state-downloading')
        resource = merge_resource(
            self, self.en_us_ftl, FTL.Resource(), self.transforms,
            in_changeset=lambda x: x in subset
        )

        self.assertEqual(
            resource.toJSON(),
            ftl_resource_to_json('''
                # This Source Code Form is subject to the terms of …

                # A generic comment.

                title = Pobrane pliki

                # A section comment.
                [[ Menu items ]]

                download-state-downloading = Pobieranie…
            ''')
        )

    def test_three_way_one_entity(self):
        ab_cd_ftl = parse(FTLParser, ftl('''
            # This Source Code Form is subject to the terms of …

            empty = Brak pobranych plików
        '''))

        subset = ('title',)
        resource = merge_resource(
            self, self.en_us_ftl, ab_cd_ftl, self.transforms,
            in_changeset=lambda x: x in subset
        )

        self.assertEqual(
            resource.toJSON(),
            ftl_resource_to_json('''
                # This Source Code Form is subject to the terms of …

                # A generic comment.

                title = Pobrane pliki
                empty = Brak pobranych plików
            ''')
        )

    def test_three_way_two_entities(self):
        ab_cd_ftl = parse(FTLParser, ftl('''
            # This Source Code Form is subject to the terms of …

            empty = Brak pobranych plików
        '''))

        subset = ('title', 'download-state-downloading')
        resource = merge_resource(
            self, self.en_us_ftl, ab_cd_ftl, self.transforms,
            in_changeset=lambda x: x in subset
        )

        self.assertEqual(
            resource.toJSON(),
            ftl_resource_to_json('''
                # This Source Code Form is subject to the terms of …

                # A generic comment.

                title = Pobrane pliki
                empty = Brak pobranych plików

                # A section comment.
                [[ Menu items ]]

                download-state-downloading = Pobieranie…
            ''')
        )

    def test_three_way_one_entity_existing_section(self):
        ab_cd_ftl = parse(FTLParser, ftl('''
            # This Source Code Form is subject to the terms of …

            empty = Brak pobranych plików

            # A section comment.
            [[ Menu items ]]

            # A message comment.
            open-menuitem =
                [html/label] Otwórz
        '''))

        subset = ('title',)
        resource = merge_resource(
            self, self.en_us_ftl, ab_cd_ftl, self.transforms,
            in_changeset=lambda x: x in subset
        )

        self.assertEqual(
            resource.toJSON(),
            ftl_resource_to_json('''
                # This Source Code Form is subject to the terms of …

                # A generic comment.

                title = Pobrane pliki
                empty = Brak pobranych plików

                # A section comment.
                [[ Menu items ]]

                # A message comment.
                open-menuitem =
                    [html/label] Otwórz
            ''')
        )

    def test_three_way_two_entities_existing_section(self):
        ab_cd_ftl = parse(FTLParser, ftl('''
            # This Source Code Form is subject to the terms of …

            empty = Brak pobranych plików

            # A section comment.
            [[ Menu items ]]

            # A message comment.
            open-menuitem =
                [html/label] Otwórz
        '''))

        subset = ('title', 'download-state-downloading')
        resource = merge_resource(
            self, self.en_us_ftl, ab_cd_ftl, self.transforms,
            in_changeset=lambda x: x in subset
        )

        self.assertEqual(
            resource.toJSON(),
            ftl_resource_to_json('''
                # This Source Code Form is subject to the terms of …

                # A generic comment.

                title = Pobrane pliki
                empty = Brak pobranych plików

                # A section comment.
                [[ Menu items ]]

                # A message comment.
                open-menuitem =
                    [html/label] Otwórz
                download-state-downloading = Pobieranie…
            ''')
        )
