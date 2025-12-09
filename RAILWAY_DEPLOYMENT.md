# 🚂 Railway Deployment Guide

## Quick Deploy to Railway

Follow these steps to deploy your Bike-Sharing Station Planner to Railway:

### Step 1: Prepare Your Railway Account

1. Go to [Railway.app](https://railway.app/)
2. Sign up or log in with your GitHub account
3. Verify your account (you may need to add a payment method, but Railway offers free tier)

### Step 2: Create New Project

1. Click **"New Project"** on Railway dashboard
2. Select **"Deploy from GitHub repo"**
3. Choose **"matthewmakh/CSCI377_JJAY"** from your repositories
4. Railway will automatically detect it's a Python/Streamlit app

### Step 3: Configure Environment (if needed)

Railway should auto-detect everything, but if needed:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true`

These are already configured in `railway.toml`!

### Step 4: Deploy!

1. Railway will automatically start building and deploying
2. Wait for deployment to complete (usually 2-5 minutes)
3. Once deployed, Railway will provide a public URL like:
   - `https://csci377-jjay-production.up.railway.app`

### Step 5: Access Your Dashboard

1. Click the Railway-provided URL
2. Your interactive dashboard is now live! 🎉
3. Share the URL with anyone

---

## 🎯 What's Included in Deployment

### Files Deployed:
- ✅ `app.py` - Main Streamlit dashboard (980+ lines)
- ✅ `graph.py` - Graph data structure
- ✅ `shortest_path.py` - Pathfinding algorithms  
- ✅ `station_placement.py` - Optimization algorithms
- ✅ `requirements.txt` - All Python dependencies
- ✅ `railway.toml` - Railway configuration
- ✅ `.streamlit/config.toml` - Streamlit configuration
- ✅ All documentation (20+ markdown files)

### Features Available:
- 🗺️ Interactive route planning with real-time maps
- 📍 Smart station placement optimization
- 📊 Network analysis with beautiful charts
- 🎨 Modern, responsive UI
- ⚡ Fast, cached data loading

---

## 🔧 Troubleshooting

### Build Fails?
- Check that `requirements.txt` has all dependencies
- Verify Python version compatibility (3.8+)

### App Won't Start?
- Check Railway logs for errors
- Ensure PORT environment variable is used correctly
- Verify Streamlit config in `.streamlit/config.toml`

### Slow Performance?
- Railway free tier has resource limits
- Consider upgrading to Railway Pro for better performance
- The app uses caching to improve speed

### Map Not Loading?
- Ensure internet connection is available (for OpenStreetMap tiles)
- Check browser console for JavaScript errors

---

## 💰 Railway Pricing

**Free Tier:**
- $5 free credit per month
- Good for development and demos
- May sleep after inactivity

**Pro Tier:**
- $20/month
- Better performance
- No sleeping
- Custom domains

For this project, the **free tier should be sufficient** for demos and presentations!

---

## 🔄 Updating Your Deployment

When you make changes to your code:

1. Commit changes locally:
   ```bash
   git add .
   git commit -m "Your update message"
   ```

2. Push to GitHub:
   ```bash
   git push
   ```

3. Railway automatically redeploys! 🚀

---

## 📊 Monitoring Your App

In Railway dashboard you can:
- View deployment logs
- Monitor resource usage (CPU, RAM)
- Check error messages
- See visitor metrics

---

## 🌐 Custom Domain (Optional)

Want a custom domain like `bike-planner.yourdomain.com`?

1. Go to Railway project settings
2. Add custom domain
3. Configure DNS records
4. Railway handles SSL automatically

---

## ✅ Deployment Checklist

Before deploying, ensure:
- [x] All code pushed to GitHub
- [x] `requirements.txt` is complete
- [x] `railway.toml` is configured
- [x] `.streamlit/config.toml` exists
- [x] No sensitive data in code (API keys, etc.)
- [x] README.md is updated
- [x] All tests pass locally

---

## 🎓 For Presentation/Demo

**Perfect for:**
- Class presentations
- Portfolio showcases
- Project demonstrations
- Live coding demos
- Sharing with professors/peers

**Share your URL:**
```
https://your-app-name.up.railway.app
```

---

## 🆘 Need Help?

- Railway Docs: https://docs.railway.app/
- Streamlit Docs: https://docs.streamlit.io/
- Project Issues: https://github.com/matthewmakh/CSCI377_JJAY/issues

---

## 🎉 Success!

Once deployed, you have:
✨ A live, interactive bike-sharing planner  
✨ Shareable URL for anyone to access  
✨ Professional portfolio piece  
✨ Auto-updating from GitHub pushes  

**Your project is now live on the internet! 🌍**
