from __future__ import division

import logging
log = logging.getLogger(__name__)

import uuid

import os
import datetime

from django.db import (
    models,
)

from autoslug import AutoSlugField

from django.core.validators import (
    RegexValidator,
    MaxValueValidator,
    MinValueValidator,
)

from django_fsm import (
    transition,
    # FSMField,
    FSMIntegerField,
)

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)

from django.core.exceptions import (
    ValidationError,
)

from model_utils.models import (
    TimeStampedModel,
)

from model_utils.fields import (
    MonitorField,
)

from model_utils import Choices

from model_utils.managers import (
    PassThroughManager,
)

from mptt.models import (
    MPTTModel,
    TreeForeignKey,
)

from timezone_field import TimeZoneField

from phonenumber_field.modelfields import PhoneNumberField

from nameparser import HumanName

from .managers import (
    UserManager,
    ContestantQuerySet,
)


from .validators import (
    validate_trimmed,
    dixon,
    is_imcontested,
    # is_scheduled,
    has_contestants,
    has_awards,
    # session_scheduled,
    award_started,
    scores_entered,
    songs_entered,
    sessions_finished,
    # session_finished,
    performances_finished,
    scores_validated,
    song_entered,
    score_entered,
    preceding_finished,
    preceding_session_finished,
)


def generate_image_filename(instance, filename):
    f, ext = os.path.splitext(filename)
    return '{0}{1}'.format(instance.id, ext)


class Common(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        help_text="""
            The name of the resource.""",
        max_length=200,
        unique=True,
        validators=[
            validate_trimmed,
        ],
        error_messages={
            'unique': 'The name must be unique.  Add middle initials, suffixes, years, or other identifiers to make the name unique.',
        }
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    start_date = models.DateField(
        help_text="""
            The founding/birth date of the resource.""",
        blank=True,
        null=True,
    )

    end_date = models.DateField(
        help_text="""
            The retirement/deceased date of the resource.""",
        blank=True,
        null=True,
    )

    location = models.CharField(
        help_text="""
            The geographical location of the resource.""",
        max_length=200,
        blank=True,
    )

    website = models.URLField(
        help_text="""
            The website URL of the resource.""",
        blank=True,
    )

    facebook = models.URLField(
        help_text="""
            The facebook URL of the resource.""",
        blank=True,
    )

    twitter = models.CharField(
        help_text="""
            The twitter handle (in form @twitter_handle) of the resource.""",
        blank=True,
        max_length=16,
        validators=[
            RegexValidator(
                regex=r'@([A-Za-z0-9_]+)',
                message="""
                    Must be a single Twitter handle
                    in the form `@twitter_handle`.
                """,
            ),
        ],
    )

    email = models.EmailField(
        help_text="""
            The contact email of the resource.""",
        blank=True,
    )

    phone = PhoneNumberField(
        help_text="""
            The phone number of the resource.  Include country code.""",
        blank=True,
        null=True,
    )

    picture = models.ImageField(
        upload_to=generate_image_filename,
        help_text="""
            The picture/logo of the resource.""",
        blank=True,
        null=True,
    )

    description = models.TextField(
        help_text="""
            A description/bio of the resource.  Max 1000 characters.""",
        blank=True,
        max_length=1000,
    )

    notes = models.TextField(
        help_text="""
            Notes (for internal use only).""",
        blank=True,
    )

    is_active = models.BooleanField(
        help_text="""
            A boolean for active/living resources.""",
        default=True,
    )

    class Meta:
        abstract = True


class Arranger(TimeStampedModel):
    """Chorus relation"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    PART = Choices(
        (1, 'arranger', 'Arranger'),
        (2, 'coarranger', 'Co-Arranger'),
    )

    name = models.CharField(
        max_length=255,
        unique=True,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    catalog = models.ForeignKey(
        'Catalog',
        related_name='arrangers',
        null=True,
        blank=True,
    )

    person = models.ForeignKey(
        'Person',
        related_name='arrangements',
    )

    part = models.IntegerField(
        choices=PART,
        default=PART.arranger,
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1}".format(
            self.catalog,
            self.person,
        )
        super(Arranger, self).save(*args, **kwargs)

    class Meta:
        unique_together = (
            ('catalog', 'person',),
        )


class Award(TimeStampedModel):

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'built', 'Built',),
        (20, 'started', 'Started',),
        (25, 'finished', 'Finished',),
        (30, 'final', 'Final',),
    )

    HISTORY = Choices(
        (0, 'new', 'New',),
        (10, 'none', 'None',),
        (20, 'pdf', 'PDF',),
        (30, 'places', 'Places',),
        (40, 'incomplete', 'Incomplete',),
        (50, 'complete', 'Complete',),
    )

    YEAR_CHOICES = []
    for r in reversed(range(1939, (datetime.datetime.now().year + 2))):
        YEAR_CHOICES.append((r, r))

    ROUNDS_CHOICES = []
    for r in reversed(range(1, 4)):
        ROUNDS_CHOICES.append((r, r))

    KIND = Choices(
        (1, 'quartet', 'Quartet',),
        (2, 'chorus', 'Chorus',),
        (3, 'senior', 'Senior',),
        (4, 'collegiate', 'Collegiate',),
        (5, 'novice', 'Novice',),
        (6, 'a', 'Plateau A',),
        (7, 'aa', 'Plateau AA',),
        (8, 'aaa', 'Plateau AAA',),
        (9, 'dc', 'Dealer\'s Choice',),
    )

    LEVEL = Choices(
        (1, 'international', "International"),
        (2, 'district', "District"),
        (3, 'division', "Division"),
    )

    GOAL = Choices(
        (1, 'championship', "Championship"),
        (2, 'qualifier', "Qualifier"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=200,
        unique=True,
        editable=False,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    contest = models.ForeignKey(
        'Contest',
        related_name='awards',
    )

    organization = TreeForeignKey(
        'Organization',
        help_text="""
            The organization that will confer the award.  Note that this may be different than the organization running the parent contest.""",
        related_name='awards',
    )

    level = models.IntegerField(
        help_text="""
            The level of the award.  Note that this may be different than the level of the parent contest.""",
        choices=LEVEL,
    )

    kind = models.IntegerField(
        help_text="""
            The kind of the award.  Note that this may be different than the kind of the parent contest.""",
        choices=KIND,
    )

    goal = models.IntegerField(
        help_text="""
            The objective of the award.""",
        choices=GOAL,
    )

    qual_score = models.FloatField(
        help_text="""
            The objective of the award.  Note that if the goal is `qualifier` then this must be set.""",
        null=True,
        blank=True,
    )

    year = models.IntegerField(
        choices=YEAR_CHOICES,
    )

    rounds = models.IntegerField(
        help_text="""
            The number of rounds that will be used in determining the award.  Note that this may be fewer than the total number of rounds (sessions) in the parent contest.""",
        choices=ROUNDS_CHOICES,
    )

    history = models.IntegerField(
        help_text="""Used to manage state for historical imports.""",
        choices=HISTORY,
        default=HISTORY.new,
    )

    history_monitor = MonitorField(
        help_text="""History last updated""",
        monitor='history',
    )

    scoresheet_pdf = models.FileField(
        help_text="""
            PDF of the OSS.""",
        upload_to=generate_image_filename,
        blank=True,
        null=True,
    )

    scoresheet_csv = models.FileField(
        help_text="""
            The parsed scoresheet (used for legacy imports).""",
        upload_to=generate_image_filename,
        blank=True,
        null=True,
    )

    class Meta:
        unique_together = (
            ('level', 'kind', 'year', 'goal', 'organization', 'contest',),
        )
        ordering = (
            '-year',
            'organization',
            'level',
            'kind',
            'goal',
        )

    @staticmethod
    def autocomplete_search_fields():
            return ("id__iexact", "name__icontains",)

    def __unicode__(self):
        return u"{0}".format(self.name)

    def clean(self):
        if self.goal == self.GOAL.qualifier and not self.qual_score:
            raise ValidationError('The qualification score must be set.')

    def save(self, *args, **kwargs):
        self.name = u"{0} {1} {2} {3} {4}".format(
            self.organization,
            self.get_level_display(),
            self.get_kind_display(),
            self.get_goal_display(),
            self.year,
        )
        super(Award, self).save(*args, **kwargs)

    @transition(
        field=status,
        source=STATUS.new,
        target=STATUS.built,
    )
    def build(self):
        # Triggered by award post_save signal if created
        r = 1
        while r <= self.rounds:
            self.sessions.create(
                contest=self,
                kind=r,
            )
            r += 1

        # # Create an adminstrator sentinel
        # self.judges.create(
        #     award=self,
        #     category=0,
        #     slot=1,
        # )

        # # Create sentinels for the contest.
        # s = 1
        # while s <= self.contest:
        #     self.judges.create(
        #         award=self,
        #         category=1,
        #         slot=s,
        #     )
        #     self.judges.create(
        #         award=self,
        #         category=2,
        #         slot=s,
        #     )
        #     self.judges.create(
        #         award=self,
        #         category=3,
        #         slot=s,
        #     )
        #     s += 1
        # return

    # @transition(
    #     field=status,
    #     source=[
    #         STATUS.built,
    #         STATUS.ready,
    #     ],
    #     target=STATUS.ready,
    #     conditions=[
    #         is_scheduled,
    #         is_imcontested,
    #         has_contestants,
    #     ],
    # )
    # def prep(self):
    #     # Seed contestants
    #     marker = []
    #     i = 1
    #     for contestant in self.contestants.accepted().order_by('-prelim'):
    #         try:
    #             match = contestant.prelim == marker[0].prelim
    #         except IndexError:
    #             contestant.seed = i
    #             contestant.save()
    #             marker.append(contestant)
    #             continue
    #         if match:
    #             contestant.seed = i
    #             i += len(marker)
    #             contestant.save()
    #             marker.append(contestant)
    #             continue
    #         else:
    #             i += 1
    #             contestant.seed = i
    #             contestant.save()
    #             marker = [contestant]
    #     return "{0} Ready".format(self)

    # @transition(
    #     field=status,
    #     source=STATUS.built,
    #     target=STATUS.started,
    #     conditions=[
    #         # is_scheduled,
    #         is_imcontested,
    #         has_contestants,
    #         has_awards,
    #     ],
    # )
    # def start(self):
    #     # Triggered in UI
    #     # TODO seed contestants?
    #     session = self.sessions.initial()
    #     p = 0
    #     for contestant in self.contestants.accepted().order_by('?'):
    #         contestant.register()
    #         contestant.save()
    #         session.performances.create(
    #             session=session,
    #             contestant=contestant,
    #             position=p,
    #         )
    #         p += 1
    #     return "{0} Started".format(self)

    @transition(
        field=status,
        source=STATUS.started,
        target=STATUS.finished,
        conditions=[
            # sessions_finished,
        ],
    )
    # Check everything is done.
    def finish(self):
        # Denormalize
        ns = Song.objects.filter(
            performance__session__contest=self.contest,
        )
        for n in ns:
            n.save()
        ps = Performance.objects.filter(
            session__contest=self.contest,
        )
        for p in ps:
            p.save()
        ts = Contestant.objects.filter(
            contest=self.contest,
        )
        for t in ts:
            t.save()
        rs = Competitor.objects.filter(
            award=self,
        )
        for r in rs:
            r.save()
        # Rank results
        cursor = []
        i = 1
        for competitor in self.competitors.order_by('-total_points'):
            try:
                match = competitor.total_points == cursor[0].total_points
            except IndexError:
                competitor.place = i
                competitor.save()
                cursor.append(competitor)
                continue
            if match:
                competitor.place = i
                i += len(cursor)
                competitor.save()
                cursor.append(competitor)
                continue
            else:
                i += 1
                competitor.place = i
                competitor.save()
                cursor = [competitor]
        return "{0} Ready for Review".format(self)

    @transition(field=status, source=STATUS.finished, target=STATUS.final)
    def finalize(self):
        # Review logic
        return "{0} Ready".format(self)


class Catalog(TimeStampedModel):
    TEMPO = Choices(
        (1, "Ballad"),
        (2, "Uptune"),
        (3, "Mixed"),
    )

    DIFFICULTY = Choices(
        (1, "Very Easy"),
        (2, "Easy"),
        (3, "Medium"),
        (4, "Hard"),
        (5, "Very Hard"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    tune = models.ForeignKey(
        'Tune',
        null=True,
        blank=True,
        related_name='catalogs',
    )

    song_name = models.CharField(
        blank=True,
        max_length=200,
    )

    bhs_id = models.IntegerField(
        null=True,
        blank=True,
    )

    bhs_published = models.DateField(
        null=True,
        blank=True,
    )

    bhs_songname = models.CharField(
        blank=True,
        max_length=200,
    )

    bhs_arranger = models.CharField(
        blank=True,
        max_length=200,
    )

    bhs_fee = models.FloatField(
        null=True,
        blank=True,
    )

    bhs_difficulty = models.IntegerField(
        null=True,
        blank=True,
        choices=DIFFICULTY
    )

    bhs_tempo = models.IntegerField(
        null=True,
        blank=True,
        choices=TEMPO,
    )

    bhs_medley = models.BooleanField(
        default=False,
    )

    is_parody = models.BooleanField(
        default=False,
    )

    is_medley = models.BooleanField(
        default=False,
    )


class Certification(TimeStampedModel):
    """Certification"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New'),
        (1, 'active', 'Active'),
        (2, 'candidate', 'Candidate'),
    )

    CATEGORY = Choices(
        (0, 'admin', 'Admin'),
        (1, 'music', 'Music'),
        (2, 'presentation', 'Presentation'),
        (3, 'singing', 'Singing'),
    )

    name = models.CharField(
        max_length=255,
        unique=True,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    person = models.ForeignKey(
        'Person',
        related_name='certifications',
    )

    category = models.IntegerField(
        choices=CATEGORY,
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1}".format(
            self.person,
            self.get_category_display(),
        )
        super(Certification, self).save(*args, **kwargs)

    class Meta:
        unique_together = (
            ('category', 'person',),
        )


class Competitor(TimeStampedModel):
    STATUS = Choices(
        (0, 'new', 'New',),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    contestant = models.ForeignKey(
        'Contestant',
        related_name='competitors',
    )

    award = models.ForeignKey(
        'Award',
        related_name='competitors',
    )

    # Denormalization
    place = models.IntegerField(
        help_text="""
            The final ranking relative to this award.""",
        null=True,
        blank=True,
        editable=False,
    )

    mus_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    prs_points = models.IntegerField(
        null=True,
        editable=False,
        blank=True,
    )

    sng_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    total_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    mus_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    prs_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    sng_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    total_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1}".format(
            self.award,
            self.contestant.group,
        )
        super(Competitor, self).save(*args, **kwargs)

    class Meta:
        unique_together = (
            ('contestant', 'award',),
        )
        ordering = (
            'award',
            'contestant',
        )

    def calculate(self):
        # If there are no performances, skip.
        if self.contestant.performances.exists():
            agg = self.contestant.performances.filter(
                session__num__lte=self.award.rounds,
            ).filter(
                session__contest=self.award.contest,
            ).aggregate(
                mus=models.Sum('mus_points'),
                prs=models.Sum('prs_points'),
                sng=models.Sum('sng_points'),
            )
            self.mus_points = agg['mus']
            self.prs_points = agg['prs']
            self.sng_points = agg['sng']

            # Calculate total points.
            try:
                self.total_points = sum([
                    self.mus_points,
                    self.prs_points,
                    self.sng_points,
                ])
            except TypeError:
                self.total_points = None

            # Calculate percentile
            try:
                possible = self.award.contest.size * 2 * self.contestant.performances.count()
                self.mus_score = round(self.mus_points / possible, 1)
                self.prs_score = round(self.prs_points / possible, 1)
                self.sng_score = round(self.sng_points / possible, 1)
                self.total_score = round(self.total_points / (possible * 3), 1)
            except TypeError:
                self.mus_score = None
                self.prs_score = None
                self.sng_score = None


class Contest(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'built', 'Built',),
        (20, 'started', 'Started',),
        (30, 'final', 'Final',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    convention = models.ForeignKey(
        'Convention',
        related_name='contests',
    )

    KIND = Choices(
        (1, 'quartet', 'Quartet',),
        (2, 'chorus', 'Chorus',),
        (3, 'senior', 'Senior',),
        (4, 'collegiate', 'Collegiate',),
    )

    kind = models.IntegerField(
        help_text="""
            The kind of contest.  Generally this will be either quartet or chorus, with the exception being International and Midwinter which hold exclusive Collegiate and Senior contests respectively.""",
        choices=KIND,
    )

    SIZE_CHOICES = []
    for r in reversed(range(1, 6)):
        SIZE_CHOICES.append((r, r))

    size = models.IntegerField(
        help_text="""
            Size of the judging panel (per category).""",
        choices=SIZE_CHOICES,
    )

    ROUNDS_CHOICES = []
    for r in reversed(range(1, 4)):
        ROUNDS_CHOICES.append((r, r))

    rounds = models.IntegerField(
        help_text="""
            Number of rounds (sessions) for the contest.""",
        choices=ROUNDS_CHOICES,
    )

    # Denormalized
    organization = TreeForeignKey(
        'Organization',
        help_text="""
            The organization that will confer the award.  Note that this may be different than the organization running the parent contest.""",
        related_name='contests',
        editable=False,
    )

    YEAR_CHOICES = []
    for r in reversed(range(1939, (datetime.datetime.now().year + 2))):
        YEAR_CHOICES.append((r, r))

    year = models.IntegerField(
        choices=YEAR_CHOICES,
        editable=False,
    )

    # Legacy
    HISTORY = Choices(
        (0, 'new', 'New',),
        (10, 'none', 'None',),
        (20, 'pdf', 'PDF',),
        (30, 'places', 'Places',),
        (40, 'incomplete', 'Incomplete',),
        (50, 'complete', 'Complete',),
    )

    history = models.IntegerField(
        help_text="""Used to manage state for historical imports.""",
        choices=HISTORY,
        default=HISTORY.new,
    )

    history_monitor = MonitorField(
        help_text="""History last updated""",
        monitor='history',
    )

    scoresheet_pdf = models.FileField(
        help_text="""
            The historical PDF OSS.""",
        upload_to=generate_image_filename,
        blank=True,
        null=True,
    )

    scoresheet_csv = models.FileField(
        help_text="""
            The parsed scoresheet (used for legacy imports).""",
        upload_to=generate_image_filename,
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.year = self.convention.year
        self.organization = self.convention.organization
        self.name = u"{0} {1}".format(
            self.convention,
            self.get_kind_display(),
        )
        super(Contest, self).save(*args, **kwargs)

    class Meta:
        unique_together = (
            ('convention', 'kind',),
        )
        ordering = (
            '-year',
            'convention',
            'kind',
        )

    @transition(
        field=status,
        source=STATUS.built,
        target=STATUS.started,
        conditions=[
            # is_scheduled,
            # is_imcontested,
            # has_contestants,
            # has_awards,
        ],
    )
    def start(self):
        # Triggered in UI
        # TODO seed contestants?
        session = self.sessions.get(num=1)
        p = 0
        for contestant in self.contestants.accepted().order_by('?'):
            contestant.register()
            contestant.save()
            session.performances.create(
                session=session,
                contestant=contestant,
                position=p,
            )
            p += 1
        return "{0} Started".format(self)


class Contestant(TimeStampedModel):

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'qualified', 'Qualified',),
        (20, 'accepted', 'Accepted',),
        (30, 'declined', 'Declined',),
        (40, 'dropped', 'Dropped',),
        (50, 'official', 'Official',),
        (60, 'finished', 'Finished',),
        (90, 'final', 'Final',),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    contest = models.ForeignKey(
        'Contest',
        related_name='contestants',
    )

    group = models.ForeignKey(
        'Group',
        related_name='contestants',
    )

    organization = TreeForeignKey(
        'Organization',
        related_name='contestants',
        null=True,
        blank=True,
    )

    picture = models.ImageField(
        help_text="""
            The on-stage contest picture (as opposed to the "official" photo).""",
        upload_to=generate_image_filename,
        blank=True,
        null=True,
    )

    seed = models.IntegerField(
        help_text="""
            The incoming rank based on prelim score.""",
        null=True,
        blank=True,
    )

    prelim = models.FloatField(
        help_text="""
            The incoming prelim score.""",
        null=True,
        blank=True,
    )

    men = models.IntegerField(
        help_text="""
            The number of men on stage.""",
        default=4,
        null=True,
        blank=True,
    )

    # Denormalized
    place = models.IntegerField(
        help_text="""
            The final placement/rank of the contestant for the entire contest (ie, not a specific award).""",
        null=True,
        blank=True,
        editable=False,
    )

    mus_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    prs_points = models.IntegerField(
        null=True,
        editable=False,
        blank=True,
    )

    sng_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    total_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    mus_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    prs_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    sng_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    total_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    @property
    def delta_score(self):
        """ The difference between qualifying score and final score.""",
        try:
            return self.total_score - self.prelim
        except TypeError:
            return None

    @property
    def delta_place(self):
        """ The difference between qualifying rank and final rank.""",
        try:
            return self.seed - self.place
        except TypeError:
            return None

    @staticmethod
    def autocomplete_search_fields():
            return ("id__iexact", "name__icontains",)

    objects = PassThroughManager.for_queryset_class(ContestantQuerySet)()

    def __unicode__(self):
        return u"{0}".format(self.name)

    def clean(self):
        if self.singers.count() > 4:
            raise ValidationError('There can not be more than four persons in a quartet.')

    def save(self, *args, **kwargs):
        self.name = u"{0} {1}".format(
            self.contest,
            self.group,
        )
        super(Contestant, self).save(*args, **kwargs)

    class Meta:
        ordering = (
            'contest',
            'group',
        )
        unique_together = (
            ('group', 'contest',),
        )

    def calculate(self):
        # If there are no performances, skip.
        if self.performances.exists():
            agg = self.performances.all().aggregate(
                mus=models.Sum('mus_points'),
                prs=models.Sum('prs_points'),
                sng=models.Sum('sng_points'),
            )
            self.mus_points = agg['mus']
            self.prs_points = agg['prs']
            self.sng_points = agg['sng']

            # Calculate total points.
            try:
                self.total_points = sum([
                    self.mus_points,
                    self.prs_points,
                    self.sng_points,
                ])
            except TypeError:
                self.total_points = None

            # Calculate percentile
            try:
                possible = self.contest.size * 2 * self.performances.count()
                self.mus_score = round(self.mus_points / possible, 1)
                self.prs_score = round(self.prs_points / possible, 1)
                self.sng_score = round(self.sng_points / possible, 1)
                self.total_score = round(self.total_points / (possible * 3), 1)
            except TypeError:
                self.mus_score = None
                self.prs_score = None
                self.sng_score = None

    @transition(field=status, source=STATUS.new, target=STATUS.qualified)
    def qualify(self):
        # Send notice?
        return "{0} Qualified".format(self)

    @transition(field=status, source=[STATUS.qualified, STATUS.declined], target=STATUS.accepted)
    def accept(self):
        # Send notice?
        return "{0} Accepted".format(self)

    @transition(field=status, source=[STATUS.qualified, STATUS.accepted], target=STATUS.declined)
    def decline(self):
        # Send notice?
        return "{0} Declined".format(self)

    @transition(
        field=status,
        source=STATUS.accepted,
        target=STATUS.official,
    )
    def register(self):
        # Triggered by award start
        return "{0} Official".format(self)

    @transition(field=status, source=STATUS.official, target=STATUS.dropped)
    def drop(self):
        # Send notice?
        return "{0} Dropped".format(self)

    @transition(field=status, source=STATUS.official, target=STATUS.finished)
    def finish(self):
        # Send notice?
        return "{0} Finished".format(self)

    @transition(field=status, source=STATUS.finished, target=STATUS.final)
    def finalize(self):
        # Send notice?
        return "{0} Finalized".format(self)


class Convention(TimeStampedModel):
    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'built', 'Built',),
        (20, 'started', 'Started',),
        (30, 'final', 'Final',),
    )

    KIND = Choices(
        (1, 'international', 'International',),
        (2, 'midwinter', 'Midwinter',),
        (3, 'fall', 'Fall',),
        (4, 'spring', 'Spring',),
        (5, 'pacific', 'Pacific',),
        (6, 'southcombo', 'Southeast and Southwest',),
        (7, 'northcombo', 'Northeast and Northwest',),
        (8, 'district', 'District',),
    )

    YEAR_CHOICES = []
    for r in reversed(range(1939, (datetime.datetime.now().year + 2))):
        YEAR_CHOICES.append((r, r))

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    organization = TreeForeignKey(
        'Organization',
        help_text="""
            The organization hosting the convention.""",
    )

    kind = models.IntegerField(
        help_text="""
            The kind of convention.""",
        choices=KIND,
    )

    year = models.IntegerField(
        choices=YEAR_CHOICES,
    )

    dates = models.CharField(
        help_text="""
            The convention dates (will be replaced by start/end).""",
        max_length=200,
        blank=True,
    )

    location = models.CharField(
        help_text="""
            The location of the convention.""",
        max_length=200,
        blank=True,
    )

    timezone = TimeZoneField(
        help_text="""
            The local timezone of the convention.""",
        default='US/Pacific',
    )

    class Meta:
        ordering = [
            '-year',
            'organization__name',
        ]

        unique_together = (
            ('organization', 'kind', 'year',),
        )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1} {2}".format(
            self.organization,
            self.get_kind_display(),
            self.year,
        )
        super(Convention, self).save(*args, **kwargs)


class Director(TimeStampedModel):
    """Chorus relation"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    PART = Choices(
        (1, 'director', 'Director'),
        (2, 'codirector', 'Co-Director'),
    )

    name = models.CharField(
        max_length=255,
        unique=True,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    contestant = models.ForeignKey(
        'Contestant',
        related_name='directors',
    )

    person = models.ForeignKey(
        'Person',
        related_name='choruses',
    )

    part = models.IntegerField(
        choices=PART,
        default=PART.director,
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1} {2}".format(
            self.contestant,
            self.get_part_display(),
            self.person,
        )
        super(Director, self).save(*args, **kwargs)

    def clean(self):
        if self.contestant.group.kind == Group.KIND.quartet:
            raise ValidationError('Quartets do not have directors.')

    class Meta:
        unique_together = (
            ('contestant', 'person',),
        )


class Group(Common):

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
        (20, 'inactive', 'Inactive',),
    )

    KIND = Choices(
        (1, 'quartet', 'Quartet'),
        (2, 'chorus', 'Chorus'),
    )

    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    kind = models.IntegerField(
        help_text="""
            The kind of group; choices are Quartet or Chorus.""",
        choices=KIND,
        default=KIND.quartet,
    )

    chapter_name = models.CharField(
        help_text="""
            The chapter name (only for choruses).""",
        max_length=200,
        blank=True,
    )

    chapter_code = models.CharField(
        help_text="""
            The chapter code (only for choruses).""",
        max_length=200,
        blank=True,
    )

    @staticmethod
    def autocomplete_search_fields():
            return ("id__iexact", "name__icontains",)

    def __unicode__(self):
        return u"{0}".format(self.name)

    def clean(self):
        if self.kind == self.KIND.quartet and self.chapter_name:
            raise ValidationError(
                {'chapter_name': 'Chapter names are only for choruses.'}
            )
        if self.kind == self.KIND.quartet and self.chapter_code:
            raise ValidationError(
                {'chapter_code': 'Chapter codes are only for choruses.'}
            )

    class Meta:
        ordering = (
            'name',
        )


class Judge(TimeStampedModel):
    """Award Judge"""

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'scheduled', 'Scheduled',),
        (20, 'confirmed', 'Confirmed',),
        (30, 'final', 'Final',),
    )

    SLOT_CHOICES = []
    for r in range(1, 6):
        SLOT_CHOICES.append((r, r))

    CATEGORY = Choices(
        (0, 'admin', 'Admin'),
        (1, 'music', 'Music'),
        (2, 'presentation', 'Presentation'),
        (3, 'singing', 'Singing'),
    )

    KIND = Choices(
        (10, 'official', 'Official'),
        (20, 'practice', 'Practice'),
        (30, 'composite', 'Composite'),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    contest = models.ForeignKey(
        'Contest',
        related_name='judges',
    )

    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    category = models.IntegerField(
        choices=CATEGORY,
    )

    kind = models.IntegerField(
        choices=KIND,
    )

    slot = models.IntegerField(
        choices=SLOT_CHOICES,
    )

    person = models.ForeignKey(
        'Person',
        related_name='contests',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    organization = TreeForeignKey(
        'Organization',
        related_name='judges',
        null=True,
        blank=True,
    )

    @staticmethod
    def autocomplete_search_fields():
            return ("id__iexact", "name__icontains", "person__icontains",)

    @property
    def designation(self):
        return u"{0[0]}{1:1d}".format(
            self.get_category_display(),
            self.slot,
        )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1} {2} {3}".format(
            self.contest,
            self.get_kind_display(),
            self.get_category_display(),
            self.slot,
        )
        super(Judge, self).save(*args, **kwargs)

    class Meta:
        unique_together = (
            ('contest', 'kind', 'category', 'slot'),
        )
        ordering = (
            'contest',
            'kind',
            'category',
            'slot',
        )


class Organization(MPTTModel, Common):
    long_name = models.CharField(
        help_text="""
            A long-form name for the resource.""",
        blank=True,
        max_length=200,
    )

    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
    )

    class MPTTMeta:
        order_insertion_by = [
            'name',
        ]
        ordering = [
            'tree_id',
        ]

    def __unicode__(self):
        return u"{0}".format(self.name)


class Performance(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        # (10, 'built', 'Built',),
        # (15, 'ready', 'Ready',),
        (20, 'started', 'Started',),
        (25, 'finished', 'Finished',),
        (40, 'confirmed', 'Confirmed',),
        (50, 'final', 'Final',),
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    session = models.ForeignKey(
        'Session',
        related_name='performances',
    )

    contestant = models.ForeignKey(
        'Contestant',
        related_name='performances',
    )

    position = models.PositiveSmallIntegerField(
        'Position',
    )

    start_time = models.DateTimeField(
        null=True,
        blank=True,
    )

    # Denormalized
    place = models.IntegerField(
        help_text="""
            The final ranking relative to this session.""",
        null=True,
        blank=True,
        editable=False,
    )

    mus_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    prs_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    sng_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    total_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    mus_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    prs_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    sng_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    total_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    @staticmethod
    def autocomplete_search_fields():
            return ("id__iexact", "name__icontains",)

    @property
    def draw(self):
        try:
            return "{0:02d}".format(self.position + 1)
        except TypeError:
            return None

    class Meta:
        ordering = (
            'session',
            'position',
        )
        unique_together = (
            ('session', 'contestant',),
        )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1}".format(
            self.session,
            self.contestant.group,
        )
        super(Performance, self).save(*args, **kwargs)

    def calculate(self):
        if self.songs.exists():
            agg = self.songs.all().aggregate(
                mus=models.Sum('mus_points'),
                prs=models.Sum('prs_points'),
                sng=models.Sum('sng_points'),
            )
            self.mus_points = agg['mus']
            self.prs_points = agg['prs']
            self.sng_points = agg['sng']

            # Calculate total points.
            try:
                self.total_points = sum([
                    self.mus_points,
                    self.prs_points,
                    self.sng_points,
                ])
            except TypeError:
                self.total_points = None

            # Calculate percentile scores
            try:
                possible = self.session.contest.size * 2
                self.mus_score = round(self.mus_points / possible, 1)
                self.prs_score = round(self.prs_points / possible, 1)
                self.sng_score = round(self.sng_points / possible, 1)
                self.total_score = round(self.total_points / (possible * 3), 1)
            except TypeError:
                self.mus_score = None
                self.prs_score = None
                self.sng_score = None

    def get_preceding(self):
        try:
            obj = self.__class__.objects.get(
                session=self.session,
                position=self.position - 1,
            )
            return obj
        except self.DoesNotExist:
            return None

    def get_next(self):
        try:
            obj = self.__class__.objects.get(
                session=self.session,
                position=self.position + 1,
            )
            return obj
        except self.DoesNotExist:
            return None

    # @transition(
    #     field=status,
    #     source=STATUS.new,
    #     target=STATUS.built,
    #     conditions=[
    #     ]
    # )
    # def build(self):
    #     return

    # @transition(
    #     field=status,
    #     source=STATUS.built,
    #     target=STATUS.ready,
    # )
    # def prep(self):
    #     return

    @transition(
        field=status,
        source=[
            # STATUS.built,
            STATUS.new,
        ],
        target=STATUS.started,
        conditions=[
            preceding_finished,
        ]
    )
    def start(self):
        # Triggered from UI
        # Creates Song and Score sentinels.
        i = 1
        while i <= 2:
            song = self.songs.create(
                performance=self,
                order=i,
            )
            for judge in self.session.contest.judges.scoring():
                song.scores.create(
                    song=song,
                    judge=judge,
                    kind=judge.kind,
                )
            i += 1
        return

    @transition(
        field=status,
        source=STATUS.started,
        target=STATUS.finished,
        conditions=[
            scores_entered,
            songs_entered,
        ]
    )
    def finish(self):
        # Triggered from UI
        dixon(self)  # TODO Should this be somewhere else?  Song perhaps?
        for song in self.songs.all():
            song.confirm()
        return

    @transition(
        field=status,
        source=STATUS.finished,
        target=STATUS.confirmed,
        # conditions=[
        #     session_finished,
        # ]
    )
    def confirm(self):
        return

    @transition(
        field=status,
        source=STATUS.confirmed,
        target=STATUS.final,
        conditions=[
        ]
    )
    def finalize(self):
        return


class Person(Common):

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
        (20, 'inactive', 'Inactive',),
        (30, 'retired', 'Retired',),
        (40, 'deceased', 'Deceased',),
    )

    KIND = Choices(
        (1, 'individual', "Individual"),
        (2, 'team', "Team"),
    )

    JUDGE = Choices(
        (0, 'admin', 'Admin'),
        (1, 'music', 'Music'),
        (2, 'presentation', 'Presentation'),
        (3, 'singing', 'Singing'),
        (4, 'music_candidate', 'Music Candidate'),
        (5, 'presentation_candidate', 'Presentation Candidate'),
        (6, 'singing_candidate', 'Singing Candidate'),
        (7, 'music_composite', 'Music Composite'),
        (8, 'presentation_composite', 'Presentation Composite'),
        (9, 'singing_composite', 'Singing Composite'),
    )

    kind = models.IntegerField(
        help_text="""
            Most persons are individuals; however, they can be grouped into teams for the purpose of multi-arranger songs.""",
        choices=KIND,
        default=KIND.individual,
    )

    status = models.IntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    organization = TreeForeignKey(
        'Organization',
        null=True,
        blank=True,
    )

    member = models.IntegerField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return u"{0}".format(self.name)

    @staticmethod
    def autocomplete_search_fields():
            return ("id__iexact", "name__icontains",)

    @property
    def is_judge(self):
        return bool(self.judge)

    @property
    def first_name(self):
        if self.name:
            name = HumanName(self.name)
            return name.first
        else:
            return None

    @property
    def last_name(self):
        if self.name:
            name = HumanName(self.name)
            return name.last
        else:
            return None

    @property
    def nick_name(self):
        if self.name:
            name = HumanName(self.nickname)
            return name.nickname
        else:
            return None


class Score(TimeStampedModel):
    """
        The Score is never released publicly.  These are the actual
        Judge's scores from the award.
    """
    STATUS = Choices(
        (0, 'new', 'New',),
        (20, 'entered', 'Entered',),
        (30, 'flagged', 'Flagged',),
        (35, 'validated', 'Validated',),
        (40, 'confirmed', 'Confirmed',),
        (50, 'final', 'Final',),
    )

    CATEGORY = Choices(
        (0, 'admin', 'Admin'),
        (1, 'music', 'Music'),
        (2, 'presentation', 'Presentation'),
        (3, 'singing', 'Singing'),
    )

    KIND = Choices(
        (10, 'official', 'Official'),
        (20, 'practice', 'Practice'),
        (30, 'composite', 'Composite'),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    song = models.ForeignKey(
        'Song',
        related_name='scores',
    )

    judge = models.ForeignKey(
        'Judge',
        related_name='scores',
    )

    category = models.IntegerField(
        choices=CATEGORY,
    )

    kind = models.IntegerField(
        choices=KIND,
    )

    points = models.IntegerField(
        help_text="""
            The number of points awarded (0-100)""",
        null=True,
        blank=True,
        validators=[
            MaxValueValidator(
                100,
                message='Points must be between 0 - 100',
            ),
            MinValueValidator(
                0,
                message='Points must be between 0 - 100',
            ),
        ]
    )

    class Meta:
        ordering = (
            'judge',
            'song',
        )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1} {2} {3}".format(
            self.song,
            self.get_kind_display(),
            self.get_category_display(),
            self.judge.slot,
        )
        super(Score, self).save(*args, **kwargs)

    @transition(
        field=status,
        source=STATUS.new,
        target=STATUS.flagged,
        conditions=[
            score_entered,
            # TODO Could be 'performance_finished' here if want to prevent admin UI
        ]
    )
    def flag(self):
        # Triggered from dixon test in performance.finish()
        return

    @transition(
        field=status,
        source=[
            STATUS.new,
            STATUS.flagged,
        ],
        target=STATUS.validated,
        conditions=[
            score_entered,
            # TODO Could be 'performance_finished' here if want to prevent admin UI
        ]
    )
    def validate(self):
        # Triggered from dixon test in performance.finish() or UI
        return

    @transition(
        field=status,
        source=[
            STATUS.validated,
        ],
        target=STATUS.confirmed,
        conditions=[
            # song_entered,
        ]
    )
    def confirm(self):
        return

    @transition(
        field=status,
        source=STATUS.confirmed,
        target=STATUS.final,
    )
    def finalize(self):
        return


class Session(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    STATUS = Choices(
        (0, 'new', 'New',),
        (10, 'built', 'Built',),
        (15, 'ready', 'Ready',),
        (20, 'started', 'Started',),
        (25, 'finished', 'Finished',),
        (30, 'final', 'Final',),
    )

    KIND = Choices(
        (1, 'finals', 'Finals'),
        (2, 'semis', 'Semis'),
        (3, 'quarters', 'Quarters'),
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    contest = models.ForeignKey(
        'Contest',
        related_name='sessions',
    )

    kind = models.IntegerField(
        choices=KIND,
    )

    num = models.IntegerField(
        null=True,
        blank=True,
    )

    start_date = models.DateField(
        null=True,
        blank=True,
    )

    slots = models.IntegerField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = (
            'contest',
            'kind',
        )
        unique_together = (
            ('contest', 'kind',),
        )

    def save(self, *args, **kwargs):
        self.name = u"{0} {1}".format(
            self.contest,
            self.get_kind_display(),
        )
        super(Session, self).save(*args, **kwargs)

    @staticmethod
    def autocomplete_search_fields():
            return ("id__iexact", "name__icontains",)

    def __unicode__(self):
        return u"{0}".format(self.name)

    def get_preceding(self):
        try:
            obj = self.__class__.objects.get(
                award=self.award,
                kind=self.kind + 1,
            )
            return obj
        except self.DoesNotExist:
            return None

    def get_next(self):
        try:
            obj = self.__class__.objects.get(
                award=self.award,
                kind=self.kind - 1,
            )
            return obj
        except self.DoesNotExist:
            return None

    def next_performance(self):
        try:
            return self.performances.filter(
                status=self.performances.model.STATUS.ready,
            ).order_by('position').first()
        except self.performances.model.DoesNotExist:
            return None

    # @transition(
    #     field=status,
    #     source=STATUS.new,
    #     target=STATUS.built,
    # )
    # def build(self):
    #     return

    # @transition(
    #     field=status,
    #     source=STATUS.built,
    #     target=STATUS.ready,
    #     # conditions=[
    #     #     award_started,
    #     # ]
    # )
    # def prep(self):
    #     p = 0
    #     for contestant in self.award.contestants.official().order_by('?'):
    #         self.performances.create(
    #             session=self,
    #             contestant=contestant,
    #             position=p,
    #         )
    #         p += 1
    #     return

    @transition(
        field=status,
        source=STATUS.new,
        target=STATUS.started,
        conditions=[
            # session_drawn,
            # session_scheduled,
            # award_started,
            # preceding_session_finished,
        ]
    )
    def start(self):
        # Triggered in UI
        return

    @transition(
        field=status,
        source=STATUS.started,
        target=STATUS.finished,
        conditions=[
            performances_finished,
            scores_validated,
        ]
    )
    def finish(self):
        # TODO Validate performances over
        cursor = []
        i = 1
        for performance in self.performances.order_by('-total_points'):
            try:
                match = performance.total_points == cursor[0].total_points
            except IndexError:
                performance.place = i
                performance.save()
                cursor.append(performance)
                continue
            if match:
                performance.place = i
                i += len(cursor)
                performance.save()
                cursor.append(performance)
                continue
            else:
                i += 1
                performance.place = i
                performance.save()
                cursor = [performance]
        return "Session Ended"

    @transition(field=status, source=STATUS.finished, target=STATUS.final)
    def finalize(self):
        return
        # # TODO Some validation
        # try:
        #     # TODO This is an awful lot to be in a try/except; refactor?
        #     next_session = self.award.sessions.get(
        #         kind=(self.kind - 1),
        #     )
        #     qualifiers = self.performances.filter(
        #         place__lte=next_session.slots,
        #     ).order_by('?')
        #     p = 0
        #     for qualifier in qualifiers:
        #         l = next_session.performances.create(
        #             contestant=qualifier.contestant,
        #             position=p,
        #             # start=next_session.start,
        #         )
        #         p += 1
        #         p1 = l.songs.create(performance=l, order=1)
        #         p2 = l.songs.create(performance=l, order=2)
        #         for j in self.award.judges.scoring():
        #             p1.scores.create(
        #                 song=p1,
        #                 judge=j,
        #             )
        #             p2.scores.create(
        #                 song=p2,
        #                 judge=j,
        #             )
        # except self.DoesNotExist:
        #     pass
        # return 'Session Confirmed'
    # def draw_award(self):
    #     cs = self.contestants.order_by('?')
    #     session = self.sessions.get(kind=self.rounds)
    #     p = 0
    #     for c in cs:
    #         session.performances.create(
    #             contestant=c,
    #             position=p,
    #             start=session.start,
    #         )
    #         p += 1
    #     self.status = self.STATUS.ready
    #     self.save()


class Singer(TimeStampedModel):
    """Quartet Relation"""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    PART = Choices(
        (1, 'tenor', 'Tenor'),
        (2, 'lead', 'Lead'),
        (3, 'baritone', 'Baritone'),
        (4, 'bass', 'Bass'),
    )

    name = models.CharField(
        max_length=255,
        unique=True,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    contestant = models.ForeignKey(
        'Contestant',
        related_name='singers',
    )

    person = models.ForeignKey(
        'Person',
        related_name='quartets',
    )

    part = models.IntegerField(
        choices=PART,
    )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def clean(self):
        # if self.contestant.group.kind == Group.CHORUS:
        #     raise ValidationError('Choruses do not have quartet singers.')
        if self.part:
            if [s['part'] for s in self.contestant.singers.values(
                'part'
            )].count(self.part) > 1:
                raise ValidationError('There can not be more than one of the same part in a quartet.')

    class Meta:
        unique_together = (
            ('contestant', 'person',),
        )
        ordering = (
            '-name',
        )

    def save(self, *args, **kwargs):
        self.name = u"{0} {1} {2}".format(
            self.contestant,
            self.get_part_display(),
            self.person,
        )
        super(Singer, self).save(*args, **kwargs)


class Song(TimeStampedModel):
    STATUS = Choices(
        (0, 'new', 'New',),
        # (10, 'built', 'Built',),
        # (20, 'entered', 'Entered',),
        # (30, 'flagged', 'Flagged',),
        # (35, 'validated', 'Validated',),
        (40, 'confirmed', 'Confirmed',),
        (50, 'final', 'Final',),
    )

    ORDER = Choices(
        (1, 'first', 'First'),
        (2, 'second', 'Second'),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
    )

    status_monitor = MonitorField(
        help_text="""Status last updated""",
        monitor='status',
    )

    performance = models.ForeignKey(
        'Performance',
        related_name='songs',
    )

    order = models.IntegerField(
        choices=ORDER,
    )

    title = models.CharField(
        max_length=255,
        blank=True,
    )

    arranger = models.CharField(
        max_length=255,
        blank=True,
    )

    is_parody = models.BooleanField(
        default=False,
    )

    catalog = models.ForeignKey(
        'Catalog',
        related_name='songs',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    tune = models.ForeignKey(
        'Tune',
        related_name='songs',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    # Denormalized values
    mus_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    prs_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    sng_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    total_points = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    mus_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    prs_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    sng_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    total_score = models.FloatField(
        null=True,
        blank=True,
        editable=False,
    )

    class Meta:
        ordering = [
            'performance',
            'order',
        ]
        unique_together = (
            ('performance', 'order',),
        )

    def __unicode__(self):
        return u"{0}".format(self.name)

    def save(self, *args, **kwargs):
        self.name = u"{0} {1} {2}".format(
            self.performance,
            'Song',
            self.order,
        )
        super(Song, self).save(*args, **kwargs)

    def calculate(self):
        if self.scores.exists():
            # Only use the Scores model when we have scores
            # from a judging panel.  Otherwise, use what's
            # already there (typically imported).
            scores = self.scores.exclude(
                kind=self.scores.model.KIND.practice,
            ).order_by(
                'category',
            ).values(
                'category',
            ).annotate(
                total=models.Sum('points')
            )
            for score in scores:
                if score['category'] == self.scores.model.CATEGORY.music:
                    self.mus_points = score['total']
                if score['category'] == self.scores.model.CATEGORY.presentation:
                    self.prs_points = score['total']
                if score['category'] == self.scores.model.CATEGORY.singing:
                    self.sng_points = score['total']

            # Calculate total points.
            try:
                self.total_points = sum([
                    self.mus_points,
                    self.prs_points,
                    self.sng_points,
                ])
            except TypeError:
                self.total_points = None

            # Calculate percentile scores.
            try:
                possible = self.performance.session.contest.size
                self.mus_score = round(self.mus_points / possible, 1)
                self.prs_score = round(self.prs_points / possible, 1)
                self.sng_score = round(self.sng_points / possible, 1)
                self.total_score = round(self.total_points / (possible * 3), 1)
            except TypeError:
                self.mus_score = None
                self.prs_score = None
                self.sng_score = None
    # @transition(
    #     field=status,
    #     source=[
    #         STATUS.new,
    #     ],
    #     target=STATUS.entered,
    #     conditions=[
    #         song_entered,
    #     ]
    # )
    # def enter(self):
    #     # Triggered from form/admin
    #     return

    @transition(
        field=status,
        source=[
            STATUS.new,
        ],
        target=STATUS.confirmed,
        conditions=[
            song_entered,
            # TODO could put `performance_finished` here if want to prevent UI
        ]
    )
    def confirm(self):
        # Triggered from performance.finish()
        return

    @transition(
        field=status,
        source=STATUS.confirmed,
        target=STATUS.final,
    )
    def finalize(self):
        return


class Tune(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=200,
        unique=True,
    )

    slug = AutoSlugField(
        populate_from='name',
        always_update=True,
        unique=True,
        max_length=255,
    )

    @staticmethod
    def autocomplete_search_fields():
            return ("id__iexact", "name__icontains",)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return u"{0}".format(self.name)


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    email = models.EmailField(
        unique=True,
        help_text="""Your email address will be your username.""",
    )
    name = models.CharField(
        max_length=200,
        help_text="""Your full name.""",
    )
    is_active = models.BooleanField(
        default=True,
    )
    is_staff = models.BooleanField(
        default=False,
    )
    date_joined = models.DateField(
        auto_now_add=True,
    )

    objects = UserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email
