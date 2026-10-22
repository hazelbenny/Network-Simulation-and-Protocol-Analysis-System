
import matplotlib.pyplot as plt

# Results collected from Packet Tracer experiments
# Format: shutdown time, replies resumed, sent, received

ospf = [
    (7.72, 14.54, 11, 9),
    (9.08, 15.77, 24, 23),
    (8.75, 20.48, 26, 24)
]

rip = [
    (9.85, 18.23, 23, 19),
    (6.47, 17.39, 22, 7),
    (8.25, 16.50, 22, 19)
]


# Calculate recovery time and recorded packet loss
def analyze(trials):
    recovery = []
    sent_total = 0
    received_total = 0

    for shutdown, resumed, sent, received in trials:
        recovery.append(resumed - shutdown)
        sent_total += sent
        received_total += received

    lost_total = sent_total - received_total
    loss_percent = lost_total / sent_total * 100

    return recovery, sent_total, received_total, lost_total, loss_percent


o_recovery, o_sent, o_received, o_lost, o_loss = analyze(ospf)
r_recovery, r_sent, r_received, r_lost, r_loss = analyze(rip)


# Display individual trial results
print("\nNETWORK PROTOCOL ANALYSIS")
print("=" * 70)

print("\nINDIVIDUAL TRIAL RESULTS")

print(f"\n{'Protocol':<10}{'Trial':<8}{'Recovery (s)':<16}"
      f"{'Sent':<8}{'Received':<12}{'Lost':<8}")

for name, trials in [("OSPF", ospf), ("RIP v2", rip)]:
    recovery, _, _, _, _ = analyze(trials)

    for i, trial in enumerate(trials):
        sent = trial[2]
        received = trial[3]
        lost = sent - received

        print(f"{name:<10}{i + 1:<8}{recovery[i]:<16.2f}"
              f"{sent:<8}{received:<12}{lost:<8}")


# Display summary
print("\nSUMMARY")
print("-" * 70)
print(f"{'Measurement':<32}{'OSPF':<16}{'RIP v2':<16}")
print("-" * 70)

print(f"{'Average recovery interval (s)':<32}"
      f"{sum(o_recovery)/3:<16.2f}{sum(r_recovery)/3:<16.2f}")

print(f"{'Total ping requests':<32}"
      f"{o_sent:<16}{r_sent:<16}")

print(f"{'Replies received':<32}"
      f"{o_received:<16}{r_received:<16}")

print(f"{'Recorded lost requests':<32}"
      f"{o_lost:<16}{r_lost:<16}")

print(f"{'Recorded loss (%)':<32}"
      f"{o_loss:<16.2f}{r_loss:<16.2f}")


# Explain the results
print("\nOBSERVATIONS")
print("-" * 70)
print("1. Both protocols successfully used an alternate route.")
print("2. OSPF average observed recovery interval:",
      f"{sum(o_recovery)/3:.2f} seconds.")
print("3. RIP v2 average observed recovery interval:",
      f"{sum(r_recovery)/3:.2f} seconds.")
print("4. Recorded ping loss was higher in the RIP v2 trials.")
print("5. Only three trials were performed per protocol.")
print("6. Results do not prove universal protocol superiority.")

print("\nADDITIONAL NETWORK CONSIDERATIONS")
print("-" * 70)
print("Payload: HTTP access demonstrated application-level data delivery.")
print("Failure: A router link was disabled to simulate network failure.")
print("Timeout: Failed ping replies were observed during recovery.")
print("External access: Cross-LAN access to the Research server was tested.")
print("Internet access and full operating-system crashes were not tested.")

print("\nLIMITATIONS")
print("-" * 70)
print("Ping totals include the recorded trial, not just the outage period.")
print("Packet loss below is calculated from all recorded requests.")
print("Recovery timings depend on the measurement method and simulator.")
print("Payload size and throughput were not quantitatively measured.")
print("The Python program analyzes manually entered data.")
print("It does not automatically collect data from Packet Tracer.")


# Chart 1: Average recovery interval
avg_recovery = [
    sum(o_recovery) / len(o_recovery),
    sum(r_recovery) / len(r_recovery)
]

plt.figure(figsize=(7, 5))
bars = plt.bar(["OSPF", "RIP v2"], avg_recovery)
plt.ylabel("Average observed recovery (seconds)")
plt.title("Average Recovery Interval After Link Failure")

for bar, value in zip(bars, avg_recovery):
    plt.text(bar.get_x() + bar.get_width() / 2,
             bar.get_height(),
             f"{value:.2f} s",
             ha="center", va="bottom")

plt.tight_layout()
plt.savefig("protocol_comparison.png", dpi=300)
plt.close()


# Chart 2: Recorded packet loss
loss_values = [o_loss, r_loss]

plt.figure(figsize=(7, 5))
bars = plt.bar(["OSPF", "RIP v2"], loss_values)
plt.ylabel("Recorded ping loss (%)")
plt.title("Recorded Ping Loss Across Three Trials")
plt.ylim(0, max(loss_values) * 1.2)

for bar, value in zip(bars, loss_values):
    plt.text(bar.get_x() + bar.get_width() / 2,
             bar.get_height(),
             f"{value:.2f}%",
             ha="center", va="bottom")

plt.tight_layout()
plt.savefig("protocol_packet_loss.png", dpi=300)
plt.close()

print("\nCharts saved:")
print("1. protocol_comparison.png")
print("2. protocol_packet_loss.png")
