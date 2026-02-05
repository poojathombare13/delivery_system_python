import json
import math
import random
import csv

# -------------------------------
# Function to calculate distance
# -------------------------------
def euclidean_distance(p1, p2):        
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# -------------------------------
# Main Delivery System Function
# -------------------------------
def run_delivery_system(input_file):

    # Read JSON input file
    with open(input_file, "r") as f:
        data = json.load(f)

    # Extract data sections
    warehouses = data["warehouses"]  
    agents = data["agents"]
    packages = data["packages"]

    # Store total packages count (for validation)
    total_packages = len(packages)

    # Create report structure
    report = {}

    for agent in agents:
        report[agent] = {
            "packages_delivered": 0,
            "total_distance": 0
        }

    # -------------------------------
    # Process each package
    # -------------------------------
    for package in packages:

        warehouse_id = package["warehouse"]
        destination = package["destination"]
        warehouse_location = warehouses[warehouse_id]

        # Find nearest agent
        nearest_agent = None
        min_dist = float("inf")

        for agent_id, agent_loc in agents.items():
            dist = euclidean_distance(agent_loc, warehouse_location)

            if dist < min_dist:
                min_dist = dist
                nearest_agent = agent_id

        # Calculate delivery distance
        agent_location = agents[nearest_agent]

        dist_agent_to_wh = euclidean_distance(agent_location, warehouse_location)
        dist_wh_to_dest = euclidean_distance(warehouse_location, destination)

        total_dist = dist_agent_to_wh + dist_wh_to_dest

        # BONUS: Add random delivery delay
        delay = random.uniform(1, 5)
        total_dist += delay

        # Update agent report
        report[nearest_agent]["packages_delivered"] += 1
        report[nearest_agent]["total_distance"] += total_dist

    # -------------------------------
    # Validate total delivered packages
    # -------------------------------
    delivered_total = sum(agent["packages_delivered"] for agent in report.values())

    if delivered_total != total_packages:
        print("WARNING: Package count mismatch!")
    else:
        print("Package validation successful")

    # -------------------------------
    # Efficiency and Best Agent
    # -------------------------------
    best_agent = None
    best_efficiency = float("inf")

    for agent in report:

        delivered = report[agent]["packages_delivered"]
        total_dist = report[agent]["total_distance"]

        if delivered > 0:
            efficiency = total_dist / delivered
        else:
            efficiency = 0

        report[agent]["efficiency"] = round(efficiency, 2)
        report[agent]["total_distance"] = round(total_dist, 2)

        if efficiency < best_efficiency:
            best_efficiency = efficiency
            best_agent = agent

    report["best_agent"] = best_agent

    # -------------------------------
    # Save JSON Report
    # -------------------------------
    with open("report.json", "w") as f:
        json.dump(report, f, indent=4)

    print("Report Generated Successfully")

    # -------------------------------
    # BONUS: Export Best Agent to CSV
    # -------------------------------
    with open("best_agent.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Agent", "Efficiency"])
        writer.writerow([best_agent, report[best_agent]["efficiency"]])

    print("Best agent exported to CSV")

# -------------------------------
# Program Entry Point
# -------------------------------
if __name__ == "__main__":
    run_delivery_system("test_case_10.json")

