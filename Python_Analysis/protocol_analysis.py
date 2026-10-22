
import matplotlib.pyplot as plt

# Results collected from our Packet Tracer experiments
protocols = ["OSPF", "RIP v2"]

ping_before = [1, 1]
ping_after = [1, 1]
alternate_route = [1, 1]
interruption = [0, 0]

# Display the comparison table
print("\nNETWORK PROTOCOL ANALYSIS")
print("-" * 65)
print(f"{'Observation':<35}{'OSPF':<15}{'RIP v2':<15}")
print("-" * 65)

print(f"{'Ping successful before failure':<35}{'Yes':<15}{'Yes':<15}")
print(f"{'Ping successful after link failure':<35}{'Yes':<15}{'Yes':<15}")
print(f"{'Alternate route verified':<35}{'Yes':<15}{'Yes':<15}")
print(f"{'Interruption observed':<35}{'No':<15}{'No':<15}")

print("-" * 65)

print("\nANALYSIS")
print("-" * 45)

print("1. Both protocols maintained connectivity.")
print("2. Both used an alternate route through R2.")
print("3. The observed results were identical in this test.")
print("4. Recovery speed was not measured.")
print("5. More tests are needed to compare performance.")

print("\nPROTOCOL CHARACTERISTICS")
print("-" * 45)
print("OSPF: Link-state routing; uses a cost metric.")
print("RIP v2: Distance-vector routing; uses hop count.")

# Prepare chart data
categories = [
    "Ping before failure",
    "Ping after failure",
    "Alternate route verified"
]

ospf_results = [1, 1, 1]
rip_results = [1, 1, 1]

# Draw a bar chart
x = range(len(categories))
width = 0.35

plt.figure(figsize=(10, 6))
plt.bar([i - width / 2 for i in x], ospf_results,
        width, label="OSPF")
plt.bar([i + width / 2 for i in x], rip_results,
        width, label="RIP v2")

plt.xticks(list(x), categories, rotation=15, ha="right")
plt.yticks([0, 1], ["No", "Yes"])
plt.ylim(0, 1.2)
plt.ylabel("Observed result")
plt.title("OSPF vs RIP v2: Link Failure Experiment")
plt.legend()
plt.tight_layout()

# Save and display the chart
plt.savefig("protocol_comparison.png")
plt.show()
