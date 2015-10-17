from django.contrib import admin
from django_object_actions import (
    DjangoObjectActions,
    takes_instance_or_queryset,
)

from easy_select2 import select2_modelform

from .models import (
    Convention,
    Contest,
    Contestant,
    Group,
    District,
    Song,
    Person,
    Performance,
    Score,
    Judge,
    Singer,
    Director,
    Catalog,
    Award,
    Event,
    Appearance,
)


class PerformancesInline(admin.TabularInline):
    form = select2_modelform(
        Performance,
        attrs={'width': '100px'},
    )
    fields = (
        'appearance',
        'order',
        'catalog',
        'mus_points',
        'prs_points',
        'sng_points',
    )
    ordering = (
        'appearance',
        'order',
    )
    model = Performance
    extra = 0
    raw_id_fields = (
        'appearance',
        'catalog',
    )
    can_delete = True
    show_change_link = True


class ScoresInline(admin.TabularInline):
    # form = select2_modelform(
    #     Score,
    #     attrs={'width': '300px'},
    # )
    fields = (
        'judge',
        'category',
        'points',
    )
    ordering = (
        'category',
    )
    model = Score
    extra = 0
    # raw_id_fields = (
    #     'judge',
    # )
    can_delete = True
    show_change_link = True


class JudgesInline(admin.TabularInline):
    model = Judge
    form = select2_modelform(
        Judge,
        attrs={'width': '100px'},
    )
    fields = (
        'contest',
        'person',
        'part',
        'num',
    )
    ordering = (
        'part',
        'num',
    )
    extra = 0
    raw_id_fields = (
        'person',
        'contest',
    )
    can_delete = True
    show_change_link = True


class SingersInline(admin.TabularInline):
    model = Singer
    form = select2_modelform(
        Singer,
        attrs={'width': '100px'},
    )
    fields = (
        'contestant',
        'person',
        'part',
    )
    ordering = (
        'part',
        'contestant',
    )
    extra = 0
    raw_id_fields = (
        'person',
        'contestant',
    )
    can_delete = True
    show_change_link = True


class DirectorsInline(admin.TabularInline):
    form = select2_modelform(
        Director,
        attrs={'width': '100px'},
    )
    fields = (
        'contestant',
        'person',
        'part',
    )
    ordering = (
        'part',
        'contestant',
    )
    model = Director
    extra = 0
    raw_id_fields = (
        'person',
        'contestant',
    )
    can_delete = True


class CatalogsInline(admin.TabularInline):
    model = Catalog
    fields = (
        'person',
        'song',
    )
    extra = 0
    raw_id_fields = (
        'song',
        'person',
    )
    can_delete = True
    show_change_link = True


class AwardsInline(admin.TabularInline):
    model = Award
    fields = (
        'name',
    )
    extra = 0
    can_delete = True
    show_change_link = True


class ContestantsInline(admin.TabularInline):
    form = select2_modelform(
        Contestant,
        attrs={'width': '100px'},
    )
    fields = (
        'contest',
        'group',
        'district',
        'seed',
        'prelim',
        'place',
        'score',
        'men',
    )
    ordering = (
        'place',
        'seed',
        'group',
    )
    show_change_link = True

    model = Contestant
    extra = 0
    raw_id_fields = (
        'contest',
        'group',
    )
    can_delete = True
    readonly_fields = (
        'group',
    )


class AppearancesInline(admin.TabularInline):
    form = select2_modelform(
        Appearance,
        attrs={'width': '100px'},
    )
    fields = (
        'contestant',
        'session',
        'draw',
        'start',
    )
    ordering = (
        'session',
        'draw',
        'contestant',
    )
    show_change_link = True

    model = Appearance
    extra = 0
    raw_id_fields = (
        'contestant',
    )
    can_delete = True
    readonly_fields = (
        'contestant',
    )


@admin.register(Convention)
class ConventionAdmin(admin.ModelAdmin):
    form = select2_modelform(
        Convention,
        attrs={'width': '100px'},
    )

    search_fields = (
        'name',
    )

    list_display = (
        'name',
        'location',
        'dates',
        'kind',
        'year',
        'district',
        'is_active',
    )

    fields = (
        'is_active',
        'name',
        ('location', 'timezone',),
        'dates',
        ('start', 'end',),
        'district',
        'kind',
        'year',
    )

    list_filter = (
        'kind',
        'year',
        'district',
    )

    readonly_fields = (
        'name',
    )

    save_on_top = True


@admin.register(Contest)
class ContestAdmin(DjangoObjectActions, admin.ModelAdmin):
    @takes_instance_or_queryset
    def import_legacy(self, request, queryset):
        for obj in queryset:
            obj.import_legacy()
    import_legacy.label = 'Import Legacy'
    form = select2_modelform(
        Contest,
        attrs={'width': '100px'},
    )
    save_on_top = True
    objectactions = [
        'import_legacy',
    ]

    inlines = [
        JudgesInline,
        ContestantsInline,
    ]

    search_fields = (
        'name',
    )

    list_filter = (
        'level',
        'kind',
        'year',
        'district',
    )

    list_display = (
        'name',
        'panel',
        'scoresheet_pdf',
        'scoresheet_csv',
        'is_active',
        'status',
    )

    fields = (
        'is_active',
        'status',
        'name',
        'convention',
        'level',
        'kind',
        'year',
        'district',
        'panel',
        'scoresheet_pdf',
        'scoresheet_csv',
    )

    raw_id_fields = (
        'convention',
    )

    readonly_fields = (
        'name',
    )


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    form = select2_modelform(
        Group,
        attrs={'width': '100px'},
    )

    search_fields = (
        'name',
    )

    list_display = (
        'name',
        'location',
        'website',
        'facebook',
        'twitter',
        'email',
        'phone',
        'chapter_name',
        'chapter_code',
        'picture',
    )

    fields = (
        'is_active',
        'name',
        'kind',
        ('start_date', 'end_date',),
        'location',
        'website',
        'facebook',
        'twitter',
        'email',
        'phone',
        'picture',
        'description',
        ('chapter_name', 'chapter_code',),
        'notes',
    )

    list_filter = (
        'kind',
    )

    inlines = [
        ContestantsInline,
    ]

    save_on_top = True


@admin.register(Contestant)
class ContestantAdmin(admin.ModelAdmin):
    @takes_instance_or_queryset
    def update_contestants(self, request, queryset):
        for obj in queryset:
            obj.save()
    update_contestants.label = 'Update Contestants'

    form = select2_modelform(
        Contestant,
        attrs={'width': '150px'},
    )

    objectactions = [
        'update_contestants',
    ]

    inlines = [
        SingersInline,
        DirectorsInline,
        AwardsInline,
        AppearancesInline,
    ]

    list_display = (
        'name',
        'place',
        'score',
        'points',
        'men',
    )

    search_fields = (
        'name',
    )

    list_filter = (
        'contest__level',
        'contest__kind',
        'contest__year',
    )

    raw_id_fields = (
        'contest',
        'group',
    )

    fields = (
        (
            'contest',
        ), (
            'group',
        ), (
            'district',
        ), (
            'seed',
            'prelim',
        ), (
            'place',
            'score',
        ),
    )

    readonly_fields = (
        'name',
    )

    save_on_top = True


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    form = select2_modelform(
        Song,
        attrs={'width': '100px'},
    )

    save_on_top = True
    fields = (
        'name',
    )

    search_fields = (
        'name',
    )

    inlines = [
        CatalogsInline,
    ]


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    form = select2_modelform(
        District,
        attrs={'width': '100px'},
    )

    search_fields = (
        'name',
    )

    list_display = (
        'name',
        'location',
        'website',
        'facebook',
        'twitter',
        'email',
        'phone',
        'picture',
        'long_name',
        'kind',
    )

    fields = (
        'is_active',
        'name',
        'long_name',
        'kind',
        ('start_date', 'end_date',),
        'location',
        'website',
        'facebook',
        'twitter',
        'email',
        'phone',
        'picture',
        'description',
        'notes',
    )

    list_filter = (
        'kind',
    )

    save_on_top = True


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    form = select2_modelform(
        Person,
        attrs={'width': '100px'},
    )

    search_fields = (
        'name',
    )

    save_on_top = True
    list_display = (
        'name',
        'location',
        'website',
        'facebook',
        'twitter',
        'email',
        'phone',
        'picture',
    )

    fields = (
        'is_active',
        'name',
        'kind',
        ('start_date', 'end_date',),
        'location',
        'website',
        'facebook',
        'twitter',
        'email',
        'phone',
        'picture',
        'description',
        'notes',
    )

    inlines = [
        DirectorsInline,
        SingersInline,
        CatalogsInline,
        JudgesInline,
    ]


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = (
        'name',
        'catalog',
        'order',
        'mus_points',
        'prs_points',
        'sng_points',
    )

    search_fields = (
        'name',
    )

    fields = (
        (
            'name',
        ),
        (
            'order',
        ),
        (
            'catalog',
        ),
        (
            'mus_points',
            'prs_points',
            'sng_points',
        ),
        (
            'penalty',
        ),
    )

    inlines = [
        ScoresInline,
    ]

    list_filter = (
        'appearance__contestant__contest__level',
        'appearance__contestant__contest__kind',
        'appearance__contestant__contest__year',
    )

    readonly_fields = (
        'name',
    )
    raw_id_fields = (
        'appearance',
        'catalog',
    )


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = (
        'song',
        'person',
        'bhs_id',
        'bhs_published',
        'bhs_fee',
        'bhs_difficulty',
        'bhs_tempo',
        'bhs_medley',
    )
    raw_id_fields = (
        'song',
        'person',
    )
    search_fields = (
        'song__name',
        'person__name',
    )
    inlines = [
        PerformancesInline,
    ]
    list_display = [
        'name',
        'song',
        'bhs_songname',
        'person',
        'bhs_arranger',
        'bhs_id',
        # 'bhs_published',
        # 'bhs_fee',
        # 'bhs_difficulty',
        # 'bhs_tempo',
        # 'bhs_medley',
    ]


@admin.register(Event)
class Event(admin.ModelAdmin):
    save_on_top = True
    fields = (
        'is_active',
        'name',
        ('start', 'end'),
        'convention',
        'contest',
        'contestant',
        'kind',
        'draw',
        'location',
    )
    list_display = [
        'name',
        'start',
        'end',
        'convention',
        'contest',
        'contestant',
        'kind',
        'draw',
    ]
    raw_id_fields = (
        'convention',
        'contest',
        'contestant',
    )


@admin.register(Appearance)
class Appearance(admin.ModelAdmin):
    save_on_top = True
    inlines = [
        PerformancesInline,
    ]
    list_display = [
        'name',
        'draw',
        'start',
    ]
    list_filter = [
        'session',
        'contestant__contest',
    ]


@admin.register(Score)
class Score(admin.ModelAdmin):
    save_on_top = True
