"""
Hook Types & Angle Database
Based on the 1M Messages copywriting framework.
"""

HOOK_TYPES = {
    "shot_in_the_dark": {
        "name": "Shot in the Dark",
        "description": "Frame it as unlikely but potentially helpful",
        "subject_templates": [
            "Bit of a long shot, but...",
            "Might be totally off base here",
            "Not sure if this even applies to {industry}",
            "This might be irrelevant, but..."
        ],
        "opener_templates": [
            "This might be a total miss, but I noticed {problem} and thought it was worth mentioning.",
            "Long shot here — but if {audience} is a priority, this could be useful.",
            "Not sure if this applies to {client}, but I've seen this issue trip up a lot of {industry} teams."
        ]
    },
    "clarity_gap": {
        "name": "Clarity Gap",
        "description": "Point to what's not obvious or missing",
        "subject_templates": [
            "The part no one talks about",
            "What's actually breaking this",
            "The hidden blocker in {industry}",
            "This usually gets missed"
        ],
        "opener_templates": [
            "Most {audience} don't realize this is what's actually slowing things down.",
            "There's something most {industry} companies overlook when scaling — and it's not what you'd expect.",
            "The surface-level fix rarely works. The real issue is usually deeper."
        ]
    },
    "math_problem": {
        "name": "Math Problem",
        "description": "Show that it's a numbers issue",
        "subject_templates": [
            "The math doesn't add up",
            "When the numbers start lying",
            "This got awkward at $5M",
            "ROAS looks good, but..."
        ],
        "opener_templates": [
            "The metrics look healthy on the surface — but the payback math tells a different story.",
            "Most {industry} companies hit a wall around $X because the unit economics quietly shift.",
            "I've seen this pattern a lot: growth looks solid, but CAC is quietly eating margin."
        ]
    },
    "overlooked_detail": {
        "name": "Overlooked Detail",
        "description": "Zoom in on a specific, overlooked blocker",
        "subject_templates": [
            "One small thing that's costing you",
            "The detail that's quietly breaking this",
            "Buried under 47 follow-ups",
            "This tiny thing is killing conversions"
        ],
        "opener_templates": [
            "There's a small detail in how {client} handles {process} that's likely costing more than it looks.",
            "Zooming in on one specific thing: {specific_issue}. It's small, but it's a surprisingly common leak.",
            "I noticed something in your {process} that most people overlook — but it's a high-leverage fix."
        ]
    },
    "anti_pitch": {
        "name": "Anti-Pitch",
        "description": "Emphasize that it's not a sales push",
        "subject_templates": [
            "Not a pitch — just a thought",
            "No agenda, just noticed this",
            "Happy to leave you alone after this",
            "Quick observation (no ask)"
        ],
        "opener_templates": [
            "Not trying to sell you anything — just noticed something that might be useful.",
            "No pitch here. I saw {observation} and thought it was worth flagging.",
            "This isn't a sales push. Just something I've seen work for other {industry} teams."
        ]
    },
    "status_signaling": {
        "name": "Status Signaling",
        "description": "Mention big logos casually for authority",
        "subject_templates": [
            "What {big_company} figured out",
            "Borrowed this from {big_company}",
            "Seeing this across YC companies",
            "Cozy Earth used this to hit $80M"
        ],
        "opener_templates": [
            "We helped {big_company} solve a similar issue — might be relevant to {client}.",
            "Seeing a pattern across companies like {big_company} and {another_company} in {industry}.",
            "This is something we stumbled on working with teams at {big_company}, {another_company}, etc."
        ]
    }
}

# CTA options (soft, curiosity-based)
CTA_OPTIONS = [
    "Want me to send over a quick breakdown?",
    "Happy to share 3 quick fixes if useful.",
    "Open to a quick call to sketch out what this could look like?",
    "Want a peek at the deck?",
    "Should I send a few examples of what's worked?",
    "Worth a 10-min chat to see if there's a fit?"
]

# P.S. templates (human, witty)
PS_TEMPLATES = [
    "P.S. If this is totally off, feel free to ignore — I won't follow up 37 times.",
    "P.S. No hard feelings if this isn't the right time. Just thought it was worth a shot.",
    "P.S. We've seen this move the needle for {industry} teams, but happy to leave you alone if not.",
    "P.S. Worst case, you have a new contact who actually knows {industry}.",
    "P.S. If you're buried under emails, I get it. Ping me whenever, or never."
]

def get_all_hook_types():
    """Return all hook type keys."""
    return list(HOOK_TYPES.keys())

def get_hook(hook_key):
    """Get a specific hook type by key."""
    return HOOK_TYPES.get(hook_key)
