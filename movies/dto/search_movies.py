from rest_framework import serializers

class SearchMovie():
    def __init__(self,frequency_actors:dict = dict(), historical_years:dict= dict(), top_reted:dict = dict()) -> None:        
        self.frequency_actors = frequency_actors
        self.historical_years = historical_years
        self.top_reted = top_reted