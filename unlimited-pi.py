import decimal
import sys

def calculate_pi(n_digits):
    """
    Calculates Pi to the specified number of decimal places using the
    Gauss-Legendre algorithm with the decimal module.
    """
    try:
        n_digits = int(n_digits)
        if n_digits < 0:
            raise ValueError("Number of digits must be non-negative.")
    except ValueError:
         raise ValueError("Invalid input. Please enter an integer number of digits.")

    MAX_DIGITS = 10000
    if n_digits > MAX_DIGITS:
        raise ValueError(f"Calculation limited to {MAX_DIGITS} decimal places for practical reasons.")

    # --- Calculation Setup ---
    # Set the precision for the decimal module.
    # Need n_digits + 1 (for '3.') + a few guard digits for intermediate calculations.
    # Setting it a bit higher ensures accuracy during iterations.
    calculation_precision = n_digits + 5
    decimal.getcontext().prec = calculation_precision

    # --- Gauss-Legendre Algorithm Implementation ---
    # Initialize variables as Decimal objects
    a_n = decimal.Decimal(1)
    b_n = decimal.Decimal(1) / decimal.Decimal(2).sqrt()
    t_n = decimal.Decimal(1) / decimal.Decimal(4)
    p_n = decimal.Decimal(1)

    # Iterate until desired precision is likely reached
    # The algorithm converges quadratically, so it doesn't take many loops
    # for high precision. We check convergence by seeing if a_n and b_n are close.
    while True:
        a_next = (a_n + b_n) / 2
        b_next = (a_n * b_n).sqrt()
        t_next = t_n - p_n * (a_n - a_next)**2
        p_next = 2 * p_n

        # Check if a_n and b_n are close enough (converged for the set precision)
        # Using == works because decimal precision controls the comparison.
        if a_n == a_next or b_n == b_next:
            break

        a_n, b_n, t_n, p_n = a_next, b_next, t_next, p_next

    # Final Pi calculation based on the algorithm
    pi_value = (a_n + b_n)**2 / (4 * t_n)

    # --- Formatting Output ---
    # Quantize the result to exactly n_digits decimal places
    # Create the quantizer string like '1e-10' for 10 digits
    # Use ROUND_DOWN to truncate, matching typical definitions of "Nth digit"
    quantizer = decimal.Decimal('1e-' + str(n_digits))
    return pi_value.quantize(quantizer, rounding=decimal.ROUND_DOWN)

if __name__ == "__main__":
    print("--- Pi to the Nth Digit Calculator ---")

    while True:
        try:
            num_digits_input = input("Enter the number of decimal places for Pi (e.g., 10, 50, max 10,000): ")
            if num_digits_input.lower() in ['q', 'quit', 'exit']:
                print("Exiting.")
                break

            pi_result = calculate_pi(num_digits_input)
            print(f"\nPi to {num_digits_input} decimal places:")
            print(pi_result)
            print("-" * 30) # Separator for next run

        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
        except Exception as e:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)

