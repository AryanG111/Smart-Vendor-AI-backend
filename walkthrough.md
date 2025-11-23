# SmartVendor AI - API Verification Guide

This guide explains how to verify the SmartVendor AI backend using Postman.

## 1. Prerequisites
- Ensure the backend server is running:
  ```bash
  python run.py
  ```
  (It should be running on `http://127.0.0.1:5000`)

## 2. Import Postman Collection
1.  Download the **SmartVendor_Postman_Collection.json** file (provided in artifacts).
2.  Open **Postman**.
3.  Click **Import** (top left).
4.  Drag and drop the JSON file or select it.
5.  You will see a new collection named **SmartVendor AI**.

## 3. Environment Variables
The collection comes with pre-configured variables:
- `base_url`: `http://127.0.0.1:5000`
- `api_key`: `my-super-secret-admin-key`

> **Note**: If you changed the `API_KEY` in your `.env` file, please update the `api_key` variable in the Postman Collection (Click "SmartVendor AI" collection -> "Variables" tab).

## 4. Verification Steps

Run the requests in the following order to verify the full flow:

### Step 1: System Check
- **Health Check**: Should return `200 OK` `{"status": "healthy"}`.
- **Readiness Check**: Should return `200 OK` `{"status": "ready", "database": "connected"}`.

### Step 2: Vendor Management
- **Create Vendor**: Creates "TechSolutions Inc.".
    - *Expected*: `201 Created`, returns an `id`.
- **Get All Vendors**: Should list the vendor you just created.
- **Get Vendor by ID**: Fetch details for ID `1`.

### Step 3: Performance Tracking
- **Add Performance**: Adds a monthly performance record for Vendor 1.
    - *Expected*: `201 Created`.
- **Get Vendor History**: Should show the record you just added with calculated `overall_score`.

### Step 4: AI Features
- **Submit Feedback**: Sends "Great service..." text.
    - *Expected*: `201 Created`. The response should include `"sentiment": "POSITIVE"` (analyzed by DistilBERT).
- **Recommend Vendors**: Asks for "powerful servers".
    - *Expected*: `200 OK`. Should return a list of vendors ranked by similarity and performance. "TechSolutions Inc." should be near the top due to the "servers" keyword match.

### Step 5: Purchase Requests
- **Create Request**: Creates a request for 50 laptops.
    - *Expected*: `201 Created`.

## Troubleshooting
- **401 Unauthorized**: Check if the `X-API-KEY` header is correct.
- **500 Internal Server Error**: Check the terminal where `run.py` is running for error logs.
- **Connection Refused**: Ensure the server is running.
