# Constant Term Reconstruction of an constant c in polynomial equation from data encrypted in SSS(Shamirs Secret Sharing) Algorithm

This project demonstrates how to **reconstruct the constant term `c`** from a polynomial encrypted using **Shamir's Secret Sharing (SSS)**.

The polynomial used in this project is of the form:


f(x) = a * x^n + b * x^(n-1) + c


- `n = 10` in the main test case  
- `c` is the secret constant term we want to recover  
- Shares are stored in a JSON file, with values encoded in different bases  

---

## Overview

Shamir's Secret Sharing works by creating a polynomial with the secret as the constant term.  
Each participant receives a **share** `(x_i, y_i)`, where:


y_i = f(x_i)


- `x_i` = index of the share (1, 2, …, n)  
- `y_i` = encoded/encrypted value  

A minimum threshold of `k` shares is required to reconstruct the secret.

---

## Algorithm Used

To recover the constant term `c`:

1. **Decode each share** from its specified base into a decimal `BigInteger`.  
2. **Select any `k` shares** from the JSON file (threshold required to reconstruct).  
3. **Apply Lagrange interpolation at x = 0**:

\[
f(0) = \sum_{i=1}^{k} y_i \prod_{\substack{j=1 \\ j \neq i}}^{k} \frac{-x_j}{x_i - x_j}
\]

- `y_i` = decoded share value  
- `x_i` = share index  
- This formula calculates the **constant term** directly.  

4. **Sum the contributions** of each share → gives the secret `c`.

---

## Method Example

### Given shares

| x | y (decoded) |
|---|-------------|
| 1 | 4           |
| 2 | 7           |
| 3 | 12          |

Threshold `k = 3`  

**Step 1 — Compute Lagrange coefficients**

\[
\lambda_1 = \frac{-2}{1-2} * \frac{-3}{1-3} = 3
\]  
\[
\lambda_2 = \frac{-1}{2-1} * \frac{-3}{2-3} = -3
\]  
\[
\lambda_3 = \frac{-1}{3-1} * \frac{-2}{3-2} = 1
\]

**Step 2 — Multiply by y_i and sum**

\[
f(0) = 4*3 + 7*(-3) + 12*1 = 12 - 21 + 12 = 3
\]

✅ Reconstructed constant term: `c = 3`

---

## Project Structure

Decry/
│
├── src/
│   └── ShamirSecret.java  // Source Code
│
├── test_case_2.json //test case
│
└── lib/
    └── gson-2.10.1.jar jar library for json file

---

## Prerequisites

- Java JDK 8 or above  
- VS Code or any Java IDE  
- Gson library [download link](https://repo1.maven.org/maven2/com/google/code/gson/gson/2.10.1/gson-2.10.1.jar)

---

## How to Run

1. Open terminal in the project root.  
2. Compile the program:

**Usage**
```bash

Windows:

javac -cp ".;lib/gson-2.10.1.jar" src/ShamirSecret.java

Mac/Linux:

javac -cp ".:lib/gson-2.10.1.jar" src/ShamirSecret.java

Run the program:

Windows:

java -cp ".;lib/gson-2.10.1.jar;src" ShamirSecret

Mac/Linux:

java -cp ".:lib/gson-2.10.1.jar:src" ShamirSecret

Output Example
Constant term (c) = -6290016743746469796
Digit length = 20

Main instruction, need to change the file name the ShamirSecret.java to get the result for the specified encoded file.
 Line 20:  String var1 = "file_name.json";