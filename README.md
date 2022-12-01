# asv-functions

This repository is part of the asv-webservices-project hosted in the Google Cloud.

The python-code generates thumbnails for coming up matchdays, uploads them to a firebase storage bucket and updates the
database with the public URL.

## Setup

To allow the project to upload and modify the db, identification is required.

Create a file containing the firebase-credentials:

`asv-webservices-firebase-credentials.json`

Add a service-account key to obtain the content for the file:

[console.cloud.google.com](https://console.cloud.google.com)
-> IAM -> Service Accounts

## Google Cloud

This project is deployed via Cloud Functions.

Functionality can be triggered by http-requests only (CORS is disabled accordingly).

## Zip for CloudFunctions-Upload

```bash
zip -r asv-functions.zip main.py requirements.txt asv-webservices-firebase-credentials.json season2223/
```