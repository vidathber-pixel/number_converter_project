"""
Advanced Number System Converter & Math Engine
Author: Portfolio Project
Description: Converts numbers between Binary, Octal, Decimal, and Hexadecimal.
Features: Fractional values, positional power expansion, successive division/multiplication,
          and modular Object-Oriented design.
"""

import sys

HEX_DIGITS = "0123456789ABCDEF"

class ConversionError(Exception):
    """Custom exception class for invalid base conversion inputs."""
    pass


class NumberConverter:
    BASES = {
        '1': ('Binary', 2),
        '2': ('Octal', 8),
        '3': ('Decimal', 10),
        '4': ('Hexadecimal', 16)
    }

    @staticmethod
    def validate_and_clean(val_str: str, base: int) -> tuple[str, bool]:
        """Cleans input string, removes prefixes, and checks valid characters for base."""
        cleaned = val_str.strip().upper()
        
        # Strip standard programming prefixes
        prefixes = {2: '0B', 8: '0O', 16: '0X'}
        if base in prefixes and cleaned.startswith(prefixes[base]):
            cleaned = cleaned[2:]
            
        if not cleaned:
            raise ConversionError("Input string cannot be empty.")
            
        is_negative = cleaned.startswith('-')
        if is_negative:
            cleaned = cleaned[1:]

        if cleaned.count('.') > 1:
            raise ConversionError("Invalid input: Multiple decimal points detected.")

        valid_chars = set(HEX_DIGITS[:base])
        valid_chars.add('.')

        for char in cleaned:
            if char not in valid_chars:
                raise ConversionError(
                    f"Invalid character '{char}' for Base-{base}. Allowed: {HEX_DIGITS[:base]}"
                )

        return cleaned, is_negative

    @classmethod
    def to_decimal(cls, num_str: str, base: int) -> tuple[float, list[str]]:
        """Converts any base representation (integer + fraction) to Base-10 Decimal."""
        steps = []
        parts = num_str.split('.')
        int_part = parts[0]
        frac_part = parts[1] if len(parts) > 1 else ""

        decimal_val = 0.0

        # Integer part expansion (Positional Powers)
        int_steps = []
        for i, char in enumerate(reversed(int_part)):
            digit = HEX_DIGITS.index(char)
            term = digit * (base ** i)
            decimal_val += term
            int_steps.append(f"({digit} × {base}^{i})")
            
        if int_steps:
            steps.append(f"Integer Expansion: {' + '.join(reversed(int_steps))} = {int(decimal_val)}")

        # Fractional part expansion (Negative Powers)
        if frac_part:
            frac_steps = []
            frac_val = 0.0
            for i, char in enumerate(frac_part, start=1):
                digit = HEX_DIGITS.index(char)
                term = digit * (base ** -i)
                frac_val += term
                frac_steps.append(f"({digit} × {base}^-{i})")
            decimal_val += frac_val
            steps.append(f"Fractional Expansion: {' + '.join(frac_steps)} = {frac_val}")

        return decimal_val, steps

    @classmethod
    def from_decimal(cls, dec_val: float, target_base: int, precision: int = 6) -> tuple[str, list[str]]:
        """Converts Base-10 Decimal to target base using division and multiplication methods."""
        steps = []
        int_part = int(dec_val)
        frac_part = dec_val - int_part

        # Integer part conversion (Successive Division)
        if int_part == 0:
            converted_int = "0"
            steps.append(f"Integer part is 0 -> Result: '0'")
        else:
            remainder_list = []
            temp = int_part
            steps.append(f"Integer Division (Divide by {target_base}):")
            while temp > 0:
                rem = temp % target_base
                quotient = temp // target_base
                rem_char = HEX_DIGITS[rem]
                steps.append(f"  {temp} ÷ {target_base} = {quotient}  (Remainder: {rem} -> '{rem_char}')")
                remainder_list.append(rem_char)
                temp = quotient
            converted_int = "".join(reversed(remainder_list))

        # Fractional part conversion (Successive Multiplication)
        converted_frac = ""
        if frac_part > 0:
            steps.append(f"Fractional Multiplication (Multiply by {target_base}):")
            temp_frac = frac_part
            count = 0
            frac_digits = []
            while temp_frac > 0 and count < precision:
                prod = temp_frac * target_base
                digit = int(prod)
                digit_char = HEX_DIGITS[digit]
                steps.append(f"  {temp_frac:.6f} × {target_base} = {prod:.6f} -> Digit: '{digit_char}'")
                frac_digits.append(digit_char)
                temp_frac = prod - digit
                count += 1
            converted_frac = "." + "".join(frac_digits)

        return converted_int + converted_frac, steps

    @classmethod
    def convert(cls, raw_str: str, source_base_key: str) -> dict:
        """Orchestrates conversion from source base to all 4 standard bases."""
        name, source_base = cls.BASES[source_base_key]
        cleaned, is_neg = cls.validate_and_clean(raw_str, source_base)
        dec_val, to_dec_steps = cls.to_decimal(cleaned, source_base)

        results = {}
        all_steps = {
            'to_decimal': to_dec_steps,
            'from_decimal': {}
        }

        for key, (b_name, b_val) in cls.BASES.items():
            if b_val == 10:
                res_str = f"{dec_val:.6g}"
            else:
                res_str, from_dec_steps = cls.from_decimal(dec_val, b_val)
                all_steps['from_decimal'][b_name] = from_dec_steps

            prefix = "-" if is_neg else ""
            results[b_name] = f"{prefix}{res_str}"

        return {'results': results, 'steps': all_steps}


def display_ui_header():
    print("┌" + "─" * 58 + "┐")
    print("│         NUMBER SYSTEM CONVERTER & ENGINE                 │")
    print("└" + "─" * 58 + "┘")


def display_output(output: dict, show_breakdown: bool):
    print("\n" + "═" * 60)
    print("                      CONVERSION RESULTS                    ")
    print("═" * 60)
    for system, value in output['results'].items():
        print(f"  {system:<18} : {value}")
    print("═" * 60)

    if show_breakdown:
        print("\n" + "─" * 60)
        print("                  MATHEMATICAL BREAKDOWN                    ")
        print("─" * 60)
        print("\n[Phase 1: Conversion to Decimal (Base 10)]")
        for step in output['steps']['to_decimal']:
            print(f"  • {step}")

        print("\n[Phase 2: Conversion from Decimal to Target Bases]")
        for base_name, steps in output['steps']['from_decimal'].items():
            print(f"\n  ► Target: {base_name}")
            for step in steps:
                print(f"    {step}")
        print("─" * 60 + "\n")


def main():
    converter = NumberConverter()
    
    while True:
        display_ui_header()
        print("Select Source Base:")
        print("  1. Binary (Base 2)")
        print("  2. Octal (Base 8)")
        print("  3. Decimal (Base 10)")
        print("  4. Hexadecimal (Base 16)")
        print("  5. Exit")

        choice = input("\nEnter choice (1-5): ").strip()

        if choice == '5':
            print("\nExiting application.")
            sys.exit()

        if choice not in converter.BASES:
            print("\n[!] Invalid choice. Enter a number between 1 and 5.\n")
            continue

        base_name, _ = converter.BASES[choice]
        user_input = input(f"Enter {base_name} value (e.g., integers or fractions like '1011.101'): ")

        show_steps = input("Show mathematical steps? (y/n) [y]: ").strip().lower() != 'n'

        try:
            output = converter.convert(user_input, choice)
            display_output(output, show_steps)
        except ConversionError as err:
            print(f"\n[Error] {err}\n")
        except Exception as e:
            print(f"\n[Unexpected Error] {e}\n")


if __name__ == "__main__":
    main()