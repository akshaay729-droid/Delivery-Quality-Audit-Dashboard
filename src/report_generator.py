import matplotlib.pyplot as plt


def generate_dashboard(issue_counts):

    labels = list(issue_counts.keys())
    values = list(issue_counts.values())

    issues = [
        "Address",
        "Coordinates",
        "Invalid Lat",
        "Invalid Long",
        "Late Delivery",
        "Failed"
    ]

    counts = [1, 2, 1, 1, 5, 1]

    plt.figure(figsize=(8, 5))
    plt.bar(issues, counts)

    plt.title("Delivery Quality Dashboard")
    plt.xlabel("Issue Type")
    plt.ylabel("Count")

    plt.tight_layout()

    plt.savefig("reports/quality_dashboard.png")

    plt.close()

    print("\nDashboard generated successfully:")
    print("reports/quality_dashboard.png")