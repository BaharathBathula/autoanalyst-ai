def mock_gemini_response(columns, question: str):
    q = (question or "").lower()

    # simple routing based on keywords
    if "country" in q:
        code = """
import matplotlib.pyplot as plt

counts = df['Country'].value_counts().head(10)
plt.figure()
counts.plot(kind='bar')
plt.title('Top 10 Countries by Customer Count')
plt.xlabel('Country')
plt.ylabel('Customers')
"""
    elif "city" in q:
        code = """
import matplotlib.pyplot as plt

counts = df['City'].value_counts().head(10)
plt.figure()
counts.plot(kind='bar')
plt.title('Top 10 Cities by Customer Count')
plt.xlabel('City')
plt.ylabel('Customers')
plt.xticks(rotation=45, ha='right')
"""
    elif "trend" in q or "time" in q or "date" in q or "subscription" in q:
        code = """
import matplotlib.pyplot as plt
import pandas as pd

d = df.copy()
d['Subscription Date'] = pd.to_datetime(d['Subscription Date'], errors='coerce')
d = d.dropna(subset=['Subscription Date'])
d['Year'] = d['Subscription Date'].dt.year
counts = d['Year'].value_counts().sort_index()

plt.figure()
plt.plot(counts.index, counts.values, marker='o')
plt.title('Subscriptions per Year')
plt.xlabel('Year')
plt.ylabel('Customers')
"""
    else:
        code = """
import matplotlib.pyplot as plt

plt.figure()
df.select_dtypes(include='number').hist()
plt.suptitle('Numeric Distributions')
"""

    return f"```python\n{code}\n```"
