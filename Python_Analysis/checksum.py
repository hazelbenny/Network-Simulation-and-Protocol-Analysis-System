
data = input("Enter 8-bit binary words separated by spaces: ").split()

# Check input
if not data or any(len(x) != 8 or any(b not in "01" for b in x) for x in data):
    print("Invalid input. Enter 8-bit binary words.")
    exit()

words = [int(x, 2) for x in data]

# Calculate sender checksum
total = sum(words)

while total > 255:
    total = (total & 255) + (total >> 8)

checksum = (~total) & 255

print("\nChecksum:", format(checksum, "08b"))

# Simulate received data
received = input("Enter received words separated by spaces (press Enter for original): ")

if received.strip() == "":
    received_words = words[:]
else:
    received_words = []

    for x in received.split():
        if len(x) != 8 or any(b not in "01" for b in x):
            print("Invalid received data.")
            exit()
        received_words.append(int(x, 2))

# Receiver checks data + checksum
check = sum(received_words) + checksum

while check > 255:
    check = (check & 255) + (check >> 8)

print("\n--- Receiver ---")

if check == 255:
    print("No error detected")
else:
    print("Error detected")
