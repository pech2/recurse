import dis

def fast_float(temp_str):
    return float(temp_str)

def slow_int(temp_str):
    return int(temp_str[:-2] + temp_str[-1:])

print("--- FAST FLOAT BYTECODE ---")
dis.dis(fast_float)

print("\n--- SLOW INT BYTECODE ---")
dis.dis(slow_int)

--- FAST FLOAT BYTECODE ---
  3           RESUME                   0

  4           LOAD_GLOBAL              1 (float + NULL)
              LOAD_FAST_BORROW         0 (temp_str)
              CALL                     1
              RETURN_VALUE

--- SLOW INT BYTECODE ---
  6           RESUME                   0

  7           LOAD_GLOBAL              1 (int + NULL)
              LOAD_FAST_BORROW         0 (temp_str)
              LOAD_CONST               0 (None)
              LOAD_CONST               1 (-2)
              BINARY_SLICE
              LOAD_FAST_BORROW         0 (temp_str)
              LOAD_CONST               2 (-1)
              LOAD_CONST               0 (None)
              BINARY_SLICE
              BINARY_OP                0 (+)
              CALL                     1
              RETURN_VALUE
