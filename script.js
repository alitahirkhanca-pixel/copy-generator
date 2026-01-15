// ============================================
// Email Copy Automation - Frontend
// ============================================

// API URL - use same origin since backend serves both API and frontend
const API_URL = '/api';

// State Management
const state = {
    step: 0,
    data: {
        onboarding: { clientName: '', industry: '', audience: '' },
        website: '',
        strategy: ''
    },
    variations: [],         // Stores the 4 generated variations
    activeVariation: 0      // Currently displayed variation index
};

const steps = [
    { title: "Attune", icon: "user" },
    { title: "Aura", icon: "globe" },
    { title: "Imprint", icon: "file-text" },
    { title: "Channel", icon: "sparkles" },
    { title: "Manifest", icon: "check-circle-2" }
];

// DOM Elements
const app = document.getElementById('app');
const header = document.getElementById('progress-header');

// Main Render Function
function render() {
    renderHeader();
    renderStep();
    lucide.createIcons();
}

function renderHeader() {
    if (state.step >= 3) {
        header.classList.add('hidden');
        return;
    }
    header.classList.remove('hidden');

    const progress = (state.step / (steps.length - 2)) * 100;

    const stepsHtml = steps.slice(0, 3).map((s, idx) => {
        const isActive = idx === state.step;
        const isCompleted = idx < state.step;

        let circleClass = 'border-slate-800 bg-slate-900 text-slate-600';
        if (isActive) circleClass = 'border-gold-500 bg-gold-900/20 text-gold-400 scale-110 shadow-[0_0_15px_rgba(212,175,55,0.3)]';
        if (isCompleted) circleClass = 'border-gold-600 bg-gold-600 text-black';

        return `
            <div class="flex flex-col items-center gap-2 relative z-10 px-2 rounded-xl transition-all duration-300">
                <div class="w-10 h-10 rounded-full flex items-center justify-center border-2 transition-all duration-300 ${circleClass}">
                    <i data-lucide="${s.icon}" width="20"></i>
                </div>
                <span class="text-sm font-medium ${isActive ? 'text-white' : 'text-slate-500'}">${s.title}</span>
            </div>
        `;
    }).join('');

    header.innerHTML = `
        <div class="flex justify-between relative">
            <div class="absolute top-1/2 left-0 w-full h-0.5 bg-slate-800 -z-10 rounded-full"></div>
            <div class="absolute top-1/2 left-0 h-0.5 bg-gold-600 -z-10 rounded-full transition-all duration-500 shadow-[0_0_10px_rgba(212,175,55,0.4)]" style="width: ${progress}%"></div>
            ${stepsHtml}
        </div>
    `;
}

function renderStep() {
    app.innerHTML = '';
    const container = document.createElement('div');
    container.className = 'fade-in w-full';

    switch (state.step) {
        case 0:
            container.innerHTML = renderOnboarding();
            break;
        case 1:
            container.innerHTML = renderWebsite();
            break;
        case 2:
            container.innerHTML = renderStrategy();
            break;
        case 3:
            container.innerHTML = renderSynthesis();
            startSynthesis();
            break;
        case 4:
            container.innerHTML = renderResult();
            break;
    }
    app.appendChild(container);
    attachListeners();
}

// ------ Step Renderers ------

function renderOnboarding() {
    const { clientName, industry, audience } = state.data.onboarding;
    const isValid = clientName && industry;

    return `
        <div class="card flex flex-col gap-6">
            <div>
                <h2 class="text-2xl font-bold mb-2 gradient-text">Attune to Client</h2>
                <p class="text-slate-400">Tell us about the entity we're channeling copy for.</p>
            </div>
            <div class="space-y-4">
                <div>
                    <label>Client Name</label>
                    <input type="text" id="input-client" value="${clientName}" placeholder="e.g. Acme Corp" autofocus>
                </div>
                <div>
                    <label>Industry</label>
                    <input type="text" id="input-industry" value="${industry}" placeholder="e.g. SaaS">
                </div>
                <div>
                    <label>Target Audience</label>
                    <input type="text" id="input-audience" value="${audience}" placeholder="e.g. Small Business Owners">
                </div>
            </div>
            <div class="flex justify-end pt-4">
                <button id="btn-next" class="btn-primary" ${!isValid ? 'disabled' : ''}>
                    Continue <i data-lucide="arrow-right" width="18"></i>
                </button>
            </div>
        </div>
    `;
}

function renderWebsite() {
    const val = state.data.website;
    const isValid = val && val.includes('.');

    return `
        <div class="card flex flex-col gap-6">
            <div>
                <h2 class="text-2xl font-bold mb-2 gradient-text">Read Brand Aura</h2>
                <p class="text-slate-400">Enter the URL. We'll sense the brand voice and offerings.</p>
            </div>
            <div class="relative">
                <div class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500">
                    <i data-lucide="link" width="18"></i>
                </div>
                <input type="url" id="input-website" value="${val}" placeholder="https://example.com" class="pl-12" autofocus>
            </div>
            <div class="flex justify-end pt-4">
                <button id="btn-next" class="btn-primary" ${!isValid ? 'disabled' : ''}>
                    Analyze <i data-lucide="arrow-right" width="18"></i>
                </button>
            </div>
        </div>
    `;
}

function renderStrategy() {
    const val = state.data.strategy;
    const isValid = val && val.length > 5;

    return `
        <div class="card flex flex-col gap-6">
            <div>
                <h2 class="text-2xl font-bold mb-2 gradient-text">Psychic Imprint</h2>
                <p class="text-slate-400">Paste your raw thoughts or strategy notes to guide the vision.</p>
            </div>
            <div>
                <textarea id="input-strategy" placeholder="e.g. Focus on summer collection..." class="min-h-[150px] resize-y" autofocus>${val}</textarea>
            </div>
            <div class="flex justify-end pt-4">
                <button id="btn-next" class="btn-primary" ${!isValid ? 'disabled' : ''}>
                    Generate Emails <i data-lucide="arrow-right" width="18"></i>
                </button>
            </div>
        </div>
    `;
}

function renderSynthesis() {
    return `
        <div class="flex flex-col items-center justify-center p-12 text-center">
            <div class="relative w-24 h-24 mb-8">
                <div class="absolute inset-0 bg-gold-500 rounded-full blur-2xl opacity-20 animate-pulse-slow"></div>
                <div class="spinner"></div> 
            </div>
            <h2 class="text-3xl font-bold gradient-text mb-4">Channeling Copy...</h2>
            <p id="synthesis-text" class="text-lg text-gold-200/80 font-medium fade-in">Gazing into the void...</p>
        </div>
    `;
}

function renderResult() {
    const v = state.variations[state.activeVariation];
    if (!v) {
        return `<div class="card text-center text-red-400">No variations generated. Please try again.</div>`;
    }

    const tabsHtml = state.variations.map((variation, idx) => {
        const isActive = idx === state.activeVariation;
        return `
            <button 
                data-tab="${idx}" 
                class="variation-tab px-4 py-2 rounded-lg text-sm font-medium transition-all ${isActive
                ? 'bg-gold-600 text-black shadow-[0_0_15px_rgba(212,175,55,0.3)] font-bold'
                : 'bg-slate-900/50 text-slate-400 hover:bg-slate-800 border border-transparent hover:border-gold-500/30'
            }"
            >
                ${variation.hookType}
            </button>
        `;
    }).join('');

    const fullEmail = `Subject: ${v.subject}

${v.body}

– Your Name
${v.ps}`;

    return `
        <div class="w-full max-w-3xl mx-auto">
            <!-- Header -->
            <div class="flex items-center justify-between mb-6">
                <div class="flex items-center gap-3">
                    <div class="bg-gold-500/10 p-2 rounded-lg text-gold-400 border border-gold-500/20">
                        <i data-lucide="sparkles" width="24"></i>
                    </div>
                    <div>
                        <h2 class="text-xl font-bold text-white">Manifested Realities</h2>
                        <p class="text-sm text-slate-400">4 visions from the future • Click tabs to compare</p>
                    </div>
                </div>
            </div>

            <!-- Variation Tabs -->
            <div class="flex flex-wrap gap-2 mb-6">
                ${tabsHtml}
            </div>

            <!-- Email Card -->
            <div class="card">
                <div class="flex items-center justify-between border-b border-slate-700/50 pb-4 mb-4">
                    <div>
                        <span class="text-xs uppercase tracking-wide text-gold-500 font-bold tracking-widest">${v.hookType}</span>
                        <h3 class="text-lg font-bold text-white mt-1">${v.subject}</h3>
                    </div>
                    <button id="btn-copy" class="btn-primary text-sm py-2 px-3">
                        <i data-lucide="copy" width="16"></i> Copy
                    </button>
                </div>
                
                <div id="copy-content" class="bg-slate-950/50 p-6 rounded-lg border border-slate-800 font-mono text-sm text-slate-300 whitespace-pre-wrap leading-relaxed">
${fullEmail}
                </div>
            </div>

            <!-- Actions -->
            <div class="mt-6 flex gap-3 justify-end">
                <button id="btn-regenerate" class="btn-primary bg-transparent border-slate-700 hover:border-gold-500/50 text-slate-400 hover:text-gold-400">
                    <i data-lucide="refresh-cw" width="18"></i> Re-Roll Destiny
                </button>
                <button class="btn-primary bg-gold-600 border-gold-500 hover:bg-gold-500 text-black shadow-[0_0_20px_rgba(212,175,55,0.2)] font-bold">
                    Export to Reality
                </button>
            </div>
        </div>
    `;
}

// ------ Logic & Listeners ------

function attachListeners() {
    const btnNext = document.getElementById('btn-next');
    if (btnNext) {
        btnNext.addEventListener('click', () => {
            state.step++;
            render();
        });
    }

    if (state.step === 0) {
        const i1 = document.getElementById('input-client');
        const i2 = document.getElementById('input-industry');
        const i3 = document.getElementById('input-audience');

        const update = () => {
            state.data.onboarding.clientName = i1.value;
            state.data.onboarding.industry = i2.value;
            state.data.onboarding.audience = i3.value;
            btnNext.disabled = !i1.value || !i2.value;
        };
        [i1, i2, i3].forEach(el => el.addEventListener('input', update));
    }

    if (state.step === 1) {
        const el = document.getElementById('input-website');
        el.addEventListener('input', (e) => {
            state.data.website = e.target.value;
            btnNext.disabled = !e.target.value.includes('.');
        });
    }

    if (state.step === 2) {
        const el = document.getElementById('input-strategy');
        el.addEventListener('input', (e) => {
            state.data.strategy = e.target.value;
            btnNext.disabled = e.target.value.length < 5;
        });
    }

    if (state.step === 4) {
        // Tab switching
        document.querySelectorAll('.variation-tab').forEach(tab => {
            tab.addEventListener('click', () => {
                state.activeVariation = parseInt(tab.dataset.tab);
                render();
            });
        });

        // Copy button
        const btnCopy = document.getElementById('btn-copy');
        if (btnCopy) {
            btnCopy.addEventListener('click', () => {
                const text = document.getElementById('copy-content').innerText;
                navigator.clipboard.writeText(text);
                btnCopy.innerHTML = `<i data-lucide="check" width="16"></i> Copied`;
                lucide.createIcons();
                setTimeout(() => {
                    btnCopy.innerHTML = `<i data-lucide="copy" width="16"></i> Copy`;
                    lucide.createIcons();
                }, 2000);
            });
        }

        // Regenerate button
        const btnRegen = document.getElementById('btn-regenerate');
        if (btnRegen) {
            btnRegen.addEventListener('click', () => {
                state.step = 3;
                state.variations = [];
                state.activeVariation = 0;
                render();
            });
        }
    }
}

async function startSynthesis() {
    const textEl = document.getElementById('synthesis-text');

    const messages = [
        'Sensing client vibrations...',
        'Consulting the strategy oracles...',
        'Divining the perfect hooks...',
        'Manifesting 4 realities...'
    ];

    // Display progress messages
    for (let i = 0; i < messages.length; i++) {
        await sleep(800);
        if (textEl) textEl.innerText = messages[i];
    }

    // Call backend API
    try {
        const response = await fetch(`${API_URL}/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                clientName: state.data.onboarding.clientName,
                industry: state.data.onboarding.industry,
                audience: state.data.onboarding.audience,
                website: state.data.website,
                strategy: state.data.strategy
            })
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        const data = await response.json();
        state.variations = data.variations;

        if (textEl) textEl.innerText = 'Done!';
        await sleep(500);

        state.step++;
        render();

    } catch (error) {
        console.error('API Error:', error);
        if (textEl) {
            textEl.innerHTML = `<span class="text-red-400">Failed to connect to Copy Engine.</span><br><span class="text-slate-500 text-sm">Make sure the backend is running: python3 backend/app.py</span>`;
        }
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Init
render();
