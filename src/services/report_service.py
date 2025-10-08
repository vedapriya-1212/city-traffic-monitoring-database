from src.dao import vehicle_dao, accident_dao

class ReportService:
    def __init__(self):
        self.vehicle_dao = vehicle_dao.VehicleDAO()
        self.accident_dao = accident_dao.AccidentDAO()

    def generate_monthly_report(self, zone_id, year, month, max_capacity=100):
        """
        Generates a traffic report for a zone in a given month/year.
        """
        vehicles = self.vehicle_dao.get_vehicles_by_zone_and_month(zone_id, year, month)
        accidents = self.accident_dao.get_accidents_by_zone_and_month(zone_id, year, month)
        
        total_vehicles = len(vehicles)
        total_accidents = len(accidents)

        # Average congestion calculation
        base_congestion = (total_vehicles / max_capacity) * 100 if max_capacity > 0 else 0
        adjusted_congestion = base_congestion + (total_accidents * 5)
        if adjusted_congestion > 100:
            adjusted_congestion = 100

        return {
            "zone_id": zone_id,
            "year": year,
            "month": month,
            "total_vehicles": total_vehicles,
            "total_accidents": total_accidents,
            "average_congestion": round(adjusted_congestion, 2)
        }
