from django.db import models


class SearchLogModel(models.Model):    
    auto_increment_id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    search_parameters = models.CharField(max_length=200)
    year_more_results = models.CharField(max_length=50)
    year_less_results = models.CharField(max_length=50)
    actor_more_appearances = models.CharField(max_length=50)
    actor_less_appearances = models.CharField(max_length=50)
    rating_min= models.FloatField()
    rating_max = models.FloatField()
    rating_mean = models.FloatField()
    rating_median = models.FloatField()
    rating_std = models.FloatField()