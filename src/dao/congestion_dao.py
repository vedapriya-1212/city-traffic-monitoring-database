from src.config.config import get_supabase
from datetime import datetime

class CongestionDAO:
    def __init__(self):
        self.supabase = get_supabase()
        self.table = "congestion"

    def add_or_update_congestion(self, zone_id, vehicle_count, accident_count, avg_congestion=None):
        """
        Adds a new congestion record or updates an existing one.
        avg_congestion: float percentage (0-100)
        """

       
        if vehicle_count > 50 or accident_count > 2:
            level = "High"
        elif vehicle_count > 20 or accident_count > 0:
            level = "Moderate"
        else:
            level = "Low"

        data = {
            "zone_id": zone_id,
            "vehicle_count": vehicle_count,
            "accident_count": accident_count,
            "level": level,  
            "timestamp": datetime.now().isoformat()
        }

        if avg_congestion is not None:
            data["average_congestion"] = round(avg_congestion, 2)

        
        existing = self.supabase.table(self.table).select("*").eq("zone_id", zone_id).execute()
        if existing.data:
            return self.supabase.table(self.table).update(data).eq("zone_id", zone_id).execute()
        else:
            return self.supabase.table(self.table).insert(data).execute()

    def get_congestion(self, zone_id):
        
        res = self.supabase.table(self.table).select("*").eq("zone_id", zone_id).execute()
        return res.data[0] if res.data else None
    def get_all_congestion(self):
        res = self.supabase.table(self.table).select("*").execute()
        return res.data