import subprocess



if __name__ == '__main__':
    # TEST CASE 1: AB = C
    result = subprocess.run(['python3', 'main.py', 'tests/array_1.txt', 'tests/array_2.txt', 'tests/array_expected.txt'], stdout=subprocess.PIPE)
    out = result.stdout.decode('utf-8')

    print("Passed AB=C" if out == "Four Russians boolean matrix is correct\n" else "Failed AB=C")
    # TEST CASE 2: Transitive Closure of Graph
    result = subprocess.run(['python3', 'main.py', 'tests/graph_1.txt', 'tests/graph_expected.txt'],
                            stdout=subprocess.PIPE)
    out = result.stdout.decode('utf-8')

    print("Passed Transitive Closure of Graph" if out == "Four Russians boolean matrix is correct\n" else "Failed Transitive Closure of Graph")