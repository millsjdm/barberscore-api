from rest_framework import serializers

from drf_haystack.serializers import HaystackSerializer

from .models import (
    Convention,
    Contest,
    Contestant,
    Group,
    Performance,
    Note,
    Singer,
    Director,
    District,
    Person,
    Song,
)

from .search_indexes import (
    GroupIndex,
    SongIndex,
    PersonIndex,
    ContestIndex,
)

from django.contrib.auth import get_user_model
User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):

    chapterName = serializers.CharField(
        source='chapter_name',
    )

    contestants = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    # lead = serializers.StringRelatedField()

    # tenor = serializers.StringRelatedField()

    # baritone = serializers.StringRelatedField()

    # bass = serializers.StringRelatedField()

    class Meta:
        model = Group
        lookup_field = 'slug'
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'kind',
            'location',
            'website',
            'facebook',
            'twitter',
            'email',
            'phone',
            'picture',
            'description',
            'notes',
            'chapterName',
            # 'lead',
            # 'tenor',
            # 'baritone',
            # 'bass',
            'bsmdb',
            'contestants',
        )


class ContestantSerializer(serializers.ModelSerializer):
    contest = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    performances = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
    )

    district = serializers.StringRelatedField()

    group = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    # lead = serializers.StringRelatedField()

    # tenor = serializers.StringRelatedField()

    # baritone = serializers.StringRelatedField()

    # bass = serializers.StringRelatedField()

    director = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    district = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    lead = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )
    tenor = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )
    baritone = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )
    bass = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    # group = GroupSerializer(
    #     read_only=True,
    # )

    # performances = PerformanceSerializer(
    #     read_only=True,
    #     many=True,
    # )

    quarters_song1 = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    quarters_song2 = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    semis_song1 = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    semis_song2 = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    finals_song1 = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    finals_song2 = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        model = Contestant
        lookup_field = 'slug'
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'contest',
            'group',
            'district',
            'picture',
            'seed',
            'prelim',
            'draw',
            'stagetime',
            'place',
            'points',
            'score',
            'quarters_place',
            'quarters_score',
            'semis_place',
            'semis_score',
            'finals_place',
            'finals_score',
            'finals_mus1_score',
            'finals_mus2_score',
            'semis_mus1_score',
            'semis_mus2_score',
            'quarters_mus1_score',
            'quarters_mus2_score',
            'finals_prs1_score',
            'finals_prs2_score',
            'semis_prs1_score',
            'semis_prs2_score',
            'quarters_prs1_score',
            'quarters_prs2_score',
            'finals_sng1_score',
            'finals_sng2_score',
            'semis_sng1_score',
            'semis_sng2_score',
            'quarters_sng1_score',
            'quarters_sng2_score',
            'quarters_song1',
            'quarters_song2',
            'semis_song1',
            'semis_song2',
            'finals_song1',
            'finals_song2',
            'quarters_song1_score',
            'quarters_song2_score',
            'semis_song1_score',
            'semis_song2_score',
            'finals_song1_score',
            'finals_song2_score',
            'director',
            'lead',
            'tenor',
            'baritone',
            'bass',
            'men',
            'district',
            'performances',
        )


class ContestSerializer(serializers.ModelSerializer):
    contestants = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    district = serializers.StringRelatedField()

    class Meta:
        model = Contest
        lookup_field = 'slug'
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'year',
            'level',
            'kind',
            'district',
            'panel',
            'is_active',
            'is_complete',
            'is_place',
            'is_score',
            'scoresheet_pdf',
            'contestants',
        )


class ConventionSerializer(serializers.ModelSerializer):
    contests = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        model = Convention
        lookup_field = 'slug'
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'dates',
            'year',
            'timezone',
            'contests',
            'is_active',
        )


class SingerSerializer(serializers.ModelSerializer):
    contestants_lead = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    contestants_tenor = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    contestants_baritone = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    contestants_bass = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        model = Singer
        lookup_field = 'slug'
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'contestants_lead',
            'contestants_tenor',
            'contestants_baritone',
            'contestants_bass',
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


class PersonSerializer(serializers.ModelSerializer):
    contestants_director = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    contestants_lead = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    contestants_tenor = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    contestants_baritone = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    contestants_bass = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        model = Person
        lookup_field = 'slug'
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'contestants_director',
            'contestants_lead',
            'contestants_tenor',
            'contestants_baritone',
            'contestants_bass',
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


class DirectorSerializer(serializers.ModelSerializer):
    contestants = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        model = Director
        lookup_field = 'slug'
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'location',
            'website',
            'facebook',
            'twitter',
            'email',
            'phone',
            'picture',
            'description',
            'notes',
            'contestants',
        )


class NoteSerializer(serializers.ModelSerializer):
    performance = serializers.SlugRelatedField(
        queryset=Performance.objects.all(),
        slug_field='slug',
    )

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        # read_only=True,
    )

    class Meta:
        model = Note
        fields = (
            'id',
            'text',
            'performance',
            'user',
        )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
        )


class SongSerializer(serializers.ModelSerializer):
    # contestants = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='slug',
    # )

    class Meta:
        model = Song
        fields = (
            'id',
            'url',
            'slug',
            'name',
            # 'contestants',
        )
        lookup_field = 'slug'


class DistrictSerializer(serializers.ModelSerializer):
    contestants = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug',
    )

    # groups = serializers.SlugRelatedField(
    #     queryset=
    # )

    class Meta:
        model = District
        lookup_field = 'slug'
        fields = (
            'id',
            'url',
            'slug',
            'name',
            'kind',
            'location',
            'website',
            'facebook',
            'twitter',
            'email',
            'phone',
            'picture',
            'description',
            'notes',
            'long_name',
            # 'chapterName',
            # 'lead',
            # 'tenor',
            # 'baritone',
            # 'bass',
            # 'bsmdb',
            'contestants',
        )


class SearchSerializer(HaystackSerializer):
    kind = serializers.CharField(
        source='model_name',
    )

    class Meta:
        index_classes = [
            GroupIndex,
            SongIndex,
            PersonIndex,
            ContestIndex,
        ]
        fields = [
            "text",
            "name",
            "slug",
            "description",
            "kind",
        ]
