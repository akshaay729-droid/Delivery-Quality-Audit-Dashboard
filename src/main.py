from data_loader import load_data
from quality_audit import audit_addresses
from sla_audit import audit_delivery_sla
from root_cause import root_cause_analysis
from geocode_validation import validate_geocodes
from report_generator import generate_dashboard
from driver_analysis import analyze_driver_performance
from route_analysis import analyze_routes


def main():

    df = load_data()

    if df is not None:
        audit_addresses(df)
        validate_geocodes(df)
        audit_delivery_sla(df)
        issue_counts = root_cause_analysis(df)
        analyze_driver_performance(df)
        analyze_routes(df)
        generate_dashboard(issue_counts)

if __name__ == "__main__":
    main()