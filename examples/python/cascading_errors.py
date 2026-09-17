# Cascading Errors Sample
def calculate_metrics():
    data = [10, 20, 30]
    # Root Cause: Index 5 out of bounds
    val = data[5]
    result = val * 2
    return result

if __name__ == "__main__":
    calculate_metrics()
