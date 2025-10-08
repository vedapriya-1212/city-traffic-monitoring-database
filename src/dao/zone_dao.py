from src.config.config import get_supabase
from datetime import datetime

class ZoneDAO:
    def __init__(self):
        self.supabase = get_supabase()
        self.table = "zones"

    def add_zone(self, zone_name, latitude, longitude, traffic_officer, max_capacity=100):
        data = {
            "zone_name": zone_name,
            "latitude": latitude,
            "longitude": longitude,
            "traffic_officer": traffic_officer,
            "max_capacity": max_capacity,
            "created_at": datetime.now().isoformat()
        }
        return self.supabase.table(self.table).insert(data).execute()

    def get_zone(self, zone_id):
        res = self.supabase.table(self.table).select("*").eq("zone_id", zone_id).execute()
        return res.data[0] if res.data else None

    def update_zone(self, zone_id, update_data):
        return self.supabase.table(self.table).update(update_data).eq("zone_id", zone_id).execute()

    def delete_zone(self, zone_id):
        return self.supabase.table(self.table).delete().eq("zone_id", zone_id).execute()

    def get_all_zones(self):
        res = self.supabase.table(self.table).select("*").execute()
        return res.data
    
    def get_all_zones(self):
        res = self.supabase.table(self.table).select("*").execute()
        return res.data
