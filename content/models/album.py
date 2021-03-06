from django.db import models
from django.conf import settings

from .track import Track
from .genre import Genre
from .contributor import Contributor
from .location import Location

ALBUM = 'content"."album'
ALBUM_CONTRIBUTOR = 'content"."album_contributor'
ALBUM_TRACK = 'content"."album_track'
ALBUM_GENRE = 'content"."album_genre'


class Album(models.Model):
    """
    An album is a collection of one or more tracks.
    It also associates various other metadata as shown here.
    """

    upc = models.BigIntegerField()
    title = models.CharField(max_length=256)
    release_date = models.DateField(null=True)
    upload_date = models.DateField(null=True)
    remaster_date = models.DateField(null=True)
    start_datetime = models.DateField(null=True)
    contributors = models.ManyToManyField(Contributor, through="AlbumContributor")
    tracks = models.ManyToManyField(Track, through="AlbumTrack")
    artwork_id = models.UUIDField(null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    purchase_cost = models.DecimalField(decimal_places=4, max_digits=6, null=True)
    purchase_count = models.BigIntegerField(default=0)
    label_name = models.CharField(max_length=256, null=True)
    notes = models.TextField(null=True)
    genres = models.ManyToManyField(Genre, through="AlbumGenre")
    recording_location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True
    )

    class Meta:
        db_table = ALBUM


class AlbumContributor(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)

    class Meta:
        db_table = ALBUM_CONTRIBUTOR


class AlbumTrack(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)

    class Meta:
        db_table = ALBUM_TRACK


class AlbumGenre(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        db_table = ALBUM_GENRE
