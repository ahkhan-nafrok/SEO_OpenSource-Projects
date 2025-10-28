def analyze_seo(seo_data):
    """
    Enhanced SEO analysis with comprehensive scoring
    Score out of 100 points with detailed breakdown
    """
    
    if 'error' in seo_data:
        return {
            'score': 0,
            'issues': [seo_data['error']],
            'strengths': [],
            'category_scores': {}
        }
    
    score = 0
    issues = []
    strengths = []
    category_scores = {
        'meta_tags': 0,
        'content': 0,
        'technical': 0,
        'social': 0
    }
    
    # ========================================
    # CATEGORY 1: META TAGS (30 points)
    # ========================================
    
    meta_score = 0
    
    # 1.1 Title Tag (10 points)
    if seo_data['title']:
        title_len = seo_data['title_length']
        if 30 <= title_len <= 60:
            meta_score += 10
            strengths.append("✅ Title tag length is optimal (30-60 characters)")
        elif 20 <= title_len <= 70:
            meta_score += 6
            issues.append(f"⚠️ Title tag length is {title_len} chars (optimal: 30-60)")
        elif title_len > 0:
            meta_score += 3
            issues.append(f"❌ Title tag length is {title_len} chars (needs improvement)")
        else:
            issues.append("❌ Title tag is empty")
    else:
        issues.append("❌ Missing title tag (critical SEO issue)")
    
    # 1.2 Meta Description (10 points)
    if seo_data['meta_description']:
        desc_len = seo_data['meta_description_length']
        if 120 <= desc_len <= 160:
            meta_score += 10
            strengths.append("✅ Meta description length is optimal (120-160 characters)")
        elif 100 <= desc_len <= 180:
            meta_score += 6
            issues.append(f"⚠️ Meta description is {desc_len} chars (optimal: 120-160)")
        elif desc_len > 0:
            meta_score += 3
            issues.append(f"❌ Meta description is {desc_len} chars (needs improvement)")
        else:
            issues.append("❌ Meta description is empty")
    else:
        issues.append("❌ Missing meta description (important for click-through rate)")
    
    # 1.3 Canonical URL (5 points)
    if seo_data['canonical_url']:
        meta_score += 5
        strengths.append("✅ Canonical URL is set (prevents duplicate content)")
    else:
        issues.append("⚠️ No canonical URL found (recommended for SEO)")
    
    # 1.4 Meta Robots (5 points)
    if seo_data['meta_robots']:
        meta_score += 5
        if 'noindex' in seo_data['meta_robots'].lower():
            issues.append("⚠️ Page is set to NOINDEX (won't appear in search results)")
        else:
            strengths.append("✅ Meta robots tag configured properly")
    else:
        meta_score += 2
        issues.append("⚠️ No meta robots tag (not critical but recommended)")
    
    category_scores['meta_tags'] = meta_score
    score += meta_score
    
    # ========================================
    # CATEGORY 2: CONTENT STRUCTURE (35 points)
    # ========================================
    
    content_score = 0
    
    # 2.1 H1 Tags (12 points)
    h1_count = len(seo_data['h1_tags'])
    if h1_count == 1:
        content_score += 12
        strengths.append("✅ Perfect! One H1 tag found")
    elif h1_count == 0:
        issues.append("❌ No H1 tag found (critical for SEO and accessibility)")
    else:
        content_score += 6
        issues.append(f"⚠️ Multiple H1 tags found ({h1_count}). Should have only 1")
    
    # 2.2 H2 Tags (8 points)
    h2_count = len(seo_data['h2_tags'])
    if h2_count >= 3:
        content_score += 8
        strengths.append(f"✅ Good content structure with {h2_count} H2 tags")
    elif h2_count >= 1:
        content_score += 4
        issues.append(f"⚠️ Only {h2_count} H2 tag(s). Add more for better structure")
    else:
        issues.append("❌ No H2 tags found. Add subheadings for better structure")
    
    # 2.3 Word Count (10 points)
    word_count = seo_data['word_count']
    if word_count >= 1000:
        content_score += 10
        strengths.append(f"✅ Good content length ({word_count} words)")
    elif word_count >= 500:
        content_score += 6
        issues.append(f"⚠️ Content is {word_count} words (aim for 1000+ for better SEO)")
    elif word_count >= 300:
        content_score += 3
        issues.append(f"⚠️ Content is short ({word_count} words). Add more valuable content")
    else:
        issues.append(f"❌ Very little content ({word_count} words). Search engines prefer comprehensive content")
    
    # 2.4 Internal Links (5 points)
    if seo_data['internal_links'] >= 5:
        content_score += 5
        strengths.append(f"✅ Good internal linking ({seo_data['internal_links']} links)")
    elif seo_data['internal_links'] >= 2:
        content_score += 3
        issues.append(f"⚠️ Only {seo_data['internal_links']} internal links. Add more for better SEO")
    else:
        issues.append("❌ Very few internal links. Add more to improve site navigation")
    
    category_scores['content'] = content_score
    score += content_score
    
    # ========================================
    # CATEGORY 3: TECHNICAL SEO (25 points)
    # ========================================
    
    technical_score = 0
    
    # 3.1 HTTPS (5 points)
    if seo_data['has_https']:
        technical_score += 5
        strengths.append("✅ Website uses HTTPS (secure)")
    else:
        issues.append("❌ Website is not using HTTPS (security risk and SEO penalty)")
    
    # 3.2 Page Load Time (5 points)
    load_time = seo_data['load_time']
    if load_time < 2:
        technical_score += 5
        strengths.append(f"✅ Fast load time ({load_time}s)")
    elif load_time < 4:
        technical_score += 3
        issues.append(f"⚠️ Load time is {load_time}s (aim for under 2s)")
    else:
        issues.append(f"❌ Slow load time ({load_time}s). Optimize for speed")
    
    # 3.3 Page Size (3 points)
    page_size = seo_data['page_size_kb']
    if page_size < 500:
        technical_score += 3
        strengths.append(f"✅ Good page size ({page_size:.1f} KB)")
    elif page_size < 1000:
        technical_score += 2
        issues.append(f"⚠️ Page size is {page_size:.1f} KB (try to keep under 500 KB)")
    else:
        issues.append(f"❌ Page size is {page_size:.1f} KB (too large, affects loading speed)")
    
    # 3.4 Mobile Viewport (3 points)
    if seo_data['has_viewport']:
        technical_score += 3
        strengths.append("✅ Mobile viewport meta tag present")
    else:
        issues.append("❌ Missing viewport meta tag (critical for mobile SEO)")
    
    # 3.5 Language Declaration (2 points)
    if seo_data['has_language']:
        technical_score += 2
        strengths.append(f"✅ Language declared ({seo_data['language']})")
    else:
        issues.append("⚠️ No language declaration in HTML tag")
    
    # 3.6 Favicon (2 points)
    if seo_data['has_favicon']:
        technical_score += 2
        strengths.append("✅ Favicon present")
    else:
        issues.append("⚠️ No favicon found (improves brand recognition)")
    
    # 3.7 Structured Data (5 points)
    if seo_data['has_schema']:
        technical_score += 5
        schema_types = ', '.join(seo_data['schema_types'][:3])
        if schema_types:
            strengths.append(f"✅ Structured data found ({schema_types})")
        else:
            strengths.append("✅ Structured data present")
    else:
        issues.append("⚠️ No structured data (Schema.org). Helps search engines understand your content")
    
    category_scores['technical'] = technical_score
    score += technical_score
    
    # ========================================
    # CATEGORY 4: SOCIAL & IMAGES (10 points)
    # ========================================
    
    social_score = 0
    
    # 4.1 Images Alt Text (5 points)
    if seo_data['images'] > 0:
        if seo_data['images_without_alt'] == 0:
            social_score += 5
            strengths.append(f"✅ All {seo_data['images']} images have alt text")
        else:
            missing_percent = (seo_data['images_without_alt'] / seo_data['images']) * 100
            if missing_percent < 30:
                social_score += 3
                issues.append(f"⚠️ {seo_data['images_without_alt']} out of {seo_data['images']} images missing alt text")
            else:
                social_score += 1
                issues.append(f"❌ {seo_data['images_without_alt']} out of {seo_data['images']} images missing alt text")
    else:
        social_score += 2
        issues.append("⚠️ No images found on the page")
    
    # 4.2 Open Graph Tags (3 points)
    og_count = sum([
        1 for x in [seo_data['og_title'], seo_data['og_description'], seo_data['og_image']] 
        if x
    ])
    if og_count >= 3:
        social_score += 3
        strengths.append("✅ Complete Open Graph tags for social sharing")
    elif og_count > 0:
        social_score += 1
        issues.append(f"⚠️ Only {og_count}/3 Open Graph tags found (add more for better social sharing)")
    else:
        issues.append("⚠️ No Open Graph tags (important for social media previews)")
    
    # 4.3 Twitter Cards (2 points)
    if seo_data['twitter_card']:
        social_score += 2
        strengths.append("✅ Twitter Card tags present")
    else:
        issues.append("⚠️ No Twitter Card tags (helps with Twitter sharing)")
    
    category_scores['social'] = social_score
    score += social_score
    
    # ========================================
    # ADDITIONAL CHECKS (Not scored but reported)
    # ========================================
    
    # External Links
    if seo_data['external_links'] > 0:
        strengths.append(f"✅ Has {seo_data['external_links']} external links (good for credibility)")
    else:
        issues.append("⚠️ No external links found (linking to authoritative sources helps SEO)")
    
    # Calculate percentage scores for categories
    category_percentages = {
        'meta_tags': round((category_scores['meta_tags'] / 30) * 100),
        'content': round((category_scores['content'] / 35) * 100),
        'technical': round((category_scores['technical'] / 25) * 100),
        'social': round((category_scores['social'] / 10) * 100)
    }
    
    return {
        'score': score,
        'issues': issues,
        'strengths': strengths,
        'category_scores': category_scores,
        'category_percentages': category_percentages,
        'seo_data': seo_data
    }