# DIRECT-FRAMEWORK-data-analysis-streamlit-app

This is a Streamlit app for showing DIRECT Framework data.

The app is deployed on Google Cloud Run and can be accessed at [https://direct-framework-data-analysis-streamlit-app-git-935794760340.europe-west1.run.app/](https://direct-framework-data-analysis-streamlit-app-git-935794760340.europe-west1.run.app/).

## This is a Streamlit app for showing DIRECT Framework data.

## Deployment Pipeline

The deployment pipeline is defined in the `.github/workflows/release.yml` file.
It uses GitHub Actions to build and release the docker image.

A google cloud console Cloud Run app connects to the tag releases and releases
the docker image.
