import sys
import math

def row_from_bottom(B, row):
    return B[-row]

def create_array(n, m):
    return [[0 for _ in range(m)] for _ in range(n)]

def or_arrays(A, B):
    return [A[i] | B[i] for i in range(len(A))]

def compare_arrays(A, B):
    if len(A) != len(B):
        return False

    for i in range(len(A)):
        if A[i] != B[i]:
            print(f"({i}): {A[i]} vs {B[i]}")
            return False

    return True

def get_adj_matrix(edges):
    max_node = -1

    for u, v in edges:
        max_node = max(max_node, u, v)

    n = max_node + 1
    adj_matrix = create_array(n, n)

    for u, v in edges:
        adj_matrix[u][v] = 1
        adj_matrix[v][u] = 1

    for i in range(n):
        adj_matrix[i][i] = 1

    return adj_matrix

def print_array_dim(A):
    print(f"{len(A)} x {len(A[0])}")

"""
Paritions a matrix by column based on the bits that each row is set to
For example, if a row has value 6, then it's binary value is 101. If we have
min_col=0 and max_col=1, we should return 1.
"""
def split_bits_by_column(A, min_col, max_col, n):
    C = []
    for row in A:
        remove_left = row & (2**(n - min_col)-1)
        remove_right = (remove_left >> (n - max_col))
        C.append(remove_right)

    return C

"""
Read in a 2D array with each row set to a list
containing 0s and 1s, and convert this row into a number
"""
def array_to_bits(A):
    bits = []

    for row in A:
        n = len(row)
        total = 0

        for i in range(n):
            total += row[i] * 2**(n-1-i)

        bits.append(total)

    return bits

def four_russians(init_A, init_B):
    A = init_A.copy()
    B = init_B.copy()

    n_A = len(A)
    n_B = len(B)

    # Check bounds
    if not (n_A == n_B):
        return None

    n = n_A
    m = math.floor(math.log(n, 2))

    n_padded = n + (n + 1) % m

    # Pad zeros
    for _ in range((n + 1) % m):
        B.append(0)
        for j in range(n):
            A[j] = A[j] << 1

    # Main logic
    C = [0 for _ in range(n)]

    for i in range(1, math.ceil(n/m) + 1):
        arr_i = i-1
        A_i = split_bits_by_column(A, arr_i*m, arr_i*m+m, n_padded)
        B_i = B[arr_i*m:arr_i*m + m]

        # Generate row sums
        RS = [0 for _ in range(2**m)]
        bp = 1
        k = 0

        for j in range(1, 2**m):
            B_bottom = row_from_bottom(B_i, k+1)
            RS[j] = RS[j-2**k] | B_bottom

            if bp == 1:
                bp = j + 1
                k = k + 1
            else:
                bp = bp - 1

        C_i = create_array(n, n)

        # Use memoized row sums to calculate each row in C_i
        for j in range(n):
            C_i[j] = RS[A_i[j]]

        C = or_arrays(C, C_i)
    return C

def read_file_into_matrix(filename, delimiter):
    try:
        file = open(filename, "r")
        matrix = []

        for row in file:
            vals = row.split(delimiter)
            matrix.append([int(val) for val in vals])
        return matrix
    except:
        sys.exit(f"{filename} does not exist")

def test_arrays(received, expected):
    if compare_arrays(received, expected):
        print("Four Russians boolean matrix is correct")
    else:
        print("Four Russians boolean matrix is incorrect")

    exit(1)

if __name__ == '__main__':
    arg = sys.argv

    # Handle transitive closure of graphs
    if len(arg) == 3:
        graph = read_file_into_matrix(arg[1], ' ')
        expected = read_file_into_matrix(arg[2], ' ')
        A = array_to_bits(get_adj_matrix(graph))
        A_transitive = array_to_bits(get_adj_matrix(expected))

        n = len(A)

        A_n = four_russians(A, A)

        for i in range(n-1):
           A_n = four_russians(A_n, A)

        test_arrays(A_n, A_transitive)
        exit(1)

    # Handle matrix multiplication
    if len(arg) == 4:
        A = array_to_bits(read_file_into_matrix(arg[1], ','))
        B = array_to_bits(read_file_into_matrix(arg[2], ','))
        C = array_to_bits(read_file_into_matrix(arg[3], ','))

        test_arrays(four_russians(A, B), C)
        exit(1)

    sys.exit('Improper arguments')