# Performance Doctor Nested Loops Demo
def process_matrix(list_a, list_b, list_c):
    # Performance Issue: O(N^3) time complexity
    for a in list_a:
        for b in list_b:
            for c in list_c:
                print(a, b, c)
