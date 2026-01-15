"""
Website Analyzer - Scrapes and extracts relevant context from client websites.
Used to enrich copy generation when strategy notes are light.
"""

import requests
from bs4 import BeautifulSoup
import re


def analyze_website(url):
    """
    Fetch and analyze a website to extract relevant context for copy generation.
    
    Returns:
        dict with extracted context like value_props, services, messaging, etc.
    """
    context = {
        "value_props": [],
        "services": [],
        "messaging": "",
        "social_proof": [],
        "ctas": [],
        "raw_text": ""
    }
    
    if not url or url == "https://example.com":
        return context
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Extract hero/headline content
        headlines = []
        for tag in soup.find_all(['h1', 'h2', 'h3']):
            text = tag.get_text(strip=True)
            if text and len(text) > 10 and len(text) < 200:
                headlines.append(text)
        
        # Extract value propositions from common patterns
        for tag in soup.find_all(['p', 'li', 'span', 'div']):
            text = tag.get_text(strip=True)
            # Look for value prop language
            if any(kw in text.lower() for kw in ['we help', 'we offer', 'we provide', 'our mission', 
                                                   'benefit', 'advantage', 'why choose', 'what we do']):
                if 20 < len(text) < 300:
                    context["value_props"].append(text)
        
        # Extract social proof (numbers, client mentions)
        for tag in soup.find_all(['p', 'span', 'div', 'li']):
            text = tag.get_text(strip=True)
            # Look for social proof patterns
            if re.search(r'\d+[\+]?\s*(clients|customers|companies|businesses|years|deals|transactions)', text.lower()):
                if len(text) < 200:
                    context["social_proof"].append(text)
        
        # Extract CTAs
        for button in soup.find_all(['button', 'a']):
            text = button.get_text(strip=True)
            if any(kw in text.lower() for kw in ['schedule', 'book', 'contact', 'get started', 
                                                   'learn more', 'talk to', 'free consultation']):
                if 3 < len(text) < 50:
                    context["ctas"].append(text)
        
        # Get main body text (limited)
        body_text = soup.get_text(separator=' ', strip=True)
        # Clean up whitespace
        body_text = re.sub(r'\s+', ' ', body_text)
        # Limit to first 2000 chars for context
        context["raw_text"] = body_text[:2000]
        
        # Store headlines as messaging
        context["messaging"] = " | ".join(headlines[:5])
        
        # Deduplicate
        context["value_props"] = list(set(context["value_props"]))[:5]
        context["social_proof"] = list(set(context["social_proof"]))[:3]
        context["ctas"] = list(set(context["ctas"]))[:3]
        
        print(f"📊 Analyzed website: {len(headlines)} headlines, {len(context['value_props'])} value props")
        
    except requests.RequestException as e:
        print(f"⚠️ Could not fetch website: {e}")
    except Exception as e:
        print(f"⚠️ Error analyzing website: {e}")
    
    return context


def format_website_context(context):
    """
    Format the extracted website context into a string for the LLM prompt.
    """
    parts = []
    
    if context.get("messaging"):
        parts.append(f"Headlines/Messaging: {context['messaging']}")
    
    if context.get("value_props"):
        parts.append(f"Value Props: {'; '.join(context['value_props'][:3])}")
    
    if context.get("social_proof"):
        parts.append(f"Social Proof: {'; '.join(context['social_proof'])}")
    
    if context.get("ctas"):
        parts.append(f"CTAs used: {', '.join(context['ctas'])}")
    
    if not parts and context.get("raw_text"):
        # Fall back to raw text summary
        parts.append(f"Website content summary: {context['raw_text'][:500]}...")
    
    return "\n".join(parts) if parts else "No website content available"
