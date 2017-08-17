from django.db import models

class Human(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        editable=False,
    )
    first_name = models.CharField(
        max_length=255,
        editable=False,
    )
    middle_name = models.CharField(
        max_length=255,
        editable=False,
        db_column='middle_initial',
    )
    last_name = models.CharField(
        max_length=255,
        editable=False,
    )
    nick_name = models.CharField(
        max_length=255,
        editable=False,
        db_column='preferred_name',
    )
    email = models.CharField(
        max_length=255,
        editable=False,
    )
    birth_date = models.DateField(
        editable=False,
        db_column='birthday'
    )
    is_deceased = models.BooleanField(
        editable=False,
    )
    phone = models.CharField(
        max_length=255,
        editable=False,
    )
    cell_phone = models.CharField(
        max_length=255,
        editable=False,
    )
    work_phone = models.CharField(
        max_length=255,
        editable=False,
    )
    bhs_id = models.IntegerField(
        editable=False,
        db_column='legacy_id',
    )
    sex = models.CharField(
        max_length=255,
        editable=False,
    )
    primary_voice_part = models.CharField(
        max_length=255,
        editable=False,
    )
    # Properties
    @property
    def full_name(self):
        if self.nick_name:
            format_nick = "({0})".format(self.nick_name)
        else:
            format_nick = ""
        full_name = " ".join([
            self.first_name,
            self.middle_name,
            self.last_name,
            format_nick,
        ])
        return full_name


    # Internals
    def __str__(self):
        if self.bhs_id:
            nomen = "{0} [{1}]".format(
                self.full_name,
                self.bhs_id,
            )
        else:
            nomen = self.full_name
        return nomen

    class Meta:
        db_table = 'vwMembers'


class Entity(models.Model):
    CHAPTER = 'chapter'
    DISTRICT = 'district'
    ORGANIZATION = 'organization'
    QUARTET = 'quartet'

    KIND_CHOICES = [
        (ORGANIZATION, 'Organization'),
        (DISTRICT, 'District'),
        (CHAPTER, 'Chapter'),
        (QUARTET, 'Quartet'),
    ]

    id = models.CharField(
        primary_key=True,
        max_length=255,
        editable=False,
    )
    name = models.CharField(
        max_length=255,
        editable=False,
    )
    kind = models.CharField(
        max_length=255,
        editable=False,
        choices=KIND_CHOICES,
        db_column='object_type',
    )
    bhs_id = models.IntegerField(
        editable=False,
        db_column='legacy_id',
    )
    chapter_code = models.CharField(
        max_length=255,
        editable=False,
        db_column='legacy_code',
    )
    chorus_name = models.CharField(
        max_length=255,
        editable=False,
    )
    phone = models.CharField(
        max_length=255,
        editable=False,
    )
    email = models.CharField(
        max_length=255,
        editable=False,
    )
    established_date = models.DateField(
        editable=False,
    )
    # FKs
    status = models.ForeignKey(
        'Status',
        related_name='entities',
        editable=False,
    )

    def __str__(self):
        if not self.name:
            name = ""
        else:
            name = self.name
        if self.kind == 'chapter':
            nomen = "{0} [{1}]".format(
                self.chorus_name,
                name,
            )
        else:
            nomen = name
        if not nomen:
            nomen = '(UNKNOWN)'
        return nomen

    class Meta:
        db_table = 'vwStructures'
        verbose_name_plural = 'entities'


class Status(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        editable=False,
    )
    name = models.CharField(
        max_length=255,
        editable=False,
    )
    # Internals
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'vwStatuses'
        verbose_name_plural = 'statuses'


class Membership(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        editable=False,
    )
    # FKs
    entity = models.ForeignKey(
        'Entity',
        related_name='memberships',
        editable=False,
        db_column='object_id',
    )
    status = models.ForeignKey(
        'Status',
        related_name='memberships',
        editable=False,
    )

    # Internals
    def __str__(self):
        return self.id

    class Meta:
        db_table = 'vwMemberships'


class Subscription(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        editable=False,
    )
    valid_through = models.DateField(
        editable=False,
    )
    status = models.CharField(
        max_length=255,
        editable=False,
    )
    # FKs
    human = models.ForeignKey(
        'Human',
        related_name='subscriptions',
        editable=False,
        db_column='members_id',
    )

    # Internals
    def __str__(self):
        return self.id

    class Meta:
        db_table = 'vwSubscriptions'


class SubscriptionMembershipJoin(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        editable=False,
    )
    status = models.BooleanField(
        editable=False,
    )
    vocal_part = models.CharField(
        max_length=255,
        editable=False,
    )
    # FKs
    subscription = models.ForeignKey(
        'Subscription',
        editable=False,
    )
    membership = models.ForeignKey(
        'Membership',
        editable=False,
    )

    # Internals
    def __str__(self):
        return self.id

    class Meta:
        db_table = 'vwSubscriptions_Memberships'