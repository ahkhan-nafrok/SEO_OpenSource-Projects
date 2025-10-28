import google.generativeai as genai
import os

def get_seo_suggestions(industry, seo_data, issues):
    """
    Enhanced AI suggestions with deep content analysis
    Provides comprehensive SEO recommendations based on actual scraped data
    """
    
    # Configure API key
    api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyB6kUdL4oPgML0R3xrb1Cv_KuODljRX46k')
    
    if not api_key or api_key == 'YOUR_API_KEY_HERE':
        print("⚠️ API key not configured properly")
        return get_fallback_suggestions(industry, seo_data)
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Build comprehensive context from scraped data
        current_h1 = seo_data['h1_tags'][0] if seo_data.get('h1_tags') else 'None'
        h2_list = ', '.join(seo_data['h2_tags'][:5]) if seo_data.get('h2_tags') else 'None'
        
        # Create detailed prompt with actual website data
        prompt = f"""You are an expert SEO consultant analyzing a {industry} website. Based on the data below, provide SPECIFIC, ACTIONABLE recommendations.

=== WEBSITE DATA ===
URL: {seo_data.get('url', 'N/A')}
Industry: {industry}

Current Title: {seo_data.get('title', 'Missing')}
Title Length: {seo_data.get('title_length', 0)} characters

Current Meta Description: {seo_data.get('meta_description', 'Missing')}
Meta Description Length: {seo_data.get('meta_description_length', 0)} characters

Current H1: {current_h1}
Current H2 Tags: {h2_list}

Content Stats:
- Word Count: {seo_data.get('word_count', 0)} words
- Images: {seo_data.get('images', 0)} ({seo_data.get('images_without_alt', 0)} missing alt text)
- Internal Links: {seo_data.get('internal_links', 0)}

Content Preview (first 500 chars):
{seo_data.get('text_content', '')[:500]}

=== SEO ISSUES FOUND ===
{chr(10).join(issues[:10]) if issues else 'No major issues'}

=== YOUR TASK ===
Provide detailed, specific recommendations in these 5 categories:

1. **OPTIMIZED TITLE TAG** - Write a better title tag (30-60 chars) that:
   - Includes primary keyword naturally
   - Is compelling for click-through
   - Specific to this {industry} business

2. **OPTIMIZED META DESCRIPTION** - Write a better meta description (120-160 chars) that:
   - Includes primary and secondary keywords
   - Has a clear call-to-action
   - Entices users to click

3. **IMPROVED H1 TAG** - Suggest a better H1 that:
   - Clearly states the page purpose
   - Includes primary keyword
   - Is engaging and descriptive

4. **CONTENT OUTLINE** - Provide 5-7 H2 subheadings for page structure:
   - Covers important topics for this industry
   - Includes relevant keywords naturally
   - Logical flow and comprehensive coverage

5. **TARGET KEYWORDS** - List 8 specific keywords for this {industry} business:
   - Mix of short-tail and long-tail keywords
   - Based on actual business and location if mentioned
   - Include search intent (informational, commercial, transactional)

6. **BLOG TOPICS** - Suggest 5 blog post ideas that:
   - Address customer pain points
   - Help with SEO and organic traffic
   - Establish authority in {industry}

Format your response EXACTLY like this (use exact section headers):

OPTIMIZED TITLE:
[Your optimized title here]

OPTIMIZED META DESCRIPTION:
[Your optimized meta description here]

IMPROVED H1:
[Your improved H1 here]

CONTENT OUTLINE:
- H2 subheading 1
- H2 subheading 2
- H2 subheading 3
(continue for 5-7 subheadings)

TARGET KEYWORDS:
- keyword 1
- keyword 2
(continue for 8 keywords)

BLOG TOPICS:
- Blog topic 1
- Blog topic 2
(continue for 5 topics)

Be specific and actionable. Base recommendations on the actual website content and industry."""

        print("🤖 Generating comprehensive AI recommendations...")
        
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=2000,
            )
        )
        
        result_text = response.text
        print("✅ Received detailed AI recommendations")
        
        # Parse the structured response
        suggestions = {
            'optimized_title': '',
            'optimized_meta_description': '',
            'improved_h1': '',
            'content_outline': [],
            'keywords': [],
            'blog_topics': []
        }
        
        current_section = None
        lines = result_text.split('\n')
        
        for line in lines:
            line_stripped = line.strip()
            
            # Detect section headers
            if 'OPTIMIZED TITLE:' in line_stripped.upper():
                current_section = 'optimized_title'
                continue
            elif 'OPTIMIZED META DESCRIPTION:' in line_stripped.upper():
                current_section = 'optimized_meta_description'
                continue
            elif 'IMPROVED H1:' in line_stripped.upper():
                current_section = 'improved_h1'
                continue
            elif 'CONTENT OUTLINE:' in line_stripped.upper():
                current_section = 'content_outline'
                continue
            elif 'TARGET KEYWORDS:' in line_stripped.upper() or ('KEYWORDS:' in line_stripped.upper() and 'TARGET' in line_stripped.upper()):
                current_section = 'keywords'
                continue
            elif 'BLOG TOPICS:' in line_stripped.upper():
                current_section = 'blog_topics'
                continue
            
            # Skip empty lines
            if not line_stripped:
                continue
            
            # Extract content based on current section
            if current_section in ['optimized_title', 'optimized_meta_description', 'improved_h1']:
                # These are single-line fields
                if not suggestions[current_section] and not line_stripped.startswith(('-', '*', '•', '#')):
                    suggestions[current_section] = line_stripped
            
            elif current_section in ['content_outline', 'keywords', 'blog_topics']:
                # These are list fields
                if line_stripped.startswith(('-', '*', '•')) or (line_stripped[0].isdigit() and '.' in line_stripped[:3]):
                    # Clean the line
                    cleaned = line_stripped.lstrip('-*•0123456789. ').strip()
                    if cleaned and len(cleaned) > 3:
                        suggestions[current_section].append(cleaned)
        
        # Validation and cleanup
        if not suggestions['optimized_title']:
            suggestions['optimized_title'] = seo_data.get('title', f"{industry} - Professional Services")
            print("⚠️ No title generated, using original")
        
        if not suggestions['optimized_meta_description']:
            suggestions['optimized_meta_description'] = seo_data.get('meta_description', f"Leading {industry} services with professional expertise.")
            print("⚠️ No meta description generated, using original")
        
        if not suggestions['improved_h1']:
            suggestions['improved_h1'] = current_h1 if current_h1 != 'None' else f"Welcome to {industry} Services"
            print("⚠️ No H1 generated, using original")
        
        if not suggestions['content_outline']:
            suggestions['content_outline'] = get_fallback_suggestions(industry, seo_data)['content_outline']
            print("⚠️ No content outline generated, using fallback")
        
        if not suggestions['keywords']:
            suggestions['keywords'] = get_fallback_suggestions(industry, seo_data)['keywords']
            print("⚠️ No keywords generated, using fallback")
        
        if not suggestions['blog_topics']:
            suggestions['blog_topics'] = get_fallback_suggestions(industry, seo_data)['blog_topics']
            print("⚠️ No blog topics generated, using fallback")
        
        # Limit lists to reasonable sizes
        suggestions['content_outline'] = suggestions['content_outline'][:7]
        suggestions['keywords'] = suggestions['keywords'][:8]
        suggestions['blog_topics'] = suggestions['blog_topics'][:5]
        
        print(f"✅ Parsed: Title, Meta Desc, H1, {len(suggestions['content_outline'])} outlines, {len(suggestions['keywords'])} keywords, {len(suggestions['blog_topics'])} topics")
        
        return suggestions
    
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error with Gemini AI: {error_msg}")
        
        # Check for common errors
        if 'API_KEY_INVALID' in error_msg or 'invalid' in error_msg.lower():
            print("⚠️ API key appears to be invalid. Please check your Gemini API key.")
        elif 'quota' in error_msg.lower():
            print("⚠️ API quota exceeded. Using fallback suggestions.")
        elif 'network' in error_msg.lower() or 'connection' in error_msg.lower():
            print("⚠️ Network error. Check your internet connection.")
        
        print("🔄 Using fallback SEO suggestions...")
        return get_fallback_suggestions(industry, seo_data)


def get_fallback_suggestions(industry, seo_data=None):
    """
    Enhanced fallback suggestions if AI fails
    Uses actual website data if available
    """
    
    if seo_data is None:
        seo_data = {}
    
    current_title = seo_data.get('title', '')
    current_h1 = seo_data['h1_tags'][0] if seo_data.get('h1_tags') else ''
    
    return {
        'optimized_title': current_title or f"Best {industry} Services - Professional {industry} Solutions",
        'optimized_meta_description': f"Looking for reliable {industry} services? We provide expert {industry} solutions with proven results. Contact us today for a free consultation.",
        'improved_h1': current_h1 or f"Professional {industry} Services You Can Trust",
        'content_outline': [
            f"Why Choose Our {industry} Services",
            f"Our {industry} Process and Methodology",
            f"Benefits of Professional {industry}",
            f"Common {industry} Challenges We Solve",
            f"Our {industry} Service Areas",
            f"Client Success Stories and Testimonials",
            f"Get Started with {industry} Today"
        ],
        'keywords': [
            f'best {industry} services',
            f'{industry} near me',
            f'affordable {industry}',
            f'{industry} expert',
            f'professional {industry}',
            f'top {industry} company',
            f'{industry} solutions',
            f'local {industry} services'
        ],
        'blog_topics': [
            f'Top 10 {industry} Tips for Beginners in 2024',
            f'How to Choose the Right {industry} Service Provider',
            f'Common {industry} Mistakes to Avoid',
            f'The Ultimate Guide to {industry} Best Practices',
            f'Why {industry} is Essential for Your Business Success'
        ]
    }


# Test function
def test_api():
    """Test if the API key is working"""
    try:
        api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyB6kUdL4oPgML0R3xrb1Cv_KuODljRX46k')
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        response = model.generate_content("Say 'API is working!' if you can read this.")
        print(f"✅ API Test Successful: {response.text}")
        return True
    except Exception as e:
        print(f"❌ API Test Failed: {e}")
        return False