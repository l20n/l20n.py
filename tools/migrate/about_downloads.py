# coding=utf8

import l20n.format.ast as FTL
from l20n.migrate import LITERAL_FROM, PLURALS_FROM, REPLACE


def migrate(ctx):
    """Migrate about:download in Firefox for Android, part {index}"""

    ctx.add_reference(
        'mobile/aboutDownloads.ftl',
        realpath='aboutDownloads.ftl'
    )
    ctx.add_localization('mobile/android/chrome/aboutDownloads.dtd')
    ctx.add_localization('mobile/android/chrome/aboutDownloads.properties')

    ctx.add_transforms('mobile/aboutDownloads.ftl', [
        FTL.Entity(
            id=FTL.Identifier('title'),
            value=LITERAL_FROM(
                'mobile/android/chrome/aboutDownloads.dtd',
                'aboutDownloads.title'
            )
        ),
        FTL.Entity(
            id=FTL.Identifier('header'),
            value=LITERAL_FROM(
                'mobile/android/chrome/aboutDownloads.dtd',
                'aboutDownloads.header'
            )
        ),
        FTL.Entity(
            id=FTL.Identifier('empty'),
            value=LITERAL_FROM(
                'mobile/android/chrome/aboutDownloads.dtd',
                'aboutDownloads.empty'
            )
        ),
        FTL.Entity(
            id=FTL.Identifier('open-menuitem'),
            traits=[
                FTL.Member(
                    FTL.Keyword('label', 'html'),
                    LITERAL_FROM(
                        'mobile/android/chrome/aboutDownloads.dtd',
                        'aboutDownloads.open'
                    )
                )
            ]
        ),
        FTL.Entity(
            id=FTL.Identifier('retry-menuitem'),
            traits=[
                FTL.Member(
                    FTL.Keyword('label', 'html'),
                    LITERAL_FROM(
                        'mobile/android/chrome/aboutDownloads.dtd',
                        'aboutDownloads.retry'
                    )
                )
            ]
        ),
        FTL.Entity(
            id=FTL.Identifier('remove-menuitem'),
            traits=[
                FTL.Member(
                    FTL.Keyword('label', 'html'),
                    LITERAL_FROM(
                        'mobile/android/chrome/aboutDownloads.dtd',
                        'aboutDownloads.remove'
                    )
                )
            ]
        ),
        FTL.Entity(
            id=FTL.Identifier('pause-menuitem'),
            traits=[
                FTL.Member(
                    FTL.Keyword('label', 'html'),
                    LITERAL_FROM(
                        'mobile/android/chrome/aboutDownloads.dtd',
                        'aboutDownloads.pause'
                    )
                )
            ]
        ),
        FTL.Entity(
            id=FTL.Identifier('resume-menuitem'),
            traits=[
                FTL.Member(
                    FTL.Keyword('label', 'html'),
                    LITERAL_FROM(
                        'mobile/android/chrome/aboutDownloads.dtd',
                        'aboutDownloads.resume'
                    )
                )
            ]
        ),
        FTL.Entity(
            id=FTL.Identifier('cancel-menuitem'),
            traits=[
                FTL.Member(
                    FTL.Keyword('label', 'html'),
                    LITERAL_FROM(
                        'mobile/android/chrome/aboutDownloads.dtd',
                        'aboutDownloads.cancel'
                    )
                )
            ]
        ),
        FTL.Entity(
            id=FTL.Identifier('remove-all-menuitem'),
            traits=[
                FTL.Member(
                    FTL.Keyword('label', 'html'),
                    LITERAL_FROM(
                        'mobile/android/chrome/aboutDownloads.dtd',
                        'aboutDownloads.removeAll'
                    )
                )
            ]
        ),
        FTL.Entity(
            id=FTL.Identifier('delete-all-title'),
            value=LITERAL_FROM(
                'mobile/android/chrome/aboutDownloads.properties',
                'downloadAction.deleteAll'
            )
        ),
        FTL.Entity(
            id=FTL.Identifier('delete-all-message'),
            value=PLURALS_FROM(
                'mobile/android/chrome/aboutDownloads.properties',
                'downloadMessage.deleteAll',
                FTL.ExternalArgument('num'),
                lambda var: REPLACE(
                    var,
                    {'#1': [FTL.ExternalArgument('num')]}
                )
            )
        ),
        FTL.Entity(
            id=FTL.Identifier('download-state-downloading'),
            value=LITERAL_FROM(
                'mobile/android/chrome/aboutDownloads.properties',
                'downloadState.downloading'
            )
        ),
        FTL.Entity(
            id=FTL.Identifier('download-state-canceled'),
            value=LITERAL_FROM(
                'mobile/android/chrome/aboutDownloads.properties',
                'downloadState.canceled'
            )
        ),
        FTL.Entity(
            id=FTL.Identifier('download-state-failed'),
            value=LITERAL_FROM(
                'mobile/android/chrome/aboutDownloads.properties',
                'downloadState.failed'
            )
        ),
        FTL.Entity(
            id=FTL.Identifier('download-state-paused'),
            value=LITERAL_FROM(
                'mobile/android/chrome/aboutDownloads.properties',
                'downloadState.paused'
            )
        ),
        FTL.Entity(
            id=FTL.Identifier('download-state-starting'),
            value=LITERAL_FROM(
                'mobile/android/chrome/aboutDownloads.properties',
                'downloadState.starting'
            )
        ),
        FTL.Entity(
            id=FTL.Identifier('download-size-unknown'),
            value=LITERAL_FROM(
                'mobile/android/chrome/aboutDownloads.properties',
                'downloadState.unknownSize'
            )
        ),
    ])
