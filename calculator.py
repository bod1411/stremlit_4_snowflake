import streamlit as st

def calculate(num1, num2, operation):
    if operation == "Add":
        return num1 + num2
    elif operation == "Subtract":
        return num1 - num2
    elif operation == "Multiply":
        return num1 * num2
    elif operation == "Divide":
        if num2 != 0:
            return num1 / num2
        else:
            return "Error: Division by zero"

st.title("Simple Calculator App")

# Input for two numbers
num1 = st.number_input("Enter the first number:", step=0.1)
num2 = st.number_input("Enter the second number:", step=0.1)

# Dropdown for operation selection
operation = st.selectbox("Choose an operation:", ["Add", "Subtract", "Multiply", "Divide"])

# Button to perform calculation
if st.button("Calculate"):
    result = calculate(num1, num2, operation)
    st.write(f"Result: {result}")