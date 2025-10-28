# 🔍 Enhanced SEO Analyzer

A comprehensive SEO analysis tool that scrapes websites, analyzes 30+ SEO factors, and provides AI-powered recommendations using Google Gemini.

## ✨ New Features

### 1. **Enhanced Scraper** (30+ data points)
- ✅ Basic meta tags (title, description, keywords)
- ✅ Open Graph tags (for social media)
- ✅ Twitter Card tags
- ✅ Canonical URLs
- ✅ Meta robots tags
- ✅ Complete heading structure (H1-H4)
- ✅ Image analysis with alt text
- ✅ Internal/external link analysis
- ✅ Content word count
- ✅ Page load time
- ✅ HTTPS detection
- ✅ Mobile viewport tag
- ✅ Structured data (Schema.org)
- ✅ Language declaration
- ✅ Favicon detection
- ✅ Character encoding

### 2. **Comprehensive Scoring System** (100 points)
- **Meta Tags** (30 points): Title, description, canonical, robots
- **Content Structure** (35 points): Headings, word count, internal links
- **Technical SEO** (25 points): HTTPS, load time, viewport, structured data
- **Social & Images** (10 points): Alt text, Open Graph, Twitter Cards

### 3. **Enhanced AI Recommendations**
- 🎯 **Optimized Title Tag**: AI-generated, keyword-rich titles
- 📄 **Optimized Meta Description**: Compelling descriptions with CTAs
- 🎯 **Improved H1 Tag**: Better page headings
- 📋 **Content Outline**: 5-7 H2 subheadings for page structure
- 🔑 **Target Keywords**: 8 specific keywords for the industry
- ✍️ **Blog Topics**: 5 content ideas for SEO growth

## 🚀 Installation

### 1. Clone or Download the Project

```bash
cd seo-analyzer
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Gemini API Key (Free!)

1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy your API key
4. **Option A**: Set environment variable (recommended)
   ```bash
   # Windows
   set GEMINI_API_KEY=your_api_key_here
   
   # Mac/Linux
   export GEMINI_API_KEY=your_api_key_here
   ```
5. **Option B**: Edit `llm_helper.py` line 9 (not recommended for production)

### 5. Run the Application

```bash
python app.py
```

Visit: **http://localhost:5000**

## 📁 Project Structure

```
seo-analyzer/
├── app.py                    # Main Flask application (enhanced)
├── scraper.py                # Enhanced web scraper (30+ metrics)
├── analyzer.py               # Comprehensive SEO scoring
├── llm_helper.py             # AI-powered suggestions
├── requirements.txt          # Python dependencies
├── static/
│   ├── style.css            # Homepage styles
│   └── results.css          # Results page styles (new)
└── templates/
    ├── index.html           # Homepage
    └── results.html         # Results page (enhanced)
```

## 🎯 How to Use

1. **Enter Industry**: E.g., "Restaurant", "E-commerce", "Consulting"
2. **Enter Website URL**: E.g., "example.com" or "https://example.com"
3. **Click Analyze**: Wait 5-10 seconds for comprehensive analysis
4. **Review Results**:
   - Overall SEO score (0-100)
   - Category breakdown (Meta, Content, Technical, Social)
   - Issues to fix
   - AI-powered recommendations (if score < 70)
   - Technical details

## 📊 Scoring System

| Score | Rating | Description |
|-------|--------|-------------|
| 80-100 | Excellent 🎉 | Great SEO, minimal improvements needed |
| 60-79 | Good 👍 | Decent SEO, room for improvement |
| 0-59 | Needs Work ⚠️ | Significant SEO improvements needed |

### Score Breakdown:
- **Meta Tags** (30 pts): Title, description, canonical, robots
- **Content** (35 pts): H1/H2 structure, word count, links
- **Technical** (25 pts): HTTPS, speed, viewport, schema
- **Social** (10 pts): Images, Open Graph, Twitter Cards

## 🤖 AI Features Explained

### When Score < 70:
1. **Optimized Title**: SEO-friendly title with keywords
2. **Optimized Meta Description**: Compelling description (120-160 chars)
3. **Improved H1**: Better heading that includes keywords
4. **Content Outline**: 5-7 H2 subheadings for page structure
5. **Target Keywords**: 8 relevant keywords for ranking
6. **Blog Topics**: 5 content ideas to improve SEO

### Example Output:
```
Original Title: "Welcome to Our Website"
AI Optimized: "Best Restaurant Services in New York | Fresh Local Cuisine"

Original H1: "Welcome"
AI Improved: "Experience Authentic Italian Cuisine at Our NYC Restaurant"
```

## 🔧 Customization

### Change AI Score Threshold:
Edit `app.py` line 49:
```python
if analysis['score'] < 70:  # Change 70 to your preference
```

### Adjust Scoring Weights:
Edit `analyzer.py` to modify point allocations

### Use Different AI Model:
Edit `llm_helper.py` line 22:
```python
model = genai.GenerativeModel('gemini-1.5-pro')  # More powerful (still free)
```

## 🐛 Troubleshooting

### Issue: "API key not configured"
- Make sure you set `GEMINI_API_KEY` environment variable
- Or update the API key in `llm_helper.py`

### Issue: "Could not fetch website"
- Check if URL is accessible
- Some websites block scrapers (use incognito to test)
- Try adding `https://` explicitly

### Issue: "Slow analysis"
- Large websites take longer (10-15 seconds)
- Check your internet connection
- AI suggestions add 2-5 seconds

### Issue: CSS not loading
- Clear browser cache (Ctrl + F5)
- Check if `static/` folder exists
- Restart Flask server

## 📝 What Changed from Basic Version

### Scraper (`scraper.py`):
- ✅ Added 20+ new data points
- ✅ Open Graph & Twitter Cards
- ✅ Structured data detection
- ✅ Load time measurement
- ✅ Better link classification

### Analyzer (`analyzer.py`):
- ✅ Comprehensive 4-category scoring
- ✅ 100-point scale (vs 85 points before)
- ✅ More detailed issue detection
- ✅ Category percentage breakdown

### LLM (`llm_helper.py`):
- ✅ Context-aware prompts using scraped data
- ✅ Generates optimized title/meta/H1
- ✅ Creates content outlines
- ✅ Better parsing and validation
- ✅ Enhanced fallback system

### Frontend:
- ✅ New comparison view (before/after)
- ✅ Category score visualization
- ✅ Expandable technical details
- ✅ Better mobile responsiveness

## 🚀 Next Steps

Want to add more features? Consider:
- Competitor analysis
- Historical tracking with database
- PDF report generation
- Multi-page site crawling
- PageSpeed Insights API integration
- User authentication
- Scheduled re-scans

## 📄 License

Free to use for personal and commercial projects.

## 🙏 Credits

- Built with Flask, BeautifulSoup, and Google Gemini
- Enhanced by following SEO best practices from Moz, Ahrefs, and Google

---

**Happy SEO Analyzing! 🎉**
