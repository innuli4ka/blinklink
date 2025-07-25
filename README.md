# 🚀 BLINKLINK URL Shortener Project - Setup Tutorial

Step-by-step guide to setting up a BlinkLinlk - URL shortening service using AWS Lambda, Lambda Function URL DynamoDB, and S3 we  .

---

## 📋 Prerequisites

* Active AWS account
* IAM permissions to create/edit AWS services:
  -In this Tutorial we will use `LabRole`
* Python 3.12+ installed locally
* Basic AWS Console knowledge

---

## 🏗️ Architecture Overview

```mermaid
graph TD
    A[User] --> B[S3 Static Website]
    B --> C[Lambda Function URL - POST /shorten]
    C --> D[Lambda Function]
    D --> E[DynamoDB - Save URL]
    D --> F[Generate short ID]
    F --> G[Return short URL]
    G --> B
    B --> A[User]

```



---

## 📚 Step 1: Create DynamoDB Table

### 1.1 Open DynamoDB Console

1. Log into AWS Console
2. Search for "DynamoDB"
3. Click on "DynamoDB"
<img width="1002" height="429" alt="image" src="https://github.com/user-attachments/assets/9637bd59-b019-4834-837e-c1b5244754ba" />

### 1.2 Create Table

1. Click **"Create table"**
   <img width="1567" height="494" alt="image" src="https://github.com/user-attachments/assets/1cdaf2e1-af99-4f11-b25f-ce2ee816b160" />

3. Enter:

   * **Table name**: `ShortUrls`
   * **Partition key**: `id` (String)
     <img width="1169" height="590" alt="image" src="https://github.com/user-attachments/assets/0963a9da-23ea-4a31-8415-13bfd13c3b49" />

4. Leave defaults as is
5. Click **"Create table"**
<img width="1840" height="424" alt="image" src="https://github.com/user-attachments/assets/5016d31f-e047-47ca-aaaf-26ab529e6be3" />


### 1.3 Wait for Table to Be Active

* Wait until status is "Active" (\~1-2 minutes)

---

## ⚡ Step 2: Create Lambda Function

### 2.1 Open Lambda Console

1. Search for "Lambda"
2. Click on "Lambda"
<img width="1005" height="428" alt="image" src="https://github.com/user-attachments/assets/5064da19-a8b4-46a3-9f4e-2b6b5c46d102" />

### 2.2 Create a New Function

1. Click **"Create function"**
   <img width="1206" height="857" alt="image" src="https://github.com/user-attachments/assets/c7586e8e-42a5-47c1-94ec-84c8389b397b" />

3. Choose **"Author from scratch"**
4. Enter:
   * **Function name**: `url-shortener`
   * **Runtime**: `Python 3.12`
   * **Architecture**: `arm64`
<img width="1206" height="857" alt="image" src="https://github.com/user-attachments/assets/8917394e-bffa-4bed-933c-48e5e7b80202" />

### 2.3 Set Permissions

1. Under **"Change default execution role"**, select **"Use an existing role"**. From the dropdown option choose `LabRole`
2. Click **"Create function"**

<img width="1169" height="523" alt="image" src="https://github.com/user-attachments/assets/50a87dcc-99d9-45e0-a078-585752cfc686" />



---

## 📦 Step 3: Upload Code

### 3.1 Prepare Folder Structure

Create a new folder `url-shortener-lambda` and use this structure:

```
url-shortener-lambda/
├── lambda_function.py
├── handlers/
│   ├── __init__.py
│   ├── redirect_handler.py
│   └── create_handler.py
├── services/
│   ├── __init__.py
│   ├── database_service.py
│   └── id_generator.py
└── utils/
    ├── __init__.py
    ├── response_builder.py
    └── request_parser.py
```

### 3.2 Copy Your Code

Place all Python files in the correct folders.

### 3.3 Create a ZIP File

* **Windows**: Select files/folders → Right-click → "Send to" → "Compressed folder"
* **Mac**: Right-click → "Compress items"
* **Linux**: `zip -r url-shortener.zip *`

> ⚠️ Make sure files are at the root of the ZIP, not inside a subfolder!

### 3.4 Upload to Lambda

1. Go to your Lambda function
2. In **"Code"** tab, click **"Upload from"** → **".zip file"**

   <img width="1206" height="857" alt="image" src="https://github.com/user-attachments/assets/8e804f95-538e-42b4-9d17-b710f52a002d" />

4. Select your ZIP file
5. Click **"Save"**
   
<img width="1206" height="857" alt="image" src="https://github.com/user-attachments/assets/4bf81e55-8d18-43cd-ac20-d9a709c72c53" />

---

## 🌐 Step 4: Configure Lambda Function URL

### 4.1 Enable Function URL

1. In your Lambda function page, click **"Configuration"** → **"Function URL"**
2. Click **"Create function URL"**

<img width="1206" height="857" alt="image" src="https://github.com/user-attachments/assets/c5bf5dd3-ca86-4acd-a98f-5b7702f4ec25" />


3. Choose:

   * **Auth type**: `NONE` (for public access)
4. Click **"Save"**

<img width="1206" height="857" alt="image" src="https://github.com/user-attachments/assets/1d42833b-08d2-4b97-88eb-3c7772fa9fdd" />


### 4.2 Get Your Function URL

You’ll receive a URL like:

```
https://xxxxxx.lambda-url.region.on.aws/
```

This URL will be used for both POST and GET requests.

<img width="1206" height="857" alt="image" src="https://github.com/user-attachments/assets/4f4ff25b-03d1-40e5-9f99-3efa7d7c6f33" />


---

## 📂 Step 5: Create and Configure S3 Static Website

### 5.1 Create an S3 Bucket

1. Go to the AWS Console and search for "S3"
<img width="1206" height="857" alt="image" src="https://github.com/user-attachments/assets/b79eab39-cb20-422b-9857-b0987393955b" />

2. Click "Create bucket"

<img width="1206" height="857" alt="image" src="https://github.com/user-attachments/assets/53f9f151-03c5-44a4-9467-4e7a7aec7f33" />

3. Choose bucket type `General purpose`
4. Enter a unique Bucket name, e.g., `blinklink-frontend`
5. Under Object Ownership - choose `ACLs disabled (recommended)`
<img width="1206" height="857" alt="image" src="https://github.com/user-attachments/assets/44bc3d4d-52a7-4769-a253-850d7fa5f688" />
6.  Uncheck "Block all public access" (you will be prompted to acknowledge this change)
7.  Click "Create bucket"

<img width="1206" height="857" alt="image" src="https://github.com/user-attachments/assets/2fd3a630-1f07-4836-88e7-ab92e32297e5" />

### 5.2 Upload Website Files

1. Prepare your HTML/JS/CSS files locally
2. Click on your bucket name

<img width="1206" height="857" alt="image" src="https://github.com/user-attachments/assets/a8eb6535-b474-4fef-8e83-d91a43a9d0a1" />

3. Click "Upload" → Drag and drop or choose your files or folder → Click "Upload"
<img width="1206" height="857" alt="image" src="https://github.com/user-attachments/assets/3471695b-1d8c-4fc5-bdfa-ef671603cfee" />

<img width="1206" height="857" alt="image" src="https://github.com/user-attachments/assets/e7c70323-3129-4436-9a70-d703c3f3015a" />

### 5.3 Enable Static Website Hosting

1. Inside your bucket, go to the "Properties" tab

<img width="1206" height="857" alt="image" src="https://github.com/user-attachments/assets/b268e36f-b8e5-4f7d-8cb8-607f38f6a77a" />

2. Scroll to "Static website hosting" and click "Edit"

<img width="1206" height="857" alt="image" src="https://github.com/user-attachments/assets/e3d8d695-9bf5-48e5-9bda-5218a7d681fb" />

3. Select "Enable"
4. Under Index document: index.html (this is the html file that you updated earlier)
5. (Optional) Error document: error.html
6. Click "Save changes"

<img width="1206" height="857" alt="image" src="https://github.com/user-attachments/assets/b6786bf3-019c-47bb-b162-1fa2de3bf5ba" />

Scroll to the bottom of the page - you will see a static website endpoint URL. This is your frontend's public URL.
Copy it, we will use it later:

<img width="1206" height="857" alt="image" src="https://github.com/user-attachments/assets/9f691639-f2d7-40bb-bd29-2b034c827e9c" />


### 5.4 Set Permissions for Public Access

1. Go to the "Permissions" tab of your bucket
2. Scroll to "Bucket policy" and click "Edit"
<img width="1206" height="857" alt="image" src="https://github.com/user-attachments/assets/76e26caa-748b-41c6-996b-b17252340e5b" />

3. Paste the following policy (replace your-bucket-name), if you don't remember your bucket name, you can find it written under **"Bucket ARN**:
`
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::your-bucket-name/*"
    }
  ]
}
`
4. Click **Save Changes**

   <img width="1206" height="857" alt="image" src="https://github.com/user-attachments/assets/8509355d-8906-4fc5-bbf7-ce4af05274c2" />

---

## 🤜 Common Errors & Fixes

### "Unable to import module 'lambda\_function'"

* Ensure all files are at ZIP root level

### "User is not authorized to perform: dynamodb\:PutItem"

* Make sure the `AmazonDynamoDBFullAccess` policy is attached

### Redirect not working

* Confirm your Lambda logic is properly routing based on `event['rawPath']` or `event['path']`

### CORS Error

* Add CORS headers manually in your Lambda response

---

## 🚀 Upgrade Ideas

1. Analytics for clicks
2. Custom domains per user
3. User authentication
4. Expiration dates for links
5. QR code generation

---

## 📞 Need Help?

1. Check logs in CloudWatch
2. Ensure all services are in the same region
3. Double-check IAM permissions

---

## ✅ Summary

After following all steps, your URL shortener is ready:

* ✅ Create short links
* ✅ Automatic redirection
* ✅ Safe storage in DynamoDB
* ✅ Full Lambda logic with error handling
* ✅ Logging and monitoring
* ✅ Super low cost

**That's it! You're ready to go live! 🎉**
