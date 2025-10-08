from src.dao import congestion_dao, vehicle_dao, accident_dao

class CongestionService:
    def __init__(self):
        self.dao = congestion_dao.CongestionDAO()
        self.vehicle_dao = vehicle_dao.VehicleDAO()
        self.accident_dao = accident_dao.AccidentDAO()

    def calculate_average_congestion(self, zone_id, max_capacity: int):
        """
        Calculates average congestion percentage for a given zone.
        Formula: (vehicles / max_capacity) * 100
        Accident factor: +5% per accident
        """
        vehicles = self.vehicle_dao.get_vehicles_by_zone(zone_id)
        vehicle_count = len(vehicles)

        accidents = self.accident_dao.get_accidents_by_zone(zone_id)
        accident_count = len(accidents)

        base_congestion = (vehicle_count / max_capacity) * 100 if max_capacity > 0 else 0
        adjusted_congestion = base_congestion + (accident_count * 5)
        if adjusted_congestion > 100:
            adjusted_congestion = 100

        
        self.dao.add_or_update_congestion(zone_id, vehicle_count, accident_count, avg_congestion=adjusted_congestion)

        return {
            "zone_id": zone_id,
            "vehicles": vehicle_count,
            "accidents": accident_count,
            "max_capacity": max_capacity,
            "average_congestion": round(adjusted_congestion, 2)
        }

    def view_congestion(self, zone_id):
        return self.dao.get_congestion(zone_id)
