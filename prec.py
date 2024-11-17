import struct

def float_to_80bit_extended_precision(num):
    # Step 1: Sign bit
    sign_bit = 0 if num >= 0 else 1
    num = abs(num)

    # Step 2: Extract the binary exponent and mantissa
    exponent = 0
    if num != 0.0:
        # Find exponent in base 2 (log2)
        while num < 1.0:
            num *= 2
            exponent -= 1
        while num >= 2.0:
            num /= 2
            exponent += 1
        exponent += 16383  # Offset by the bias for 80-bit precision

    # Step 3: Create the integer bit and mantissa
    integer_bit = 1  # Always 1 for normalized numbers
    fraction = int((num - integer_bit) * (1 << 63))  # Scale fraction to 63 bits

    # Step 4: Construct the 80-bit binary representation
    # Combine sign, exponent, integer bit, and mantissa into 80 bits
    # | sign (1 bit) | exponent (15 bits) | integer bit (1 bit) | mantissa (63 bits) |
    sign_and_exponent = (sign_bit << 15) | (exponent & 0x7FFF)
    high_bits = (sign_and_exponent << 16) | (integer_bit << 15) | (fraction >> 48)
    low_bits = fraction & 0xFFFFFFFFFFFF  # Lower 48 bits of mantissa

    # Step 5: Convert to hex output (in big-endian order)
    high_bytes = struct.pack('>Q', high_bits)[2:]  # High 64 bits, but trim to 6 bytes
    low_bytes = struct.pack('>Q', low_bits)[2:]    # Low 48 bits, 6 bytes total

    # Step 6: Combine and format output
    hex_output = ' '.join(f'{b:02X}' for b in high_bytes + low_bytes)
    return hex_output

# Example usage
number = float(input("Enter a number: "))
print("80-bit Extended Precision:", float_to_80bit_extended_precision(number)[6:])  # Remove the '0x' prefix
def extended_precision_to_float(hex_string):
    # Step 1: Convert the hex string to bytes
    hex_bytes = bytes.fromhex(hex_string.replace(" ", ""))
    if len(hex_bytes) != 10:
        raise ValueError("The input must be exactly 10 bytes (80 bits) in hex format.")

    # Step 2: Parse the sign, exponent, and mantissa
    sign_bit = (hex_bytes[0] & 0x80) >> 7
    exponent = ((hex_bytes[0] & 0x7F) << 8) | hex_bytes[1]
    integer_bit = (hex_bytes[2] & 0x80) >> 7

    # Combine the remaining mantissa bits into a 63-bit integer
    mantissa = (
        ((hex_bytes[2] & 0x7F) << 56)
        | (hex_bytes[3] << 48)
        | (hex_bytes[4] << 40)
        | (hex_bytes[5] << 32)
        | (hex_bytes[6] << 24)
        | (hex_bytes[7] << 16)
        | (hex_bytes[8] << 8)
        | hex_bytes[9]
    )

    # Step 3: Adjust the exponent (subtract the bias of 16383)
    exponent -= 16383

    # Step 4: Reconstruct the floating-point number
    if exponent == -16383 and mantissa == 0:
        # Handle special case: Zero
        return 0.0 if sign_bit == 0 else -0.0
    else:
        # Calculate the mantissa as a floating-point number
        mantissa_value = 1.0 + mantissa / (1 << 63)
        result = mantissa_value * (2 ** exponent)
        return -result if sign_bit == 1 else result

# Example usage
#hex_input = input("Enter a 80-bit hex representation (e.g., '40 01 80 00 00 00 00 00 00 00'): ")
#print("Converted to float:", extended_precision_to_float(hex_input))