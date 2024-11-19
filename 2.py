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
    sign_and_exponent = (sign_bit << 15) | (exponent & 0x7FFF)
    high_bits = (sign_and_exponent << 16) | (integer_bit << 15) | (fraction >> 48)
    low_bits = fraction & 0xFFFFFFFFFFFF  # Lower 48 bits of mantissa

    # Step 5: Convert to bytes in correct big-endian order
    high_bytes = high_bits.to_bytes(4, 'big')  # 4 старших байта
    low_bytes = low_bits.to_bytes(6, 'big')   # 6 младших байтов

    # Step 6: Combine and format output
    hex_output = ' '.join(f'{b:02X}' for b in high_bytes + low_bytes)
    return hex_output


def float_to_64bit_double_precision(num):
    # Use struct to pack the float into 64 bits (IEEE 754 double precision)
    packed = struct.pack('>d', num)
    return ' '.join(f'{b:02X}' for b in packed)

def float_to_32bit_single_precision(num):
    # Use struct to pack the float into 32 bits (IEEE 754 single precision)
    packed = struct.pack('>f', num)
    return ' '.join(f'{b:02X}' for b in packed)

def extended_precision_to_float(hex_string):
    hex_bytes = bytes.fromhex(hex_string.replace(" ", ""))
    if len(hex_bytes) != 10:
        raise ValueError("The input must be exactly 10 bytes (80 bits) in hex format.")
    sign_bit = (hex_bytes[0] & 0x80) >> 7
    exponent = ((hex_bytes[0] & 0x7F) << 8) | hex_bytes[1]
    integer_bit = (hex_bytes[2] & 0x80) >> 7
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

    exponent -= 16383
    if exponent == -16383 and mantissa == 0:
        # Handle special case: Zero
        return 0.0 if sign_bit == 0 else -0.0
    else:
        mantissa_value = 1.0 + mantissa / (1 << 63)
        result = mantissa_value * (2 ** exponent)
        return -result if sign_bit == 1 else result
# Example usage
number = float(input("Enter a number: "))
print("80-bit Extended Precision:", float_to_80bit_extended_precision(number))
print("64-bit Double Precision:", float_to_64bit_double_precision(number))
print("32-bit Single Precision:", float_to_32bit_single_precision(number))

# Example for converting extended precision back to float
#hex_input = input("Enter a 80-bit hex representation (e.g., '40 01 80 00 00 00 00 00 00 00'): ")
#print("Converted to float:", extended_precision_to_float(hex_input))
