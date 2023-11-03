import sys
import math

def row_from_bottom(B, row):
    return B[-row]

def create_array(n, m):
    return [[0 for _ in range(m)] for _ in range(n)]

def binary_to_decimal(A):
    decimal = 0
    n = len(A)

    for i in range(n):
        decimal += A[i] * 2**(n-i-1)

    return decimal

def or_arrays(A, B):
    n = len(A)
    m = len(A[0])
    C = create_array(n, m)

    for i in range(n):
        for j in range(m):
            C[i][j] = A[i][j] or B[i][j]

    return C

def compare_arrays(A, B):
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        return False

    for i in range(len(A)):
        for j in range(len(B)):
            if A[i][j] != B[i][j]:
                print(f"({i},{j}): {A[i][j]} vs {B[i][j]}")
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

def split_array_by_column(A, min_col, max_col):
    num_row = len(A)
    C = create_array(num_row, max_col-min_col)

    for i in range(num_row):
        C[i] = A[i][min_col:max_col]

    return C

def copy_array(A):
    copy = create_array(len(A), len(A[0]))

    for i in range(len(A)):
        for j in range(len(A[0])):
            copy[i][j] = A[i][j]

    return copy

def four_russians(init_A, init_B):
    A = copy_array(init_A)
    B = copy_array(init_B)

    n_A, m_A = len(A), len(A[0])
    n_B, m_B = len(B), len(B[0])

    # Check bounds
    if not (n_A == m_A == n_B == m_B):
        return None

    n = n_A
    m = math.floor(math.log(n, 2))

    # Pad zeros
    for _ in range((n + 1) % m):
        B.append([0 for _ in range(n)])
        for j in range(n):
            A[j].append(0)

    # Main logic
    C = create_array(n, n)

    for i in range(1, math.ceil(n/m) + 1):
        arr_i = i-1
        A_i = split_array_by_column(A, arr_i*m, arr_i*m+m)
        B_i = B[arr_i*m:arr_i*m + m][:]

        RS = create_array(2**m, n)
        bp = 1
        k = 0

        for j in range(1, 2**m):
            B_bottom = row_from_bottom(B_i, k+1)
            RS[j] = or_arrays([RS[j-2**k]], [B_bottom])[0]

            if bp == 1:
                bp = j + 1
                k = k + 1
            else:
                bp = bp - 1

        C_i = create_array(n, n)

        for j in range(n):
            C_i[j] = RS[binary_to_decimal(A_i[j])]

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

    if len(arg) == 3:
        graph = read_file_into_matrix(arg[1], ' ')
        expected = read_file_into_matrix(arg[2], ' ')
        A = get_adj_matrix(graph)
        A_transitive = get_adj_matrix(expected)

        n = len(A)

        A_n = four_russians(A, A)

        for i in range(n-1):
           A_n = four_russians(A_n, A)

        test_arrays(A_n, A_transitive)
        exit(1)

    if len(arg) == 4:
        A = read_file_into_matrix(arg[1], ',')
        B = read_file_into_matrix(arg[2], ',')
        C = read_file_into_matrix(arg[3], ',')

        test_arrays(four_russians(A, B), C)
        exit(1)

    sys.exit('Improper arguments')


"""
TODO:
- Setup arg and file reading
- Code up algorithm
- Set up testing
"""