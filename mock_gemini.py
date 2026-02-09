def mock_gemini_response(df_columns):
    text = ""

    text += "ANALYSIS_PLAN:\n"
    text += "- Step 1: Inspect dataset columns and types\n"
    text += "- Step 2: Check missing values\n"
    text += "- Step 3: Summary stats for numeric columns\n"
    text += "- Step 4: Plot histogram or category counts\n\n"

    text += "PYTHON_CODE:\n"
    text += "```python\n"
    text += "import pandas as pd\n"
    text += "import matplotlib.pyplot as plt\n\n"

    text += "print('Columns:', list(df.columns))\n\n"

    text += "# Missing values\n"
    text += "missing = df.isna().sum().sort_values(ascending=False)\n"
    text += "print('\\nMissing values (top):')\n"
    text += "print(missing.head(10))\n\n"

    text += "# Numeric stats\n"
    text += "num_cols = df.select_dtypes(include='number').columns\n"
    text += "if len(num_cols) > 0:\n"
    text += "    print('\\nNumeric summary stats:')\n"
    text += "    print(df[num_cols].describe().T)\n\n"

    text += "    col = num_cols[0]\n"
    text += "    plt.figure()\n"
    text += "    df[col].dropna().hist(bins=20)\n"
    text += "    plt.title(f'Distribution of {col}')\n"
    text += "    plt.xlabel(col)\n"
    text += "    plt.ylabel('Count')\n"
    text += "    plt.tight_layout()\n"
    text += "else:\n"
    text += "    cat_cols = df.select_dtypes(exclude='number').columns\n"
    text += "    if len(cat_cols) > 0:\n"
    text += "        col = cat_cols[0]\n"
    text += "        top = df[col].astype(str).value_counts().head(10)\n"
    text += "        plt.figure()\n"
    text += "        top.plot(kind='bar')\n"
    text += "        plt.title(f'Top 10 categories for {col}')\n"
    text += "        plt.xlabel(col)\n"
    text += "        plt.ylabel('Count')\n"
    text += "        plt.tight_layout()\n"

    text += "```\n\n"

    text += "INSIGHTS:\n"
    text += "- Missing values were computed per column.\n"
    text += "- Summary statistics were generated for numeric columns.\n"
    text += "- At least one visualization was produced.\n"

    return text
