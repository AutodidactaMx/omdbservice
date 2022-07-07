from rest_framework import serializers


class MovieSerializer(serializers.Serializer):

    name = serializers.CharField(
        required=True
    )
    year_start = serializers.IntegerField(
        required=True,
        allow_null=True
    )
    year_end = serializers.IntegerField(
        required=True,
        allow_null=True
    )
    
class SearchMovieSerializer(serializers.Serializer):

    frequency_actors = serializers.DictField()
    historical_years = serializers.DictField()
    top_reted = serializers.DictField()