import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import time
import json
import re

def scrape_website(url):
    """
    Enhanced scraper with comprehensive SEO data extraction
    """
    try:
        # Add https:// if not present
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Set headers to mimic a real browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Fetch the webpage with timing
        print(f"Fetching URL: {url}")
        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=15)
        load_time = time.time() - start_time
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Initialize SEO data dictionary
        seo_data = {
            'url': url,
            'status_code': response.status_code,
            'load_time': round(load_time, 2),
            
            # Basic Meta Tags
            'title': None,
            'title_length': 0,
            'meta_description': None,
            'meta_description_length': 0,
            'meta_keywords': None,
            'canonical_url': None,
            'meta_robots': None,
            
            # Open Graph Tags
            'og_title': None,
            'og_description': None,
            'og_image': None,
            'og_type': None,
            
            # Twitter Cards
            'twitter_card': None,
            'twitter_title': None,
            'twitter_description': None,
            
            # Heading Structure
            'h1_tags': [],
            'h2_tags': [],
            'h3_tags': [],
            'h4_tags': [],
            
            # Images
            'images': 0,
            'images_without_alt': 0,
            'images_with_alt': 0,
            
            # Links
            'internal_links': 0,
            'external_links': 0,
            'broken_links': 0,
            
            # Content Analysis
            'word_count': 0,
            'text_content': '',
            'paragraph_count': 0,
            
            # Technical SEO
            'has_https': url.startswith('https://'),
            'has_viewport': False,
            'has_favicon': False,
            'has_language': False,
            'language': None,
            'has_charset': False,
            'page_size_kb': len(response.content) / 1024,
            
            # Structured Data
            'has_schema': False,
            'schema_types': [],
        }
        
        # ========================================
        # 1. BASIC META TAGS
        # ========================================
        
        # Title Tag
        title_tag = soup.find('title')
        if title_tag:
            seo_data['title'] = title_tag.get_text().strip()
            seo_data['title_length'] = len(seo_data['title'])
        
        # Meta Description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            seo_data['meta_description'] = meta_desc.get('content', '').strip()
            seo_data['meta_description_length'] = len(seo_data['meta_description'])
        
        # Meta Keywords (legacy but still checked)
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords:
            seo_data['meta_keywords'] = meta_keywords.get('content', '').strip()
        
        # Canonical URL
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        if canonical:
            seo_data['canonical_url'] = canonical.get('href', '').strip()
        
        # Meta Robots
        meta_robots = soup.find('meta', attrs={'name': 'robots'})
        if meta_robots:
            seo_data['meta_robots'] = meta_robots.get('content', '').strip()
        
        # ========================================
        # 2. OPEN GRAPH TAGS
        # ========================================
        
        og_title = soup.find('meta', property='og:title')
        if og_title:
            seo_data['og_title'] = og_title.get('content', '').strip()
        
        og_desc = soup.find('meta', property='og:description')
        if og_desc:
            seo_data['og_description'] = og_desc.get('content', '').strip()
        
        og_image = soup.find('meta', property='og:image')
        if og_image:
            seo_data['og_image'] = og_image.get('content', '').strip()
        
        og_type = soup.find('meta', property='og:type')
        if og_type:
            seo_data['og_type'] = og_type.get('content', '').strip()
        
        # ========================================
        # 3. TWITTER CARDS
        # ========================================
        
        twitter_card = soup.find('meta', attrs={'name': 'twitter:card'})
        if twitter_card:
            seo_data['twitter_card'] = twitter_card.get('content', '').strip()
        
        twitter_title = soup.find('meta', attrs={'name': 'twitter:title'})
        if twitter_title:
            seo_data['twitter_title'] = twitter_title.get('content', '').strip()
        
        twitter_desc = soup.find('meta', attrs={'name': 'twitter:description'})
        if twitter_desc:
            seo_data['twitter_description'] = twitter_desc.get('content', '').strip()
        
        # ========================================
        # 4. HEADING STRUCTURE
        # ========================================
        
        # H1 Tags
        h1_tags = soup.find_all('h1')
        seo_data['h1_tags'] = [h1.get_text().strip() for h1 in h1_tags if h1.get_text().strip()]
        
        # H2 Tags
        h2_tags = soup.find_all('h2')
        seo_data['h2_tags'] = [h2.get_text().strip() for h2 in h2_tags if h2.get_text().strip()][:10]
        
        # H3 Tags
        h3_tags = soup.find_all('h3')
        seo_data['h3_tags'] = [h3.get_text().strip() for h3 in h3_tags if h3.get_text().strip()][:10]
        
        # H4 Tags
        h4_tags = soup.find_all('h4')
        seo_data['h4_tags'] = [h4.get_text().strip() for h4 in h4_tags if h4.get_text().strip()][:5]
        
        # ========================================
        # 5. IMAGES ANALYSIS
        # ========================================
        
        images = soup.find_all('img')
        seo_data['images'] = len(images)
        
        for img in images:
            alt_text = img.get('alt', '').strip()
            if alt_text:
                seo_data['images_with_alt'] += 1
            else:
                seo_data['images_without_alt'] += 1
        
        # ========================================
        # 6. LINKS ANALYSIS
        # ========================================
        
        domain = urlparse(url).netloc
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link['href'].strip()
            
            # Skip empty, anchor, javascript, and mailto links
            if not href or href.startswith(('#', 'javascript:', 'mailto:', 'tel:')):
                continue
            
            # Convert relative URLs to absolute
            absolute_url = urljoin(url, href)
            link_domain = urlparse(absolute_url).netloc
            
            # Classify as internal or external
            if domain in link_domain or link_domain in domain:
                seo_data['internal_links'] += 1
            else:
                seo_data['external_links'] += 1
        
        # ========================================
        # 7. CONTENT ANALYSIS
        # ========================================
        
        # Remove script and style elements
        for script in soup(['script', 'style', 'nav', 'footer', 'header']):
            script.decompose()
        
        # Get text content
        text_content = soup.get_text()
        lines = (line.strip() for line in text_content.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        seo_data['text_content'] = text[:3000]  # First 3000 chars for LLM
        seo_data['word_count'] = len(text.split())
        
        # Count paragraphs
        paragraphs = soup.find_all('p')
        seo_data['paragraph_count'] = len([p for p in paragraphs if p.get_text().strip()])
        
        # ========================================
        # 8. TECHNICAL SEO
        # ========================================
        
        # Viewport meta tag
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        seo_data['has_viewport'] = viewport is not None
        
        # Favicon
        favicon = soup.find('link', rel=lambda x: x and 'icon' in x.lower())
        seo_data['has_favicon'] = favicon is not None
        
        # Language declaration
        html_tag = soup.find('html')
        if html_tag and html_tag.get('lang'):
            seo_data['has_language'] = True
            seo_data['language'] = html_tag.get('lang')
        
        # Charset
        charset = soup.find('meta', attrs={'charset': True})
        if not charset:
            charset = soup.find('meta', attrs={'http-equiv': 'Content-Type'})
        seo_data['has_charset'] = charset is not None
        
        # ========================================
        # 9. STRUCTURED DATA (Schema.org)
        # ========================================
        
        # Look for JSON-LD
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        if json_ld_scripts:
            seo_data['has_schema'] = True
            for script in json_ld_scripts[:3]:  # Check first 3
                try:
                    data = json.loads(script.string)
                    if '@type' in data:
                        seo_data['schema_types'].append(data['@type'])
                    elif isinstance(data, list):
                        for item in data:
                            if '@type' in item:
                                seo_data['schema_types'].append(item['@type'])
                except:
                    pass
        
        # Look for Microdata
        if not seo_data['has_schema']:
            microdata = soup.find_all(attrs={'itemtype': True})
            if microdata:
                seo_data['has_schema'] = True
        
        print("✅ Scraping completed successfully!")
        print(f"   - Found {seo_data['word_count']} words")
        print(f"   - {len(seo_data['h1_tags'])} H1 tags, {len(seo_data['h2_tags'])} H2 tags")
        print(f"   - {seo_data['images']} images ({seo_data['images_with_alt']} with alt text)")
        print(f"   - Load time: {seo_data['load_time']}s")
        
        return seo_data
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching website: {e}")
        return {'error': f"Could not fetch website: {str(e)}"}
    except Exception as e:
        print(f"❌ Error parsing website: {e}")
        return {'error': f"Error analyzing website: {str(e)}"}