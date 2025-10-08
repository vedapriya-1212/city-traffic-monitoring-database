from src.config.config import get_supabase

class ReportDAO:
    def __init__(self):
        self.supabase = get_supabase()
        self.table = "traffic_reports"

    def add_report(self, zone_id, month, total_vehicles, total_accidents, avg_congestion):
        report = {
            "zone_id": zone_id,
            "month": month,
            "total_vehicles": total_vehicles,
            "total_accidents": total_accidents,
            "avg_congestion_level": avg_congestion
        }
        return self.supabase.table(self.table).insert(report).execute()

    def view_report(self, report_id):
        return self.supabase.table(self.table).select("*").eq("report_id", report_id).execute()

    def view_reports_by_zone(self, zone_id):
        return self.supabase.table(self.table).select("*").eq("zone_id", zone_id).execute()
