import pandas as pd

# Create a sample DataFrame with Name, Age, and City columns
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Henry', 'Iris', 'Jack'],
    'Age': [25, 30, 35, 28, 32, 27, 29, 31, 26, 33],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
}

df = pd.DataFrame(data)
print(df)
