from .poi_service import POI_Service

poi_service_instance = POI_Service()


def get_all_POI():
    return poi_service_instance.get_all_POI()


def get_POI(poi_id):
    return poi_service_instance.get_POI(poi_id)
