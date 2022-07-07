from  movies.model.search_model import SearchLogModel


class SearchLogRepository:
    url: str = None

    def __init__(self) -> None:
        pass
    
    def insert(self, searh_log:SearchLogModel) -> None:
        searh_log.save()        
        

