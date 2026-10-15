import pathlib
import math

#Reading from the file
def load_system(path: pathlib.Path) -> tuple[list[list[float]], list[float]]:
    A = []
    B = []
    
    with open(path, 'r') as f:
        for line in f:
            if not line.strip(): 
                continue
            
            # Split into left-hand side and right-hand side
            left, right = line.split('=')
            B.append(float(right.strip()))
            
            #split by spaces
            parts = left.split()
            
            # Combine operators (+ / -) with their corresponding variable terms
            terms = []
            current_sign = '+'
            for p in parts:
                if p in ('+', '-'):
                    current_sign = p
                else:
                    # Prepend negative sign if applicable, otherwise keep it positive
                    terms.append(f"-{p}" if current_sign == '-' else p)
                    current_sign = '+' 
            
            # Extract coefficients
            row = []
            for term, var in zip(terms, ['x', 'y', 'z']):
                # Remove the variable letter to leave just the coefficient
                coeff_str = term.replace(var, '')
                
                if coeff_str == '' or coeff_str == '+':
                    row.append(1.0)
                elif coeff_str == '-':
                    row.append(-1.0)
                else:
                    row.append(float(coeff_str))
                    
            A.append(row)
            
    return A, B


#Operations with matrix and vectors
def determinant(matrix: list[list[float]]) -> float:
    # Using the standard 3x3 determinant formula
    a11, a12, a13 = matrix[0]
    a21, a22, a23 = matrix[1]
    a31, a32, a33 = matrix[2]
    
    return float(a11 * (a22 * a33 - a23 * a32) - 
                 a12 * (a21 * a33 - a23 * a31) + 
                 a13 * (a21 * a32 - a22 * a31))

def trace(matrix: list[list[float]]) -> float:
    # Sum of the elements on the main diagonal
    return float(matrix[0][0] + matrix[1][1] + matrix[2][2])

def norm(vector: list[float]) -> float:
    # Euclidean norm
    return math.sqrt(sum(v**2 for v in vector))

def transpose(matrix: list[list[float]]) -> list[list[float]]:
    # Swap rows and columns using a nested list comprehension
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

def multiply(matrix: list[list[float]], vector: list[float]) -> list[float]:
    # Matrix-vector multiplication (dot product of each matrix row with the vector)
    return [sum(r * v for r, v in zip(row, vector)) for row in matrix]


#Solving using Cramer's rule
def solve_cramer(matrix: list[list[float]], vector: list[float]) -> list[float]:
    det_A = determinant(matrix)
    if det_A == 0:
        raise ValueError("Determinant is 0. The system does not have a unique solution.")
        
    def replace_column(mat, col_idx, vec):
        # Create a deep copy of the matrix
        new_mat = [row[:] for row in mat]
        for i in range(len(vec)):
            new_mat[i][col_idx] = vec[i]
        return new_mat
        
    # Replace columns with vector B
    Ax = replace_column(matrix, 0, vector)
    Ay = replace_column(matrix, 1, vector)
    Az = replace_column(matrix, 2, vector)
    
    # Calculate x, y, z
    return [determinant(Ax) / det_A, 
            determinant(Ay) / det_A, 
            determinant(Az) / det_A]


#Solving using Inversion
def minor(matrix: list[list[float]], i: int, j: int) -> list[list[float]]:
    # Create a minor matrix by skipping row i and column j
    return [row[:j] + row[j+1:] for idx, row in enumerate(matrix) if idx != i]

def get_2x2_det(mat: list[list[float]]) -> float:
    # Helper function for the determinant of a 2x2 matrix
    return mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]

def cofactor(matrix: list[list[float]]) -> list[list[float]]:
    cof_matrix = []
    for i in range(3):
        row = []
        for j in range(3):
            # Calculate the minor and apply the sign (-1)^(i+j)
            minor_mat = minor(matrix, i, j)
            row.append(((-1) ** (i + j)) * get_2x2_det(minor_mat))
        cof_matrix.append(row)
    return cof_matrix

def adjoint(matrix: list[list[float]]) -> list[list[float]]:
    # The adjoint is simply the transpose of the cofactor matrix
    return transpose(cofactor(matrix))

def solve(matrix: list[list[float]], vector: list[float]) -> list[float]:
    det_A = determinant(matrix)
    if det_A == 0:
        raise ValueError("Determinant is 0. Matrix is not invertible.")
        
    adj = adjoint(matrix)
    
    # Multiply the adjoint matrix by (1 / det_A) to get the inverted matrix A^(-1)
    inverse_matrix = [[element / det_A for element in row] for row in adj]
    
    # Final step: multiply A^(-1) by B
    return multiply(inverse_matrix, vector)



if __name__ == "__main__":
 
    file_path = pathlib.Path("ecuatie.txt")
    
    print("Reading from file")
    A, B = load_system(file_path)
    print(f"Matricea A: {A}")
    print(f"Vectorul B: {B}\n")
    
    print("Opetarions with matrix and vectors")
    print(f"Determinant(A) = {determinant(A)}")
    print(f"Urma (Trace) A = {trace(A)}")
    print(f"Norma(B) = {norm(B)}")
    print(f"Transpusa(A) = {transpose(A)}")
    print(f"Inmulțire A * B = {multiply(A, B)}\n")
    
    print("Resolve by using Cramer's rule")
    print(f"Soluție [x, y, z] = {solve_cramer(A, B)}\n")
    
    print("Resolve by using A ^(-1)")
    print(f"Soluție [x, y, z] = {solve(A, B)}")