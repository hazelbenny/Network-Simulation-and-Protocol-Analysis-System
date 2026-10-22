
n = int(input("Enter number of packets: "))
window = int(input("Enter window size: "))
lost = int(input("Enter packet number to simulate loss (0 for none): "))

if n <= 0 or window <= 0 or lost < 0 or lost > n:
    print("Invalid input.")
    exit()

print("\n--- Go-Back-N ARQ ---")

start = 1

while start <= n:
    end = min(start + window - 1, n)
    print("\nSending packets:", list(range(start, end + 1)))

    if start <= lost <= end:
        print("Packet", lost, "lost!")
        print("Receiver discards later packets in the window.")
        print("Timeout occurred.")
        print("Retransmitting:", list(range(lost, end + 1)))
        print("All retransmitted packets acknowledged.")
    else:
        print("All packets acknowledged.")

    start = end + 1

print("\nTransmission completed.")
