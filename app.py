import streamlit as st
from datetime import datetime

from src.services.vehicle_service import VehicleService
from src.services.accident_service import AccidentService
from src.services.congestion_service import CongestionService
from src.services.zone_service import ZoneService


vehicle_service = VehicleService()
accident_service = AccidentService()
congestion_service = CongestionService()
zone_service = ZoneService()


if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'


st.set_page_config(page_title="City Traffic Monitoring System", layout="wide")


# =========================================================
# FUNCTION FOR THE MAIN APPLICATION TABS (Your Original Code)
# =========================================================
def show_main_app():
    """Displays the main traffic management application with all tabs (Vehicles, Accidents, Zones, etc.)."""
    st.title("🚦 City Traffic Monitoring Dashboard")

    # 1. Enhanced Tab Titles with Emojis for Elegance and Clarity
    tabs = st.tabs([
        "🚗 *Vehicles*",
        "💥 *Accidents*",
        "🗺 *Zones*",
        "📈 *Congestion*",
        "🧾 *Traffic Report*",
        "🔒 *Admin*"
    ])

    # ---------------------------------------------------------
    # TAB 1: VEHICLES
    # ---------------------------------------------------------
    with tabs[0]:
        st.markdown("### 🚗 Vehicle Management")
        st.info("Manage vehicle entry, exit, and information.")

        with st.container(border=True):
            # Added unique key for action radio to prevent conflicts
            action = st.radio("Select Action", ["Add Vehicle", "View Vehicle", "Update Exit", "Delete Vehicle"], key="vehicle_action_main")

        if action == "Add Vehicle":
            st.subheader("Register New Vehicle Entry")
            col1, col2, col3 = st.columns(3)
            with col1:
                vtype = st.text_input("Vehicle Type (e.g., Car, Bike)", key="vtype")
            with col2:
                plate = st.text_input("License Plate", key="plate")
            with col3:
                zone = st.number_input("Zone ID", min_value=1, key="zone_vehicle")

            if st.button("Add Vehicle", use_container_width=True, key="btn_add_vehicle"):
                result = vehicle_service.add_vehicle(vtype, plate, zone)
                st.success(f"✅ Vehicle Added: {result}")

        elif action == "View Vehicle":
            st.subheader("Retrieve Vehicle Details")
            plate = st.text_input("License Plate", key="view_plate")
            if st.button("Get Vehicle Details", use_container_width=True, key="btn_view_vehicle"):
                data = vehicle_service.view_vehicle(plate)
                st.dataframe(data)

        elif action == "Update Exit":
            st.subheader("Mark Vehicle Exit")
            plate = st.text_input("License Plate", key="exit_plate")
            if st.button("Update Exit Time", use_container_width=True, key="btn_update_exit"):
                result = vehicle_service.update_vehicle_exit(plate)
                st.success(f"✅ Exit Time Updated: {result}")

        elif action == "Delete Vehicle":
            st.subheader("Remove Vehicle Record")
            plate = st.text_input("License Plate", key="delete_plate")
            if st.button("Delete Vehicle", use_container_width=True, key="btn_delete_vehicle"):
                result = vehicle_service.delete_vehicle(plate)
                st.warning(f"⚠ Vehicle Deleted: {result}")

    # ---------------------------------------------------------
    # TAB 2: ACCIDENTS
    # ---------------------------------------------------------
    with tabs[1]:
        st.markdown("### 💥 Accident Management")
        st.info("Report new accidents and view incident history.")

        with st.container(border=True):
            action = st.radio("Select Action", ["Report Accident", "View Accident by Zone"], key="accident_action_main")

        if action == "Report Accident":
            st.subheader("Report New Incident")
            col1, col2 = st.columns(2)
            with col1:
                location = st.text_input("Location Details", key="acc_loc")
                severity = st.selectbox("Severity", ["Low", "Moderate", "Severe"], key="acc_sev")
            with col2:
                reported_by = st.text_input("Reported By", key="acc_rep")
                zone = st.number_input("Zone ID", min_value=1, key="acc_zone")

            if st.button("🚨 Report Accident", use_container_width=True, key="btn_report_accident"):
                result = accident_service.add_accident(location, severity, reported_by, zone)
                st.success(f"✅ Accident Reported: {result}")

        elif action == "View Accident by Zone":
            st.subheader("Accidents in a Specific Zone")
            zone = st.number_input("Zone ID", min_value=1, key="view_acc_zone")
            if st.button("View Accidents", use_container_width=True, key="btn_view_accidents"):
                data = accident_service.get_accidents_by_zone(zone)
                st.dataframe(data)

    # ---------------------------------------------------------
    # TAB 3: ZONES
    # ---------------------------------------------------------
    with tabs[2]:
        st.markdown("### 🗺 Zone Management")
        st.info("Define new city zones and view existing zone data.")

        with st.container(border=True):
            action = st.radio("Select Action", ["Add Zone", "View All Zones"], key="zone_action_main")

        if action == "Add Zone":
            st.subheader("Create New Traffic Zone")
            col1, col2, col3 = st.columns(3)
            with col1:
                name = st.text_input("Zone Name", key="zone_name")
                lat = st.number_input("Latitude", format="%.6f", key="zone_lat")
            with col2:
                lon = st.number_input("Longitude", format="%.6f", key="zone_lon")
                officer = st.text_input("Traffic Officer", key="zone_officer")
            with col3:
                max_capacity = st.number_input("Max Vehicle Capacity", min_value=1, key="zone_capacity")

            if st.button("Add Zone", use_container_width=True, key="btn_add_zone"):
                result = zone_service.add_zone(name, lat, lon, officer, max_capacity)
                st.success(f"✅ Zone Created: {result}")

        elif action == "View All Zones":
            st.subheader("All Defined Traffic Zones")
            data = zone_service.get_all_zones()
            st.dataframe(data)

    # ---------------------------------------------------------
    # TAB 4: CONGESTION
    # ---------------------------------------------------------
    with tabs[3]:
        st.markdown("### 📈 Congestion Data")
        st.info("Calculate and monitor real-time congestion levels.")

        with st.container(border=True):
            # Combined action for simplicity since 'update' is now a side-effect of 'calculate'
            action = st.radio("Select Action", ["View Latest Congestion", "Calculate & View Now"], key="cong_action_main")

        if action == "Calculate & View Now":
            st.subheader("Force Real-time Congestion Calculation")
            zone = st.number_input("Zone ID to Calculate", min_value=1, key="cong_zone_calc")

            if st.button("Calculate and Update Status", use_container_width=True, key="btn_calc_cong"):
                # 1. Get capacity needed for calculation
                zone_details = zone_service.get_zone_by_id(zone)
                max_capacity = zone_details.get("max_capacity", 1)
                
                # 2. Call the service method (which calculates and saves)
                data = congestion_service.calculate_average_congestion(zone, max_capacity)
                st.success("✅ Congestion Status Calculated and Updated!")
                st.json(data)
                
        elif action == "View Latest Congestion":
            st.subheader("Latest Recorded Congestion for a Zone")
            zone = st.number_input("Zone ID to View", min_value=1, key="view_cong_zone")
            if st.button("Get Congestion Info", use_container_width=True, key="btn_view_cong"):
                data = congestion_service.view_congestion(zone)
                st.json(data)

    # ---------------------------------------------------------
    # TAB 5: TRAFFIC REPORT
    # ---------------------------------------------------------
    with tabs[4]:
        st.markdown("### 🧾 Monthly Traffic Report")
        st.info("Generate comprehensive traffic reports for a specific zone and month.")

        st.subheader("Report Parameters")
        col1, col2 = st.columns(2)
        with col1:
            zone = st.number_input("Zone ID", min_value=1, key="report_zone")
        with col2:
            month = st.text_input("Enter month (YYYY-MM)", value=datetime.now().strftime("%Y-%m"), key="report_month", help="Example: 2023-10")

        if st.button("Generate Report 📄", use_container_width=True, key="btn_generate_report"):
            st.subheader(f"Report for Zone {zone} - {month}")
            try:
                with st.spinner('Generating report...'):
                    # Retrieve data using services
                    vehicles = vehicle_service.get_vehicles_by_zone_and_month(zone, month)
                    accidents = accident_service.get_accidents_by_zone_and_month(zone, month)
                    zone_details = zone_service.get_zone_by_id(zone)

                    vehicle_count = len(vehicles)
                    accident_count = len(accidents)

                    # Handle division by zero safeguard
                    max_capacity = zone_details.get("max_capacity", 1) 

                    # Calculation requires capacity, assuming the service handles it
                    avg_cong = congestion_service.calculate_average_congestion(zone, max_capacity)

                    col_v, col_a, col_c = st.columns(3)
                    col_v.metric("Total Vehicles Entered", vehicle_count)
                    col_a.metric("Total Accidents Reported", accident_count)
                    col_c.metric("Average Congestion %", f"{avg_cong.get('average_congestion', 0):.2f}%")

                    st.markdown("---")
                    st.write("#### Detailed Data")
                    st.markdown("*Vehicles in Report Period*")
                    st.dataframe(vehicles)
                    st.markdown("*Accidents in Report Period*")
                    st.dataframe(accidents)

            except Exception as e:
                st.error(f"❌ Error generating report: {e}")

    # ---------------------------------------------------------
    # TAB 6: ADMIN
    # ---------------------------------------------------------
    with tabs[5]:
        st.markdown("### 🔒 Admin Panel")
        st.warning("⚠ Access to all raw data. Please use caution.")

        st.subheader("Secure Access")
        admin_pass = st.text_input("Enter Admin Password", type="password", key="admin_pass")
        
        if st.button("🔑 Login", use_container_width=True, key="btn_admin_login"):
            if admin_pass == "admin123":
                st.success("✅ Admin Login Successful!")
                st.markdown("## All Registered Data")

                # NOTE: Accessing DAO directly, assuming 'dao' attribute exists
                st.write("### 🚗 Vehicles Data")
                st.dataframe(vehicle_service.dao.get_all_vehicles())

                st.write("### 💥 Accidents Data")
                st.dataframe(accident_service.dao.get_all_accidents())

                st.write("### 🗺 Zones Data")
                st.dataframe(zone_service.get_all_zones())

            else:
                st.error("❌ Incorrect Password")


# =========================================================
# FUNCTION FOR THE DASHBOARD LANDING PAGE
# =========================================================
def show_dashboard():
    st.markdown("""
        <style>
        .main-title {
            color: #2c3e50; /* Darker blue-gray for main titles */
            font-size: 3.2em;
            font-weight: 700;
            margin-bottom: 10px;
            letter-spacing: -0.03em;
        }
        .tagline {
            color: #34495e; /* Slightly lighter for tagline */
            font-size: 1.5em;
            margin-top: 5px;
            margin-bottom: 40px;
            font-weight: 400;
        }
        .feature-card {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
            margin: 10px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            text-align: left;
            height: 100%; /* Ensure cards are same height */
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            border-left: 5px solid; /* Dynamic border color */
        }
        .feature-card h4 {
            color: #2980b9; /* A nice blue for feature titles */
            font-weight: 600;
            margin-top: 0;
            margin-bottom: 10px;
            font-size: 1.3em;
        }
        .feature-card p {
            color: #7f8c8d; /* Gray for description */
            font-size: 0.95em;
            line-height: 1.5;
        }
        .stButton button {
            background-color: #3498db; /* Blue for action button */
            color: white;
            padding: 12px 30px;
            border-radius: 8px;
            border: none;
            font-size: 1.2em;
            font-weight: 600;
            transition: background-color 0.2s;
        }
        .stButton button:hover {
            background-color: #2980b9; /* Darker blue on hover */
        }
        /* Specific border colors for feature cards */
        .card-vehicle { border-color: #3498db; } /* Vehicle Blue */
        .card-accident { border-color: #e74c3c; } /* Accident Red */
        .card-zone { border-color: #f39c12; }    /* Zone Orange */
        .card-congestion { border-color: #2ecc71; } /* Congestion Green */
        .card-report { border-color: #9b59b6; }  /* Report Purple */
        .card-admin { border-color: #34495e; }   /* Admin Dark Gray */
        </style>
        """, unsafe_allow_html=True)

    # Central Header (Stylized Banner)
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">🏙️ City Traffic Monitoring System</h1>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("### Application Features Overview")
    st.markdown("---")

    # Feature Cards Overview (Replacing the short paragraph with tabs overview)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="feature-card card-vehicle">
                <h4>🚗 Vehicles Tab</h4>
                <p>Track entries, exits, and manage all vehicle registration details by license plate.</p>
            </div>
            """, unsafe_allow_html=True
        )
        st.markdown(
            """
            <div class="feature-card card-congestion">
                <h4>📈 Congestion Tab</h4>
                <p>Calculate and view real-time congestion levels, factored by vehicle count and accidents.</p>
            </div>
            """, unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="feature-card card-accident">
                <h4>💥 Accidents Tab</h4>
                <p>Report new traffic incidents with location and severity. View incident history per zone.</p>
            </div>
            """, unsafe_allow_html=True
        )
        st.markdown(
            """
            <div class="feature-card card-report">
                <h4>🧾 Traffic Report Tab</h4>
                <p>Generate comprehensive monthly reports detailing traffic flow, accidents, and average congestion.</p>
            </div>
            """, unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="feature-card card-zone">
                <h4>🗺 Zones Tab</h4>
                <p>Define new city zones, manage capacity limits, and view traffic officer assignments.</p>
            </div>
            """, unsafe_allow_html=True
        )
        st.markdown(
            """
            <div class="feature-card card-admin">
                <h4>🔒 Admin Tab</h4>
                <p>Secure area for administrators to view all raw data records across vehicles, accidents, and zones.</p>
            </div>
            """, unsafe_allow_html=True
        )
        
    st.markdown("<br>", unsafe_allow_html=True)

    # Launch Button (Centered)
    launch_col1, launch_col2, launch_col3 = st.columns([1, 2, 1])
    with launch_col2:
        if st.button("🚀 Enter Main Traffic Dashboard", use_container_width=True, key="launch_app"):
            st.session_state.page = 'main_app'
            st.rerun() 
            
    st.markdown("---")
    st.markdown('<p style="text-align: center; color: #7f8c8d;">✨ Your unified source for city traffic data.</p>', unsafe_allow_html=True)


# =========================================================
# MAIN APP EXECUTION FLOW
# =========================================================
if st.session_state.page == 'dashboard':
    show_dashboard()
elif st.session_state.page == 'main_app':
    # Button to go back to the dashboard, placed in the sidebar for easy access
    with st.sidebar:
        st.header("Navigation")
        if st.button("🏠 Go to Dashboard", key="back_to_dashboard"):
            st.session_state.page = 'dashboard'
            st.rerun()
            
    show_main_app()