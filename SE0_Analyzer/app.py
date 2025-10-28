from flask import Flask, render_template, request, jsonify
from scraper import scrape_website
from analyzer import analyze_seo
from llm_helper import get_seo_suggestions

app = Flask(__name__)

@app.route('/')
def index():
    """Display the home page with input form"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Handle the SEO analysis request with enhanced features"""
    try:
        # Get form data
        industry = request.form.get('industry', '').strip()
        website_url = request.form.get('website_url', '').strip()
        
        # Validate inputs
        if not industry or not website_url:
            return render_template('results.html', 
                                 error="Please provide both industry and website URL")
        
        print(f"\n{'='*60}")
        print(f"🚀 STARTING ENHANCED SEO ANALYSIS")
        print(f"{'='*60}")
        print(f"Industry: {industry}")
        print(f"Website: {website_url}")
        print(f"{'='*60}\n")
        
        # Step 1: Scrape the website (enhanced with more data)
        print("📡 Step 1: Scraping website with enhanced crawler...")
        seo_data = scrape_website(website_url)
        
        if 'error' in seo_data:
            return render_template('results.html', 
                                 error=seo_data['error'])
        
        print(f"✅ Scraping complete - extracted {len(seo_data)} data points\n")
        
        # Step 2: Analyze SEO (enhanced scoring system)
        print("📊 Step 2: Analyzing SEO with comprehensive scoring...")
        analysis = analyze_seo(seo_data)
        
        print(f"✅ Analysis complete!")
        print(f"   Overall Score: {analysis['score']}/100")
        print(f"   Meta Tags: {analysis['category_scores']['meta_tags']}/30")
        print(f"   Content: {analysis['category_scores']['content']}/35")
        print(f"   Technical: {analysis['category_scores']['technical']}/25")
        print(f"   Social: {analysis['category_scores']['social']}/10\n")
        
        # Step 3: Get AI suggestions if score is low
        suggestions = None
        if analysis['score'] < 70:
            print(f"🤖 Step 3: Score is {analysis['score']}/100 - Getting enhanced AI suggestions...")
            suggestions = get_seo_suggestions(industry, seo_data, analysis['issues'])
            
            if suggestions:
                print(f"✅ AI Suggestions generated:")
                print(f"   - Optimized Title: {suggestions['optimized_title'][:50]}...")
                print(f"   - Optimized Meta Desc: {suggestions['optimized_meta_description'][:50]}...")
                print(f"   - Content Outline: {len(suggestions['content_outline'])} sections")
                print(f"   - Keywords: {len(suggestions['keywords'])} keywords")
                print(f"   - Blog Topics: {len(suggestions['blog_topics'])} topics")
        else:
            print(f"✅ Score is {analysis['score']}/100 - Great! No AI suggestions needed.")
        
        print(f"\n{'='*60}")
        print("✅ ANALYSIS COMPLETE!")
        print(f"{'='*60}\n")
        
        # Render results page with enhanced data
        return render_template('results.html',
                             industry=industry,
                             url=website_url,
                             score=analysis['score'],
                             issues=analysis['issues'],
                             strengths=analysis['strengths'],
                             analysis=analysis,  # Pass full analysis object
                             seo_data=seo_data,
                             suggestions=suggestions)
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return render_template('results.html', 
                             error=f"An error occurred: {str(e)}")

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 ENHANCED SEO ANALYZER STARTING...")
    print("="*60)
    print("✨ New Features:")
    print("   - Enhanced scraper with 30+ data points")
    print("   - Comprehensive scoring system (4 categories)")
    print("   - AI-powered title, meta, and H1 optimization")
    print("   - Content outline suggestions")
    print("   - Detailed technical SEO analysis")
    print("="*60)
    print("📍 Open your browser and go to: http://localhost:5000")
    print("="*60 + "\n")
    app.run(debug=True, port=5000)