"""
Gemini Client - LLM integration for email copy generation
Uses the 1M Messages framework and cold email psychology principles.
Now includes website analysis for enriched context.
"""

import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Import website analyzer
try:
    from website_analyzer import analyze_website, format_website_context
    WEBSITE_ANALYZER_AVAILABLE = True
except ImportError:
    WEBSITE_ANALYZER_AVAILABLE = False
    print("⚠️ Website analyzer not available")

# Load environment variables
load_dotenv()


# =============================================================================
# COMPLETE 1M MESSAGES FRAMEWORK & COLD EMAIL PSYCHOLOGY
# =============================================================================

COPY_FRAMEWORK_CONTEXT = """
🚧 1. CORE PRINCIPLES (PULLED FROM 1M MESSAGES & CONVERSION COPYWRITING)

This is the foundation of everything:

✅ Conversational over corporate
Write how you'd speak in a DM or group chat — casual, smart, human.
Drop filler like "I hope this finds you well" or "would love to connect."
No jargon, no robotic intros, no fluff.

✅ Open loops > closing too hard
Most emails are not trying to sell — they're trying to spark curiosity.
The CTA is just to open the door — i.e. "Want me to send it over?" not "Can I book 30 mins?"

✅ Humor + unexpected detail builds trust
Tiny, specific details (e.g. "buried under 47 follow-ups") signal this isn't mass spam.
Light wit keeps tone confident but not pushy. This makes people want to reply.

✅ Be short, but not dry
Strip copy to the essence (2-4 lines max for DMs, 5-7 lines for emails).
But keep emotion, specificity, and edge.

🧠 2. MESSAGING BLUEPRINT

Each message uses some combo of these elements:

📌 Cold Email Stack:

Pattern Interrupt Subject Line
- Avoid "Quick question" or "Intro"
- Use something intriguing, casual, or unexpected:
  "This got awkward at $5M"
  "Turvo didn't fix this either"
  "Is this the weirdest email in your inbox?"

Problem Recognition (Open strong)
- Call out the pain with detail or specificity
- Be provocative but honest

Flip the Frame
- Reposition what the prospect thinks is the solution
- e.g. "It's not the ad creative — it's the payback math that's broken"

Credibility (softly)
- Mention recognizable names or outcomes casually (not bragging)
- e.g. "We helped Cozy Earth grow from $1.5M to $80M" or "We've worked with YSL, BMW, etc."

CTA = Curiosity / Hand-raise
- "Want a peek at the deck?"
- "Happy to send 3 quick fixes if useful"
- "Open to a quick call to sketch what this could look like?"

🧩 3. FRAMEWORKS WE USE (FROM 1M MESSAGES + PROVEN COPY MODELS)

🎯 A. The 1-Problem, 1-Offer Rule
Each message focuses on:
- One bottleneck
- One relevant fix
- One soft next step

🎭 B. The "Role-Based POV" Framework
Every message is built for who we're writing to:
- Founder: Speaks to bottleneck, scale tension, time
- Head of Ops: Workflow pain, hacks, load issues
- Sales leader: CAC, funnel, conversion math
- Clinician/Dr: Evidence + patient outcome + revenue

You must walk in their shoes → "What would this sound like if they vented it on Slack?"

💡 C. Hook Structures:

Here are a few of our most-used copy angles:

| Hook Type | Description | Example |
|-----------|-------------|---------|
| Shot in the Dark | Frame it as unlikely but potentially helpful | "Bit of a long shot, but would this be useful?" |
| Clarity Gap | Point to what's not obvious or missing | "Most patients don't realize this is gut-related" |
| Math Problem | Show that it's a numbers issue | "ROAS looks good but payback is quietly stretched" |
| Overlooked Detail | Zoom in on a specific, overlooked blocker | "The form field feels risky — that's killing signups" |
| Anti-Pitch | Emphasize that it's not a sales push | "Not a pitch — just a teardown of what's breaking" |
| Status Signaling | Mention big logos casually for authority | "Used by teams at Microsoft, YC, Procore" |

✍️ 4. COPY SYSTEM TO BUILD MESSAGES

Input:
- Who's the persona (title)?
- What's the moment of pain?
- What do they believe the problem is?
- What's actually causing it?
- What's a specific, non-obvious, lightweight fix?

Output Message:
```
Hey {{FirstName}},

[Pattern interrupt / recognition of problem]
[Flip the assumption / insight]
[Small offer or next step]

– Your Name
P.S. [Human note / light credential / fun detail]
```

🔁 5. FOLLOW-UP SYSTEM

Use progressive follow-ups, not repeats.

Follow-Up 1: "Just in case it got buried"
- Include a nudge + key benefit again

Follow-Up 2: Lighter CTA (send resource / lead magnet)
- "Want me to send a quick signal list we've seen work in this space?"

Follow-Up 3: Human check-in
- "Should I leave this alone or was it at least 10% interesting?"

🛠 6. BUILDING A STANDALONE COPY SYSTEM (YOUR INTERNAL PROCESS)

- Set up a database of angles + hooks
- Reuse successful templates + remix hooks
- Track opens/replies to measure performance
- Use Notion/Sheets for prospect signals
- Track ICP, roles, brand mentions, timing, etc.
- Write daily in short batches (3–5 message variations per angle per day)
- Train your voice to stay witty, smart, human

Edit in layers:
- First pass = raw draft
- Second pass = make it human
- Third pass = make it short
- Final pass = remove friction words

✅ TL;DR CHEATSHEET

| Principle | Reminder |
|-----------|----------|
| Be human | Write like a smart DM |
| Be specific | Vague = deleted |
| Open loops > closes | Tease value, don't pitch |
| Humor is trust | Not "funny" — just light and real |
| 1 idea per message | Kill the clutter |
| CTA = curiosity | "Want a peek?" wins |

---

THE PSYCHOLOGY OF COLD EMAIL

Cold email may be the rawest way to get direct market feedback from your ICP. If prospects don't like what you offer or what you say, they will let you know.

They do not care about your feelings, have had people tell me heinous things because of the unfortunate fact that my email happened to end up in their inbox.

When it comes to outbound sales, we are dealing with the primitive brain of the prospects we reach out to, nothing held back since they are faceless & have nothing to lose.

This, to many, is why outbound is scary to them & brings them to conclude it "doesn't work".

This couldn't be further from the truth.

Because we are dealing with the primitive, subconscious brain of the prospects here - we can actually find predictability.

At the subconscious level, humans are 99% the same.

We all have hardwired response mechanisms to certain social & environmental cues we encounter on a daily basis, and the subconscious is trained by consistent patterns within these daily occurrences.

Why does this matter or have anything to do with cold email?

Let's say you run a successful E-commerce store and receive 50 cold emails from marketing agencies in your inbox everyday. In your inbox, you see a plethora of:
- "quick question {Name}"
- "question {Name}"
- "thoughts?"
- "Hey {Name}"

When you open these emails, you see the same 75-150 word email giving the life story of how their agency is somehow "different" from the rest.

At the end of their long winded story (which you probably didn't read) they ask for 30 minutes of your precious time on a Zoom meeting you didn't have any intention of ever wanting to attend.

Now imagine for years on end this is what you see in your inbox everyday.

What do you think your immediate, subconscious response will be to these emails?
"SPAM" "UNSUBSCRIBE" "WHY DO I KEEP RECEIVING THESE EMAILS??"

Do you get it now?

Imagine everyday for YEARS you receive the same bullshit emails in your inbox with no end. I'd be pissed off too!

You might think: "Well if this is the case, then isn't cold email dead? Why even send cold emails if everyone is already being spammed and tired of it?"

This is true, IF you send the same spammy, non-relevant emails that 99% of cold emailers are sending.

When a prospect opens an email that looks just like the 100 other emails in their inbox, no matter how great of a service you run or how "well written" your email is, their subconscious brain immediately classifies you as spam.

If we really want to get their attention and not be classified by their subconscious as spam, we must be a…

PATTERN DISRUPT

Definition: "Recognizing an unwanted pattern, disrupting it, and leading someone to the desired behavior."

This is exactly what we are trying to achieve with our cold emails:
- Unwanted pattern: Being classified as spam
- Disrupt: Our well written, unique cold email
- Desired behavior: Meeting booked

So how do we write a cold email prospects actually want to read?

BE RELEVANT & PROVIDE VALUE

Write about what the prospect wants to hear, not what YOU want to tell them.

They only care about 5 things:
1. How will you make more money enter my bank account?
2. Have you successfully helped others just like me before?
3. Did this person do any research on our company?
4. Are you a real person or a scammer?
5. Is this a waste of my time?

You must address each one of these in your email, and do it in less than 50 words.

You have a solid 5 seconds to catch your prospects' attention & keep them engaged, they don't have time or want to read a whole ass essay.

Get straight to the point.

Here's an example of a TikTok organic offer to clothing brands:

"Real quick {{name}}, created a deck outlining the TikTok organic strategy we used to help Nike generate 10,000,000 views on TikTok in 30 days.

May I share with you?"

In 31 words, we addressed EVERY objection the prospect had in their mind opening your cold email:

Q: How will you make more money enter my bank account?
A: TikTok organic

Q: Have you successfully helped others just like me before?
A: Helped Nike generate 10,000,000 views in 30 days

Q: Did this person do any research on our company?
A: Relevant clothing brand case study for their clothing brand

Q: Are you a real person or a scammer?
A: Website w/ social proof & LinkedIn

Q: Is this a waste of my time?
A: Only 30 words long & offer valuable strategy deck covering great result

Get it?

No bs personalization, no long essay, not asking for anything in return - just straight leading with value.

This is a pattern disrupt.

This is something prospects actually don't mind receiving in their inbox.

Because you are presenting them value first, not trying to blatantly take their time away from them and sell them right out the gates.

We are also taking advantage of reciprocity since when you give to someone without asking for return, they naturally feel obliged to give something back.

So next time you're writing a cold email, keep this in mind:
1. Be a pattern disrupt, don't blend in
2. Write about them, not you
3. Lead with value first
4. Cut all the bs

---

BEST COLD EMAIL FRAMEWORKS

Framework #1 (Lead Magnet):
{{first_name}} – created a {{Lead Magnet}} for {{company_name}} covering the {{Mechanism Strategy}} we implemented to help {{Client from same Industry}}, {{Client Name}}, generate {{Result}} within the last {{Timeframe}} – {{CTA}}?

Framework #2 (One-Liner + P.S.):
{{first_name}} – interested in {{Free Work/Frontend Offer}} for {{company_name}}?
%signature%
P.S. {{Social proof}}
NOTE: this is literally the full email, one sentence + P.S. line

Framework #3 (Guarantee):
{{first_name}} – interested in generating {{Dream Result}} with {{Mechanism}} for {{company_name}} in the next {{Timeframe}}?
Asking since our {{Mechanism}} guarantees {{Dream Result}} in {{Timeframe}} for your company or {{Risk Reversal}} – {{CTA}}?
NOTE: can offer a lead magnet for the CTA as well

Framework #4 (Pain Point):
{{first_name}} – {{Relevant question around pain point}}?
Our {{solution}} offers {{how to fix problem}} to {{achieve end result of solution}}
{{Interest-based CTA}}
%signature%
P.S. {{Social proof}}

Framework #5 (Touchpoint):
{{first_name}} – {{Relevant Touchpoint}}
Noticed {{Relevant Pain Point}}
Interested in {{Quick Solution to Pain Point}}?

Framework #6 (Market Insight):
{{first_name}} – {{Question around relevant touchpoint}}
{{Unique Market Insight Relevant to Initial Touchpoint Questions}}
{{CTA around offering implementing Unique Market Insight}}
NOTE: You need to use market research to come up with a unique market insight angle for this email.

---

FRONT-END OFFERS (All copy should be centered around these):

1. Service-Based Front-End Offer (Free Audit or Diagnostic)
A service where you review, assess, or analyze something in their business — essentially "looking under the hood."
Examples:
- Free creative audit
- Free ad account diagnostic
- Free growth bottleneck audit
- Free performance snapshot
Why: Makes the first step feel helpful and consultative, giving prospects clarity on what's broken and what to fix AND allows you to naturally progress into the pitch/sales process because you know their exact problems.

2. Deliverable-Based Front-End Offer (You Create Something for Them)
A done-for-them asset — something you actually produce and deliver to the prospect.
Examples:
- Free ad creative (image or video asset)
- Free landing page mockup
- Free email flow outline
- Free micro-strategy play (e.g., "Your 3 quick wins for Q4")
Why: They receive something tangible you created, showcasing capability and giving them a reason to book to see "what else you can do." and we require a meeting to provide the deliverable, which can then transition into sales process.

3. Solution-Focused Asset (Generic or Custom)
A short PDF/Gamma doc that solves a common industry pain point.
Examples:
- "Why Growth Stalls + How to Fix It" guide
- "3 Bottlenecks Preventing Scale" breakdown
- Custom CRO quick-win outline
- Custom margin-improvement breakdown
Why: Demonstrates expertise and provides immediate value, helping prospects understand your thinking before a call.

4. Case Study Breakdown Asset (How You Produced a Specific Result)
A transparent walkthrough — written, video (or even better, both) — showing exactly how you achieved a real outcome for a client.
Examples:
- Written step-by-step breakdown of a past win
- Video teardown explaining the strategy and actions
Why: Builds credibility fast by revealing the process behind real results, making it easy for prospects to picture how you'd help them.
"""


class GeminiClient:
    """
    Handles communication with Google's Gemini API.
    Generates email variations using cold email psychology principles.
    """

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your_api_key_here":
            raise ValueError("GEMINI_API_KEY not configured. Please set it in backend/.env")
        
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-2.5-flash"

    def generate_variations(self, client_name, industry, audience, website, strategy, count=4):
        """
        Generate email variations using Gemini with cold email psychology.
        
        Returns:
            dict with "variations" list, or raises exception on failure
        """
        
        # Analyze the website for additional context
        website_context = ""
        if WEBSITE_ANALYZER_AVAILABLE and website:
            print(f"🌐 Analyzing website: {website}")
            context = analyze_website(website)
            website_context = format_website_context(context)
        
        # Build the full prompt with complete framework context
        prompt = f"""{COPY_FRAMEWORK_CONTEXT}

---

## YOUR TASK NOW

You have internalized the 1M Messages framework above. Now THINK like a master copywriter who has written 10,000 cold emails and knows exactly what makes prospects stop scrolling.

## ⚠️ CRITICAL: UNDERSTAND WHO IS WHO

- **SENDER (who we're writing FOR)**: {client_name}
- **RECIPIENTS (who we're emailing TO)**: {audience}

The email is written BY {client_name} TO reach {audience}.
- {client_name} = the company offering the service
- {audience} = the prospects/leads receiving the email

❌ WRONG: "Not sure if this applies to {client_name}..." (treating client as recipient)
✅ RIGHT: "Not sure if this applies to your [audience's business type]..." (talking TO the recipient)

DO NOT mention {client_name} in the email body. The email is FROM them, not TO them.

## THE BRIEF

- **WE ARE WRITING FOR**: {client_name} (the sender)
- **WE ARE REACHING OUT TO**: {audience} (the recipients/prospects)
- **Industry**: {industry}
- **Website**: {website}

**Website Intel**:
{website_context if website_context else "No website data scraped - rely on strategy notes."}

**Strategy / Offer**:
{strategy if strategy else "Infer the offer from context."}

## HOW TO THINK ABOUT THIS

Before writing, ask yourself:
1. What keeps {audience} up at night? What's the real pain behind the pain?
2. What do they THINK the solution is? How can I flip that assumption?
3. What's one ultra-specific detail from the strategy that would make them think "okay, this person actually gets it"?
4. What would make this email feel like it came from a friend, not a vendor?
5. How can I lead with value so compelling they feel obligated to respond (reciprocity)?

## AVOID THESE TEMPLATED PATTERNS

❌ "Bit of a long shot, but..." (overused)
❌ "Not a pitch, but..." (everyone says this)
❌ "Just wanted to reach out..." (filler)
❌ "I noticed that..." (generic)
❌ "Would you be open to..." (weak CTA)
❌ "I help companies like yours..." (me-focused)

## INSTEAD, TRY THESE ANGLES

✅ Start with a provocative observation about their world
✅ Reference something ultra-specific (numbers, timelines, pain points from strategy)
✅ Ask a question that makes them think "huh, I never considered that"
✅ Use pattern interrupts that feel fresh, not formulaic
✅ Make the CTA so low-friction it feels rude to ignore

## ⚠️ CRITICAL RULES - DO NOT BREAK THESE

1. **NEVER reference case studies from the training examples above** (NO Cozy Earth, NO Nike, NO YSL, NO BMW, NO Microsoft). These are examples ONLY. Use ONLY info from the user's strategy notes below.

2. **EVERY email body MUST end with a CTA** - a curiosity-based question or soft ask:
   - "Want me to send it over?"
   - "Worth a quick look?"
   - "Curious if this resonates?"
   - "Mind if I share how?"
   - "Open to a peek?"

3. **P.S. lines must ONLY use information from the user's strategy notes** - NO hallucinated claims, NO made-up credentials, NO fake case studies. If the user didn't mention a case study, DON'T invent one.

4. If you don't have specific case studies from the user, make the P.S. human/light instead:
   - "P.S. No pressure either way - just thought it might click."
   - "P.S. Happy to leave it alone if timing's off."
   - "P.S. Took 2 min to write, takes 10 sec to reply 'nope' if not useful."

## CREATE 4 DISTINCT VARIATIONS

Each should use a DIFFERENT psychological angle from the framework:

1. **The Unexpected Insight**: Lead with something they haven't considered. Flip their assumptions.
2. **The Specificity Play**: Zoom in on one hyper-specific detail that signals deep understanding.
3. **The Casual Value Drop**: Offer something genuinely useful with zero ask attached.
4. **The Pattern Break**: Write something that looks/feels NOTHING like the 100 other emails in their inbox.

## EMAIL STRUCTURE (FOLLOW THIS EXACTLY)

Each email body MUST follow this structure:
```
{{{{first_name}}}} – [Opening hook / insight / observation]

[Middle: flip the frame, add value, or expand on the insight]

[FINAL LINE = CTA QUESTION - this is MANDATORY]
```

CTA EXAMPLES (use these as the LAST LINE of the body):
- "Worth a quick look?"
- "Want me to send it over?"
- "Curious if this resonates?"
- "Mind if I share how we do it?"
- "Open to a 2-min breakdown?"
- "Should I send the details?"

## OUTPUT FORMAT (JSON)

{{
  "variations": [
    {{
      "id": 1,
      "hookType": "Unexpected Insight",
      "subject": "lowercase intriguing subject",
      "body": "{{{{first_name}}}} – Most [audience] assume X. But the real issue is Y.\\n\\nWe found Z works better.\\n\\nWorth a quick look?",
      "ps": "P.S. No pressure - just thought it might click."
    }},
    {{
      "id": 2,
      "hookType": "Specificity Play",
      "subject": "the [specific number] detail",
      "body": "{{{{first_name}}}} – Noticed [specific detail from strategy].\\n\\nThat one thing often [outcome].\\n\\nCurious if this resonates?",
      "ps": "P.S. Happy to leave it alone if timing's off."
    }},
    {{
      "id": 3,
      "hookType": "Casual Value Drop",
      "subject": "something for [audience type]",
      "body": "{{{{first_name}}}} – Put together [resource/breakdown/audit] for [their situation].\\n\\nNo strings attached.\\n\\nWant me to send it over?",
      "ps": "P.S. Took 2 min to make, takes 10 sec to reply 'nope' if not useful."
    }},
    {{
      "id": 4,
      "hookType": "Pattern Break",
      "subject": "weird question",
      "body": "{{{{first_name}}}} – [Unexpected opening that breaks the pattern].\\n\\n[Quick value/insight].\\n\\nMind if I share how?",
      "ps": "P.S. No agenda either way."
    }}
  ]
}}

## ⛔ ANTI-HALLUCINATION RULES (MANDATORY)

You MUST NOT invent ANY of these:
- ❌ Case studies: "when we fixed this for similar companies, replies went up 3x" - BANNED
- ❌ Metrics: "saw 47% increase" or "3x replies" - BANNED unless in user's strategy notes
- ❌ Client mentions: "worked with Video production teams" - BANNED unless in strategy
- ❌ Framework examples: Cozy Earth, Nike, YSL, BMW, Microsoft - BANNED
- ❌ Made up credentials: "top 1% partner" or "we've seen this move the needle" - BANNED

If you don't have specific metrics or case studies from the strategy notes, use GENERIC language:
- ✅ "Worth a quick look?"
- ✅ "Curious if this resonates?"
- ✅ "No pressure either way."

## CRITICAL REMINDERS

1. The CTA question MUST be the FINAL LINE of the body - NOT after the signature
2. EVERY variation MUST have a CTA question as the last line
3. DO NOT HALLUCINATE - only use facts from the strategy notes provided
4. P.S. = human touch only, no fake credentials or made-up results
5. Under 50 words per email body
6. DO NOT mention {client_name} in the email body - you are writing FROM them

FINAL CHECK: Each email FROM {client_name} TO {audience}. Last line of body = CTA? No made-up metrics or case studies?"""

        # Debug: print what we're sending
        print(f"\n🔍 Writing FOR: {client_name}")
        print(f"📧 Sending TO: {audience}")
        print(f"🎯 Strategy: {strategy[:100] if strategy else 'Using website analysis'}...")
        if website_context:
            print(f"🌐 Website context: {website_context[:150]}...")
        
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.5,  # Lower temp to reduce hallucinations
                    max_output_tokens=4000,
                )
            )
            
            # Parse the response
            text = response.text.strip()
            print(f"📝 Raw response length: {len(text)} chars")
            
            # Handle potential markdown code blocks
            if text.startswith("```"):
                lines = text.split("\n")
                end_idx = -1
                for i in range(len(lines) - 1, 0, -1):
                    if lines[i].strip() == "```":
                        end_idx = i
                        break
                if end_idx > 0:
                    text = "\n".join(lines[1:end_idx])
                else:
                    text = "\n".join(lines[1:])
            
            # Also handle ```json
            if text.startswith("json"):
                text = text[4:].strip()
            
            # Try to extract JSON using regex if direct parsing fails
            import re
            try:
                result = json.loads(text)
            except json.JSONDecodeError:
                # Try to find JSON object in text
                json_match = re.search(r'\{[\s\S]*"variations"[\s\S]*\}', text)
                if json_match:
                    try:
                        result = json.loads(json_match.group())
                    except json.JSONDecodeError:
                        # Last resort: try to fix common issues
                        fixed_text = text.replace('\n', '\\n').replace("'", '"')
                        result = json.loads(fixed_text)
                else:
                    raise ValueError("Could not find valid JSON in response")
            
            # Validate structure
            if "variations" not in result:
                raise ValueError("Response missing 'variations' key")
            
            # Post-process: Clean up any formatting issues
            for variation in result["variations"]:
                if "body" in variation:
                    variation["body"] = variation["body"].replace("\\n", "\n")
            
            if len(result["variations"]) < count:
                print(f"Warning: Only {len(result['variations'])} variations generated")
            
            print(f"✅ Generated {len(result['variations'])} variations using 1M Messages framework")
            return result
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parse error: {e}")
            print(f"Raw text: {text[:500]}")
            raise ValueError(f"Failed to parse LLM response as JSON: {e}")
        except Exception as e:
            raise RuntimeError(f"Gemini API error: {e}")


def get_gemini_client():
    """Factory function to create a GeminiClient instance."""
    return GeminiClient()
