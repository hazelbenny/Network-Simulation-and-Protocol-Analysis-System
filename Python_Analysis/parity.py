
data = input("Enter binary data: ")

if not data or any(bit not in "01" for bit in data):
    print("Invalid input. Enter only 0s and 1s.")
    exit()

bits = [int(bit) for bit in data]
cols = 4

# Pad with zeros to complete the last row
while len(bits) % cols != 0:
    bits.append(0)

rows = [bits[i:i + cols] for i in range(0, len(bits), cols)]

print("\n--- Simple Parity ---")
ones = data.count("1")
parity = ones % 2

print("Data:", data)
print("Even parity bit:", parity)
print("Transmitted data:", data + str(parity))

print("\n--- 2D Parity ---")

# Calculate parity for each row
row_parity = [sum(row) % 2 for row in rows]

# Calculate parity for each column
col_parity = []
for j in range(cols):
    total = 0
    for row in rows:
        total += row[j]
    col_parity.append(total % 2)

# Bottom-right corner bit
corner = sum(row_parity) % 2

# Display complete block
for i in range(len(rows)):
    print(*(rows[i] + [row_parity[i]]))

print(*(col_parity + [corner]))

print("\n2D parity block generated successfully.")
