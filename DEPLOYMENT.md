# SmartBackupSystem - Vercel Deployment Guide

## Project Structure for Vercel

```
SmartBackupSystem/
├── index.html              # Frontend (served as static file)
├── api/
│   └── proxy.py            # API endpoint - proxies requests to Lambda
├── vercel.json             # Vercel configuration
├── package.json            # Project metadata
└── .gitignore              # Files to exclude from git
```

## Deployment Steps

### 1. Install Vercel CLI
```bash
npm install -g vercel
```

### 2. Login to Vercel
```bash
vercel login
```

### 3. Deploy the Project
Navigate to your project directory and run:
```bash
vercel
```

Follow the prompts:
- Select your GitHub/GitLab account (or create new project)
- Choose to link an existing project or create new
- Vercel will automatically detect the configuration

### 4. Alternative: GitHub Integration
1. Push your project to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit for Vercel deployment"
   git remote add origin https://github.com/YOUR_USERNAME/smartbackupsystem.git
   git push -u origin main
   ```

2. Visit https://vercel.com/new and import your GitHub repository

## How It Works

- **Frontend (index.html)**: Served as a static file at the root
- **API Endpoint**: `/api` requests are routed to `api/proxy.py`
- **Proxy Function**: Converts calls to your Lambda function URL without CORS issues
- **CORS Headers**: All responses include CORS headers for cross-origin access

## Environment Variables (if needed in future)

If you need to add environment variables (like different Lambda URLs for different environments):

1. Create `api/.env.local` locally (for testing)
2. Add to Vercel Dashboard > Settings > Environment Variables for production

## Local Testing

To test locally before deploying:

```bash
vercel dev
```

Then open `http://localhost:3000` in your browser.

## File Exclusions

The `.gitignore` file excludes these from deployment:
- `backup_client.py`, `restore_file.py`, `timeline_viewer.py` (local utilities)
- `proxy_server.py` (local testing only - Vercel uses `api/proxy.py`)
- `testfile.txt`, `index1.html`, `index2.html` (not needed)
- `__pycache__`, `node_modules` (generated files)

## Troubleshooting

### Netlify shows `Failed to sync list (List parse failed (404))`
- Cause: this project's API routing in `vercel.json` is Vercel-specific, so Netlify does not know how to handle `/api` by default.
- Fix: keep the root `_redirects` file in the deployed publish directory so Netlify proxies `/api` to the Lambda Function URL.
- If you still see 404s, confirm `_redirects` is included in the deployed artifact and that the site publish directory is the repository root.

### Lambda errors 502
- Check that the `LAMBDA_URL` in `api/proxy.py` is correct
- Verify Lambda function is accessible from Vercel

### CORS errors
- All requests should go through `/api` endpoint
- The proxy function automatically adds CORS headers

### Static files not loading
- Ensure `index.html` is in the root directory
- Vercel automatically serves HTML, CSS, JS from root

## Support

For more details on Vercel deployment:
- https://vercel.com/docs/concepts/deployments/overview
- https://vercel.com/docs/functions/serverless-functions/python
