import argparse
from src.services.vehicle_service import VehicleService
from src.services.accident_service import AccidentService
from src.services.congestion_service import CongestionService
from src.services.zone_service import ZoneService

class TrafficMonitoringCLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="City Traffic Monitoring CLI")
        self.parser.add_argument("--menu", action="store_true", help="Run in menu-driven mode")

        # Services
        self.vehicle_service = VehicleService()
        self.accident_service = AccidentService()
        self.congestion_service = CongestionService()
        self.zone_service = ZoneService()

    def run(self):
        args = self.parser.parse_args()
        if args.menu:
            self.menu_loop()
        else:
            print("Please run with --menu for menu-driven mode.")

    def menu_loop(self):
        while True:
            print("\n--- City Traffic Monitoring Menu ---")
            print("1. Add Vehicle")
            print("2. View Vehicle")
            print("3. Update Vehicle Exit")
            print("4. Delete Vehicle")
            print("5. Add Accident")
            print("6. View Accident")
            print("7. Update Accident")
            print("8. Delete Accident")
            print("9. Calculate Congestion")
            print("10. View Congestion (by Zone)")
            print("11. Add Zone")
            print("12. View Zone")
            print("13. Update Zone")
            print("14. Delete Zone")
            print("15. Generate Traffic Report by Zone/Month")
            print("16. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1": self.add_vehicle()
            elif choice == "2": self.view_vehicle()
            elif choice == "3": self.update_vehicle_exit()
            elif choice == "4": self.delete_vehicle()
            elif choice == "5": self.add_accident()
            elif choice == "6": self.view_accident()
            elif choice == "7": self.update_accident()
            elif choice == "8": self.delete_accident()
            elif choice == "9": self.calculate_congestion()
            elif choice == "10": self.view_congestion()
            elif choice == "11": self.add_zone()
            elif choice == "12": self.view_zone()
            elif choice == "13": self.update_zone()
            elif choice == "14": self.delete_zone()
            elif choice == "15": self.generate_traffic_report()
            elif choice == "16":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

    #Vehicle Methods
    def add_vehicle(self):
        vtype = input("Enter vehicle type (Car/Bike/Bus): ")
        plate = input("Enter vehicle license plate: ")
        zone = int(input("Enter zone ID: "))
        result = self.vehicle_service.add_vehicle(vtype, plate, zone)
        print("Vehicle added:", result)

    def view_vehicle(self):
        plate = input("Enter vehicle license plate: ")
        vehicle = self.vehicle_service.view_vehicle(plate)
        print("Vehicle details:", vehicle)

    def update_vehicle_exit(self):
        plate = input("Enter vehicle license plate: ")
        self.vehicle_service.update_vehicle_exit(plate)
        print("Vehicle exit time updated!")

    def delete_vehicle(self):
        plate = input("Enter vehicle license plate: ")
        self.vehicle_service.delete_vehicle(plate)
        print("Vehicle deleted!")

    #Accident Methods
    def add_accident(self):
        location = input("Enter accident location: ")
        severity = input("Enter severity (Minor/Moderate/Severe): ")
        reported_by = input("Reported by: ")
        zone = int(input("Enter zone ID: "))
        result = self.accident_service.add_accident(location, severity, reported_by, zone)
        print("Accident reported:", result)

    def view_accident(self):
        accident_id = int(input("Enter Accident ID: "))
        accident = self.accident_service.view_accident(accident_id)
        print("Accident details:", accident)

    def update_accident(self):
        accident_id = int(input("Enter Accident ID: "))
        field = input("Enter field to update (location/severity/zone): ")
        value = input("Enter new value: ")
        result = self.accident_service.update_accident(accident_id, {field: value})
        print("Accident updated:", result)

    def delete_accident(self):
        accident_id = int(input("Enter Accident ID: "))
        self.accident_service.delete_accident(accident_id)
        print("Accident deleted!")

    #Congestion Methods
    def calculate_congestion(self):
        zone = int(input("Enter zone ID: "))
        max_capacity = int(input("Enter max vehicle capacity for this zone: "))
        result = self.congestion_service.calculate_average_congestion(zone, max_capacity)
        print(f"Average congestion updated for zone {zone}:", result)

    def view_congestion(self):
        zone = int(input("Enter zone ID: "))
        congestion = self.congestion_service.view_congestion(zone)
        print(f"Congestion details for zone {zone}:", congestion)

    #Zone Methods
    def add_zone(self):
        name = input("Zone name: ")
        lat = float(input("Latitude: "))
        lon = float(input("Longitude: "))
        officer = input("Traffic Officer: ")
        result = self.zone_service.add_zone(name, lat, lon, officer)
        print("Zone added:", result)

    def view_zone(self):
        zone_id = int(input("Enter Zone ID: "))
        result = self.zone_service.view_zone(zone_id)
        print("Zone details:", result)

    def update_zone(self):
        zone_id = int(input("Enter Zone ID: "))
        field = input("Field to update (zone_name/latitude/longitude/traffic_officer): ")
        value = input("New value: ")
        result = self.zone_service.update_zone(zone_id, {field: value})
        print("Zone updated:", result)

    def delete_zone(self):
        zone_id = int(input("Enter Zone ID: "))
        self.zone_service.delete_zone(zone_id)
        print("Zone deleted!")

    # Traffic Report Method
    def generate_traffic_report(self):
        zone_id = int(input("Enter Zone ID: "))
        month = input("Enter month (YYYY-MM): ")
        try:
            vehicles = self.vehicle_service.get_vehicles_by_zone_and_month(zone_id, month)
            accidents = self.accident_service.get_accidents_by_zone_and_month(zone_id, month)
            vehicle_count = len(vehicles)
            accident_count = len(accidents)

            zone = self.zone_service.view_zone(zone_id)
            max_capacity = zone.get("max_capacity", max(vehicle_count, 1))  # fallback

            avg_cong = self.congestion_service.calculate_average_congestion(zone_id, max_capacity=max_capacity)

            report_data = {
                "Zone ID": zone_id,
                "Month": month,
                "Total Vehicles": vehicle_count,
                "Total Accidents": accident_count,
                "Average Congestion %": avg_cong.get("average_congestion", 0)
            }
            print("Traffic Report:")
            for k, v in report_data.items():
                print(f"{k}: {v}")
        except Exception as e:
            print("Error generating traffic report:", e)


if __name__ == "__main__":
    TrafficMonitoringCLI().run()
