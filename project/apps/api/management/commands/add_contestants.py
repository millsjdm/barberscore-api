from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from apps.api.factories import (
    add_contestants,
)

from apps.api.models import (
    Contest,
)


class Command(BaseCommand):
    help = "Create contestants."

    def add_arguments(self, parser):
        parser.add_argument(
            'slug',
            type=str,
        )

    def handle(self, *args, **options):
        try:
            contest = Contest.objects.get(
                slug=options['slug'],
            )
        except Contest.DoesNotExist:
            raise CommandError("Contest does not exist.")
        result = add_contestants(contest)
        self.stdout.write("{0}".format(result))
