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
assert gsheetkey is not None, "GSHEETKEY environment variable is not set."

# Utils

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


def get_user_data_from_gsheet(gsheetkey: str) -> pd.DataFrame:
    """
    Get user data from a Google Sheet.

    Args:
        gsheetkey (str): The key of the Google Sheet.

    Returns:
        pd.DataFrame: A DataFrame containing the user data.
    """
    url = f"https://docs.google.com/spreadsheet/ccc?key={gsheetkey}&output=csv"
    input_df = pd.read_csv(url)

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
    all_user_df = pd.concat(user_data, ignore_index=True)
    return all_user_df

# %%

all_user_df = get_user_data_from_gsheet(gsheetkey)


# Set up header

st.image("https://n8cir.org.uk/static/bootstrap/image/n8cir-logo-v1-cropped-224x63.png")

st.title("N8 CIR RSE Meetup 2026 - DIRECT Framework Data Analysis")



# == Plot functions ==

def plot_skill_level_category_distribution(df):
    # Create a matrix where rows are levels and columns are categories, and the values are the average skill levels for each user
    matrix = df[["skill_level", "category", "user_id"]].pivot_table(
        index="skill_level", columns="category", values="user_id", aggfunc="count", fill_value=0
    )
    # reverse the order of the rows in the matrix so that the highest skill level is at the top
    matrix = matrix.iloc[::-1]

    fig, ax = plt.subplots()
    st.write("Skill Level Distribution Across Categories")
    sns.heatmap(matrix, annot=True, fmt="d", cmap="Blues", ax=ax, cbar=False)
    plt.xlabel("Category")
    plt.ylabel("Skill Level")
    plt.title("Skill Level Distribution Across Categories")
    st.write(fig)

def plot_skill_level_subcategory_distribution(df):
    """Plots the distribution of skill levels across subcategories.

    The subcategories are grouped by category on the x axis, and the skill levels are represented by different colors in the bars. The height of each bar represents the number of users with that skill level in that subcategory.

    """
    # Create a matrix where rows are levels and columns are subcategories, and the values are the average skill levels for each user
    categories = df["category"].unique()
    st.header("Skill Level Distribution Across Subcategories")
    columns = st.columns(len(categories))
    max_val = df.groupby(["category", "subcategory", "skill_level"]).size().max()
    for i, cat in enumerate(categories):
        fig, ax = plt.subplots(figsize=(4, 6))
        df_cat = df[df["category"] == cat]

        matrix = df_cat[["skill_level", "subcategory", "user_id"]].pivot_table(
            index="skill_level", columns="subcategory", values="user_id", aggfunc="count", fill_value=0
        )
        # reverse the order of the rows in the matrix so that the highest skill level is at the top
        matrix = matrix.iloc[::-1]

        sns.heatmap(matrix, annot=True, fmt="d", cmap="Blues", ax=ax, cbar=False, square=True, vmin=0, vmax=max_val)
        ax.set_xlabel(cat)
        ax.set_ylabel("Skill Level")
        columns[i].write(cat)
        columns[i].write(fig)

def plot_skill_level_subcategory_distribution_per_institution(df):
    """Plots the distribution of skill levels across subcategories.

    The subcategories are grouped by category on the x axis, and the skill levels are represented by different colors in the bars. The height of each bar represents the number of users with that skill level in that subcategory.

    """
    # Create a matrix where rows are levels and columns are subcategories, and the values are the average skill levels for each user
    categories = df["category"].unique()
    st.header("Skill Level Distribution Across Subcategories Per Institution")
    max_val = df.groupby(["category", "subcategory", "skill_level", "Institution"]).size().max()
    for j, institution in enumerate(df["Institution"].unique()):
        st.header(f"Skill Level Distribution Across Subcategories for {institution}")
        columns = st.columns(len(categories))
        for i, cat in enumerate(categories):
            fig, ax = plt.subplots(figsize=(4, 4))
            df_cat = df[df["category"] == cat][df["Institution"] == institution]

            matrix = df_cat[["skill_level", "subcategory", "user_id"]].pivot_table(
                index="skill_level", columns="subcategory", values="user_id", aggfunc="count", fill_value=0
            )
            # reverse the order of the rows in the matrix so that the highest skill level is at the top
            matrix = matrix.iloc[::-1]

            sns.heatmap(matrix, annot=True, fmt="d", cmap="Blues", ax=ax, cbar=False, square=True, vmin=0, vmax=max_val)
            ax.set_xlabel(cat)
            ax.set_ylabel("Skill Level")
            columns[i].write(cat)
            columns[i].write(fig)

# == Pages ==


def intro_page():
    st.text("Data analysis of the DIRECT Framework competency data collected from multiple users.")

    st.text(
        "Users are asked to complete their competencies in the DIRECT Framework and then share their data via a Google Sheet. This app will analyse the data from multiple users and provide visualisations of the results."
    )

    st.link_button("Go to DIRECT Framework web app", "https://directframework.com/")



def raw_data_page():
    st.header("Raw Data")
    st.dataframe(all_user_df)
    st.download_button("Download All Skill Data as CSV", all_user_df.to_csv(index=False), "all_user_data.csv", "text/csv")


def skill_data_visualisations_page():
    # %%
    st.header("Skill data visualisations")
    plot_skill_level_category_distribution(all_user_df)
    plot_skill_level_subcategory_distribution(all_user_df)
    plot_skill_level_subcategory_distribution_per_institution(all_user_df)


page_names_to_funcs = {
    "Intro": intro_page,
    "Raw Data": raw_data_page,
    "Skill Data Visualisations": skill_data_visualisations_page,
}



# Setup  Sidebar

st.sidebar.header("N8 CIR RSE Meetup 2026 - DIRECT Framework Data Analysis")
st.sidebar.text("Data analysis of the DIRECT Framework competency data collected from multiple users.")
# Add links to each page of the app
page_name = st.sidebar.selectbox("Choose a page", page_names_to_funcs.keys())
page_names_to_funcs[page_name]()
