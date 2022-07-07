
from rest_framework import serializers
from movies.model.search_model import SearchLogModel


class SearchLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchLogModel
        fields = [
            "timestamp",
            "search_parameters",
            "year_more_results",
            "year_less_results",
            "actor_more_appearances",
            "actor_less_appearances",
            "rating_min",
            "rating_max",
            "rating_mean",
            "rating_median",
            "rating_std"]
