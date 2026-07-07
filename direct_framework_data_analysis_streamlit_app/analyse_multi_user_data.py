# %%
import urllib.parse
import json
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
import os
# %%

# ENV VARS
gsheetkey = os.environ.get("GSHEETKEY")
sheet_name = os.environ.get("GSHEETNAME")


def url_string_to_user_data(url_string: str) -> dict:
    """
    Convert a URL string to a dictionary of user data.

    Args:
        url_string (str): The URL string containing user data.

    Returns:
        dict: A dictionary containing the user data.
    """
    # Extract the chart_data parameter from the URL
    parsed_url = urllib.parse.urlparse(url_string)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    chart_data = query_params.get("chart_data", [None])[0]

    if chart_data is None:
        raise ValueError("No chart_data found in the URL.")

    # Decode the chart_data from JSON
    user_data = json.loads(chart_data)[0]["user_data"]

    return user_data


# %%

url = f"https://docs.google.com/spreadsheet/ccc?key={gsheetkey}&output=csv"
input_df = pd.read_csv(url)

# # %%
user_data = [
    pd.DataFrame(
        [{**v, "user_id": i, **row.to_dict()} for v in url_string_to_user_data(row["Paste your competency data"])]
    )
    for i, row in input_df.iterrows()
]
# %%
all_user_df = pd.concat(user_data, ignore_index=True)
st.write("All User Data")
st.write(all_user_df.head(5))
# %%

# %%
# Create a matrix where rows are levels and columns are categories, and the values are the average skill levels for each user
matrix = all_user_df.pivot_table(
    index="skill_level", columns="category", values="user_id", aggfunc="count", fill_value=0
)
# %%
fig, ax = plt.subplots()
st.write("Skill Level Distribution Across Categories")
sns.heatmap(matrix, annot=True, fmt="d", cmap="Blues", ax=ax)
plt.xlabel("Category")
plt.ylabel("Skill Level")
plt.title("Skill Level Distribution Across Categories")
st.write(fig)

# %%
# TODO: Create a matrix for each institution
