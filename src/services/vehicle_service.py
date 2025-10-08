from src.dao import vehicle_dao

class VehicleService:
    def __init__(self):
        self.dao = vehicle_dao.VehicleDAO()

    def add_vehicle(self, vehicle_type, license_plate, zone_id):
        return self.dao.add_vehicle(vehicle_type, license_plate, zone_id)

    def view_vehicle(self, license_plate):
        return self.dao.get_vehicle(license_plate)

    def update_vehicle_exit(self, license_plate):
        return self.dao.update_vehicle_exit(license_plate)

    def delete_vehicle(self, license_plate):
        return self.dao.delete_vehicle(license_plate)

    def get_vehicles_by_zone(self, zone_id):
        return self.dao.get_vehicles_by_zone(zone_id)

    def get_vehicles_by_zone_and_month(self, zone_id, month):
        return self.dao.get_vehicles_by_zone_and_month(zone_id, month)

    def get_all_vehicles(self):
        return self.dao.list_all()