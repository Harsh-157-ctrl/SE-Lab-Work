def parse_collection(text):
    import math

    if not isinstance(text, str):
        return ("", 0.0)

    parts = text.split(":")
    if len(parts) != 2:
        return ("", 0.0)

    material, kg = parts
    material = material.strip()

    if not material:
        return ("", 0.0)

    try:
        weight = float(kg)
    except (ValueError, OverflowError):
        return ("", 0.0)

    if not math.isfinite(weight) or weight < 0:
        return ("", 0.0)

    return (material.title(), weight)

def weight_average(weights_csv):
    if not isinstance(weights_csv, str):
        return 0

    if not weights_csv.strip():
        return 0

    values = []

    for item in weights_csv.split(","):
        item = item.strip()

        if not item:
            return 0

        try:
            weight = int(item)
        except (ValueError, OverflowError):
            return 0

        if weight < 0:
            return 0

        values.append(weight)

    return sum(values) // len(values)

def net_points(text):
    import math

    if not isinstance(text, str):
        return 0.0

    parts = text.split("|")
    if len(parts) != 2:
        return 0.0

    points_text, penalty_text = parts

    try:
        points = float(points_text)
        penalty = float(penalty_text)
    except (ValueError, OverflowError):
        return 0.0

    if not math.isfinite(points) or not math.isfinite(penalty):
        return 0.0

    if points < 0 or penalty < 0:
        return 0.0

    total = points * 2 - penalty

    if not math.isfinite(total):
        return 0.0

    return max(total, 0.0)

def main():
    print("==== Running parse_collection ====")
    user_input = input("Enter material:weight in kg (e.g. paper:12): ")
    result = parse_collection(user_input)
    print("Material and Weight:", result)

    print("\n==== Running weight_average ====")
    user_input = input("Enter weights in kg as CSV (e.g. 5,12,20): ")
    result = weight_average(user_input)
    print("Average Weight:", result)

    print("\n==== Running net_points ====")
    user_input = input("Enter points|penalty (e.g. 80|10): ")
    result = net_points(user_input)
    print("Net Points:", result)

if __name__ == "__main__":
    main()
