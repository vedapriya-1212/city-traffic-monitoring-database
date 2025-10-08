from src.dao import zone_dao

class ZoneService:
    def __init__(self):
        self.dao = zone_dao.ZoneDAO()

    def add_zone(self, zone_name, latitude, longitude, traffic_officer, max_capacity=100):
        return self.dao.add_zone(zone_name, latitude, longitude, traffic_officer, max_capacity)

    def view_zone(self, zone_id):
        return self.dao.get_zone(zone_id)

    def update_zone(self, zone_id, update_data):
        return self.dao.update_zone(zone_id, update_data)

    def delete_zone(self, zone_id):
        return self.dao.delete_zone(zone_id)

    def get_all_zones(self):
        return self.dao.get_all_zones()
    def get_zone_by_id(self, zone_id):
        return self.dao.get_zone(zone_id)