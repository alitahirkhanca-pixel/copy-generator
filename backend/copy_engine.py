"""
Copy Engine - Core generation logic
Implements the 1M Messages copywriting framework to generate 4 email variations.
Now powered by Gemini Pro API with fallback to template mode.
"""

import random
from hooks import HOOK_TYPES, CTA_OPTIONS, PS_TEMPLATES, get_all_hook_types, get_hook

# Try to import Gemini client - may fail if not configured
try:
    from gemini_client import get_gemini_client
    GEMINI_AVAILABLE = True
except Exception as e:
    print(f"Gemini client not available: {e}")
    GEMINI_AVAILABLE = False


class CopyEngine:
    """
    Generates email copy variations based on:
    - Client onboarding data
    - Website context
    - Strategy notes
    
    Uses Gemini Pro API when available, falls back to templates.
    """

    def __init__(self, client_name, industry, audience, website, strategy):
        self.client_name = client_name
        self.industry = industry
        self.audience = audience
        self.website = website
        self.strategy = strategy
        
        # Extract key signals from strategy for personalization (fallback mode)
        self.pain_points = self._extract_pain_points(strategy)
        self.big_companies = ["Cozy Earth", "YSL", "BMW", "Microsoft", "Shopify"]

    def _extract_pain_points(self, strategy):
        """
        In a full implementation, this would use NLP/LLM to extract pain points.
        For now, we use simple keyword matching and fallbacks.
        """
        keywords = ["pain", "problem", "issue", "challenge", "struggle", "slow", "broken", "cost"]
        sentences = strategy.split('.')
        
        pain_points = []
        for sentence in sentences:
            lower = sentence.lower()
            if any(kw in lower for kw in keywords):
                pain_points.append(sentence.strip())
        
        # Fallbacks based on industry
        if not pain_points:
            pain_points = [
                f"scaling {self.industry} operations efficiently",
                f"reaching {self.audience} at the right moment",
                f"converting leads without burning budget"
            ]
        
        return pain_points

    def _fill_template(self, template, **extra_vars):
        """Fill a template string with context variables."""
        context = {
            "client": self.client_name,
            "industry": self.industry,
            "audience": self.audience,
            "website": self.website,
            "problem": random.choice(self.pain_points) if self.pain_points else "growth bottlenecks",
            "process": "outreach" if "outreach" in self.strategy.lower() else "workflow",
            "specific_issue": "email timing" if "email" in self.strategy.lower() else "conversion flow",
            "observation": f"how {self.client_name} is approaching {self.industry}",
            "big_company": random.choice(self.big_companies),
            "another_company": random.choice([c for c in self.big_companies if c != self.big_companies[0]])
        }
        context.update(extra_vars)
        
        try:
            return template.format(**context)
        except KeyError:
            # If a placeholder isn't found, just return the template with partial fills
            result = template
            for key, val in context.items():
                result = result.replace("{" + key + "}", str(val))
            return result

    def _generate_body(self, hook_type, opener):
        """
        Generate the email body following the structure:
        1. Pattern interrupt (opener)
        2. Flip the frame / insight
        3. Small CTA
        """
        # Frame flip based on hook type
        frame_flips = {
            "shot_in_the_dark": f"The conventional approach in {self.industry} usually misses the nuance. What we've seen work is a lighter-touch model.",
            "clarity_gap": f"Most people assume it's a {random.choice(['content', 'targeting', 'timing'])} issue. But the real blocker is usually upstream.",
            "math_problem": f"On paper, the metrics look fine. But when you zoom into payback windows, the story changes.",
            "overlooked_detail": f"It's a small thing — but when we fixed this for similar {self.industry} companies, replies went up 3x.",
            "anti_pitch": f"Just flagging something I've observed. No agenda here — just thought it might save you some headaches.",
            "status_signaling": f"This is something we stumbled on working with teams at {random.choice(self.big_companies)}. Might be worth exploring for {self.client_name}."
        }
        
        frame_flip = frame_flips.get(hook_type, "There's a simpler fix than what most people try first.")
        cta = random.choice(CTA_OPTIONS)
        
        body = f"""{opener}

{frame_flip}

{cta}"""
        return body

    def _generate_single_variation(self, hook_key, variation_id):
        """Generate a single email variation using the specified hook type."""
        hook = get_hook(hook_key)
        
        # Select and fill subject
        subject_template = random.choice(hook["subject_templates"])
        subject = self._fill_template(subject_template)
        
        # Select and fill opener
        opener_template = random.choice(hook["opener_templates"])
        opener = self._fill_template(opener_template)
        
        # Generate body
        body = self._generate_body(hook_key, opener)
        
        # Select and fill P.S.
        ps_template = random.choice(PS_TEMPLATES)
        ps = self._fill_template(ps_template)
        
        return {
            "id": variation_id,
            "hookType": hook["name"],
            "subject": subject,
            "body": body,
            "ps": ps
        }

    def generate_variations_template(self, count=4):
        """
        Generate variations using template mode (fallback).
        """
        all_hooks = get_all_hook_types()
        selected_hooks = random.sample(all_hooks, min(count, len(all_hooks)))
        
        variations = []
        for i, hook_key in enumerate(selected_hooks, start=1):
            variation = self._generate_single_variation(hook_key, i)
            variations.append(variation)
        
        return variations

    def generate_variations(self, count=4):
        """
        Generate `count` distinct email variations.
        Uses Gemini Pro API when available, otherwise falls back to templates.
        """
        # Try Gemini first
        if GEMINI_AVAILABLE:
            try:
                client = get_gemini_client()
                result = client.generate_variations(
                    self.client_name,
                    self.industry,
                    self.audience,
                    self.website,
                    self.strategy,
                    count
                )
                print("✅ Generated variations using Gemini Pro")
                return result["variations"]
            except Exception as e:
                print(f"⚠️ Gemini generation failed: {e}")
                print("📝 Falling back to template mode...")
        
        # Fallback to template mode
        print("📝 Using template mode for generation")
        return self.generate_variations_template(count)


def generate_copy(client_name, industry, audience, website, strategy, count=4):
    """
    Main entry point for generating email copy.
    
    Args:
        client_name: Name of the client/brand
        industry: Client's industry (e.g., "SaaS", "E-commerce")
        audience: Target audience (e.g., "Small Business Owners")
        website: Client's website URL
        strategy: Strategy call notes/summary
        count: Number of variations to generate (default: 4)
    
    Returns:
        dict with "variations" list
    """
    engine = CopyEngine(client_name, industry, audience, website, strategy)
    variations = engine.generate_variations(count)
    
    return {"variations": variations}
