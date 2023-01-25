from .poi_service import POI_Service

poi_service_instance = POI_Service()

# TODO Exception handling
# TODO type hints
def get_all_POI():
    return poi_service_instance.get_all_POI()


def get_POI(poi_id):
    return poi_service_instance.get_POI(poi_id)


def suggest_new_POI():
    return poi_service_instance.suggest_new_POI()
