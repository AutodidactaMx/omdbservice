def get_total_pages(json_object) -> int:
    if "totalResults" in json_object:
        total = int(int(json_object["totalResults"]) / 10) + 1
    else:
        total = 0
    return total
