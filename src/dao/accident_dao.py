from src.config.config import get_supabase
from datetime import datetime

class AccidentDAO:
    def __init__(self):
        self.supabase = get_supabase()
        self.table = "accidents"

    def add_accident(self, location, severity, reported_by, zone_id):
        accident = {
            "location": location,
            "severity": severity,
            "reported_by": reported_by,
            "zone_id": zone_id,
            "time": datetime.now().isoformat()
        }
        return self.supabase.table(self.table).insert(accident).execute()

    def get_accident(self, accident_id):
        res = self.supabase.table(self.table).select("*").eq("accident_id", accident_id).execute()
        return res.data[0] if res.data else None

    def update_accident(self, accident_id, update_data):
        return self.supabase.table(self.table).update(update_data).eq("accident_id", accident_id).execute()

    def delete_accident(self, accident_id):
        return self.supabase.table(self.table).delete().eq("accident_id", accident_id).execute()

    def get_accidents_by_zone(self, zone_id):
        res = self.supabase.table(self.table).select("*").eq("zone_id", zone_id).execute()
        return res.data


    def get_accidents_by_zone_and_month(self, zone_id, month):
        res = self.supabase.table(self.table)\
                .select("*")\
                .eq("zone_id", zone_id)\
                .execute()

    
        accidents = [a for a in res.data if a["time"].startswith(f"{month}-")]
        return accidents
    def get_all_accidents(self):
        res = self.supabase.table(self.table).select("*").execute()
        return res.data

