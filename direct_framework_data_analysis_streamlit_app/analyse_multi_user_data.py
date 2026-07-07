# %%
import urllib.parse
import json
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
import os
# %%

st.image("https://n8cir.org.uk/static/bootstrap/image/n8cir-logo-v1-cropped-224x63.png")

st.title("N8 CIR RSE Meetup 2026 - DIRECT Framework Data Analysis")
st.text("Data analysis of the DIRECT Framework competency data collected from multiple users.")

st.text(
    "Users are asked to complete their competencies in the DIRECT Framework and then share their data via a Google Sheet. This app will analyse the data from multiple users and provide visualisations of the results."
)

st.link_button("Go to DIRECT Framework web app", "https://directframework.com/")
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
columns = [
    "user_id",
    "category",
    "skill_level",
    "subcategory",
    "Career Stage",
    "Institution",
    "Timestamp",
]
user_data = [
    (
        pd.DataFrame(
            [{**v, "user_id": i, **row.to_dict()} for v in url_string_to_user_data(row["Paste your competency data"])]
        )
    )[columns]
    for i, row in input_df.iterrows()
    if row["Confirm you are happy for your data to be included anonymously in the dashboard"] == "Yes"
]
# %%
all_user_df = pd.concat(user_data, ignore_index=True)
st.header("All Skill Data")

st.dataframe(all_user_df)
st.download_button("Download All Skill Data as CSV", all_user_df.to_csv(index=False), "all_user_data.csv", "text/csv")
# %%
st.header("Skill data visualisations")
# %%
# Create a matrix where rows are levels and columns are categories, and the values are the average skill levels for each user
matrix = all_user_df[["skill_level", "category", "user_id"]].pivot_table(
    index="skill_level", columns="category", values="user_id", aggfunc="count", fill_value=0
)
# reverse the order of the rows in the matrix so that the highest skill level is at the top
matrix = matrix.iloc[::-1]
# %%
fig, ax = plt.subplots()
st.write("Skill Level Distribution Across Categories")
sns.heatmap(matrix, annot=True, fmt="d", cmap="Blues", ax=ax)
plt.xlabel("Category")
plt.ylabel("Skill Level")
plt.title("Skill Level Distribution Across Categories")
st.write(fig)

# %%

st.dataframe(all_user_df[all_user_df["skill_level"] == 2][all_user_df["category"] == "Communication"])
