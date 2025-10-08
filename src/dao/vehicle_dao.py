from src.config.config import get_supabase
from datetime import datetime

class VehicleDAO:
    def __init__(self):
        self.supabase = get_supabase()
        self.table = "vehicles"

    def add_vehicle(self, vehicle_type, license_plate, zone_id):
        vehicle = {
            "vehicle_type": vehicle_type,
            "license_plate": license_plate,
            "entry_time": datetime.now().isoformat(),
            "exit_time": None,
            "zone_id": zone_id
        }
        return self.supabase.table(self.table).insert(vehicle).execute()

    def get_vehicle(self, license_plate):
        res = self.supabase.table(self.table).select("*").eq("license_plate", license_plate).execute()
        return res.data[0] if res.data else None

    def update_vehicle_exit(self, license_plate):
        return self.supabase.table(self.table).update({
            "exit_time": datetime.now().isoformat()
        }).eq("license_plate", license_plate).execute()

    def delete_vehicle(self, license_plate):
        return self.supabase.table(self.table).delete().eq("license_plate", license_plate).execute()

    def get_vehicles_by_zone(self, zone_id):
        res = self.supabase.table(self.table).select("*").eq("zone_id", zone_id).is_("exit_time", None).execute()
        return res.data

    
    def get_vehicles_by_zone_and_month(self, zone_id, month):
        res = self.supabase.table(self.table)\
                .select("*")\
                .eq("zone_id", zone_id)\
                .execute()
    
        vehicles = [v for v in res.data if v["entry_time"].startswith(f"{month}-")]
        return vehicles
    def get_all_vehicles(self):
        res = self.supabase.table(self.table).select("*").execute()
        return res.data
