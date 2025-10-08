from src.dao import accident_dao

class AccidentService:
    def __init__(self):
        self.dao = accident_dao.AccidentDAO()

    def add_accident(self, location, severity, reported_by, zone_id):
        return self.dao.add_accident(location, severity, reported_by, zone_id)

    def view_accident(self, accident_id):
        return self.dao.get_accident(accident_id)

    def update_accident(self, accident_id, update_data):
        return self.dao.update_accident(accident_id, update_data)

    def delete_accident(self, accident_id):
        return self.dao.delete_accident(accident_id)

    def get_accidents_by_zone(self, zone_id):
        return self.dao.get_accidents_by_zone(zone_id)

    def get_accidents_by_zone_and_month(self, zone_id, month):
        return self.dao.get_accidents_by_zone_and_month(zone_id, month)
    def get_all_accidents(self):
        return self.dao.list_all()
    
    