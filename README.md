# Calci: Stateless Solana Calculator 🧮

## Overview
**Calci** is a **Stateless Solana Program** demonstrating fundamental blockchain interactions without persistent storage.
It performs mathematical operations (`Add`, `Sub`, `Mul`, `Div`) entirely within the transaction execution, returning results via **Program Logs**.

## 🎥 Demo Video


## 🛠 Technical Features

### 1. Stateless Execution
- **No Accounts**: Uses 0-byte storage. The program simply reads input data, computes, logs the result, and exits.
- **Cost Efficient**: Users only pay for the transaction signature (~0.000005 SOL), not rent-exempt storage.

### 2. Manual Instruction Packing (Python Client)
We bypass high-level abstractions to manually construct transaction data:
- **Discriminator**: First 8 bytes of `SHA256("global:instruction_name")`.
- **Arguments**: Inputs `a` (i64) and `b` (i64) are packed as Little Endian bytes (`<qq`).
```python
# [Discriminator (8 bytes)] + [Argument A (8 bytes)] + [Argument B (8 bytes)]
data = sha256("global:add")[:8] + struct.pack("<qq", 10, 5)
```

### 3. Atomic Transactions
The CLI demonstrates **Instruction Batching**.
Though not currently exposed in the simplified menu, the client allows adding multiple instructions `txn.add(ix1, ix2)` to a single transaction.
- **Atomicity**: Both math operations succeed, or both fail.

### 4. Log Parsing
Since there is no state to read back, we extract data from the **Transaction Simulation Logs**:
- The contract emits `msg!("Result: {}", result)`.
- The client polls for the transaction signature and parses `meta.log_messages` to find and display the answer.

## 📦 Project Structure
- `programs/calci/src/lib.rs`: The Smart Contract (Rust/Anchor).
    - Defines instructions: `add`, `sub`, `mul`, `div`.
- `python_cli/venv/cli.py`: The Main Client (Python).
    - Robust menu-based CLI with error handling.
- `python_cli/venv/own_cli.py`: Your custom implementation.

## 🚀 Usage

```bash
# 1. Activate Environment (if needed)
# source python_cli/venv/bin/activate

# 2. Run the CLI
python python_cli/venv/cli.py
```

### Flow:
1.  Enter `Number A`.
2.  Enter `Number B`.
3.  Select Operation (Add/Sub/Mul/Div).
4.  View Result (parsed from chain logs).
