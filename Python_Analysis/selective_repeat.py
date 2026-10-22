
n = int(input("Enter number of packets: "))
window = int(input("Enter window size: "))
lost = int(input("Enter packet number to simulate loss (0 for none): "))

if n <= 0 or window <= 0 or lost < 0 or lost > n:
    print("Invalid input.")
    exit()

print("\n--- Selective Repeat ARQ ---")

start = 1

while start <= n:
    end = min(start + window - 1, n)
    packets = list(range(start, end + 1))

    print("\nSending packets:", packets)

    if lost in packets:
        print("Packet", lost, "lost!")
        acknowledged = [p for p in packets if p != lost]
        print("Acknowledged packets:", acknowledged)
        print("Retransmitting only packet:", lost)
        print("Acknowledgement received for packet", lost)
        lost = 0
    else:
        print("Acknowledged packets:", packets)

    start = end + 1

print("\nTransmission completed.")
