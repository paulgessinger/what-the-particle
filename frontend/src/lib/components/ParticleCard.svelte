<script>
  import { createEventDispatcher } from 'svelte';
  import LaTeX from './LaTeX.svelte';
  
  export let particle;
  
  const dispatch = createEventDispatcher();

  function getParticleType(particle) {
    const pdgId = Math.abs(particle.pdgid);
    const name = particle.name.toLowerCase();
    
    // Quarks (PDG IDs 1-6)
    if (pdgId >= 1 && pdgId <= 6) return 'quark';
    
    // Leptons
    if ([11, 13, 15].includes(pdgId)) return 'lepton'; // e, mu, tau
    if ([12, 14, 16].includes(pdgId)) return 'neutrino'; // neutrinos
    
    // Gauge bosons
    if ([21, 22, 23, 24].includes(pdgId)) return 'boson'; // gluon, photon, Z, W
    if (pdgId === 25) return 'higgs'; // Higgs
    
    // Baryons (includes protons, neutrons)
    if (pdgId >= 2212 && pdgId <= 2224) return 'baryon';
    if (pdgId >= 2112 && pdgId <= 2114) return 'baryon';
    
    // Mesons (includes pions, kaons)
    if ((pdgId >= 111 && pdgId <= 331) || (pdgId >= 211 && pdgId <= 223)) return 'meson';
    
    // Fallback based on name
    if (name.includes('pi')) return 'meson';
    if (name.includes('kaon') || name.includes('k')) return 'meson';
    
    return 'particle';
  }

  function getWikipediaUrl(particle) {
    const pdgId = Math.abs(particle.pdgid);
    const descriptiveName = particle.descriptive_name?.toLowerCase();
    
    // Mapping of particles to their Wikipedia URLs
    const wikipediaMap = {
      // Leptons
      11: "https://en.wikipedia.org/wiki/Electron",
      13: "https://en.wikipedia.org/wiki/Muon", 
      15: "https://en.wikipedia.org/wiki/Tau_(particle)",
      12: "https://en.wikipedia.org/wiki/Electron_neutrino",
      14: "https://en.wikipedia.org/wiki/Muon_neutrino",
      16: "https://en.wikipedia.org/wiki/Tau_neutrino",
      
      // Quarks
      1: "https://en.wikipedia.org/wiki/Down_quark",
      2: "https://en.wikipedia.org/wiki/Up_quark",
      3: "https://en.wikipedia.org/wiki/Strange_quark",
      4: "https://en.wikipedia.org/wiki/Charm_quark",
      5: "https://en.wikipedia.org/wiki/Bottom_quark",
      6: "https://en.wikipedia.org/wiki/Top_quark",
      
      // Gauge bosons
      21: "https://en.wikipedia.org/wiki/Gluon",
      22: "https://en.wikipedia.org/wiki/Photon",
      23: "https://en.wikipedia.org/wiki/W_and_Z_bosons",
      24: "https://en.wikipedia.org/wiki/W_and_Z_bosons",
      25: "https://en.wikipedia.org/wiki/Higgs_boson",
      
      // Baryons
      2212: "https://en.wikipedia.org/wiki/Proton",
      2112: "https://en.wikipedia.org/wiki/Neutron",
      
      // Mesons
      111: "https://en.wikipedia.org/wiki/Pion",
      211: "https://en.wikipedia.org/wiki/Pion",
      321: "https://en.wikipedia.org/wiki/Kaon",
      311: "https://en.wikipedia.org/wiki/Kaon",
      130: "https://en.wikipedia.org/wiki/Kaon",
      310: "https://en.wikipedia.org/wiki/Kaon",
    };
    
    return wikipediaMap[pdgId] || null;
  }

  function isStable(particle) {
    // A particle is considered stable if:
    // 1. Width is exactly 0 (or null/undefined), AND
    // 2. Lifetime is infinite (or null/undefined)
    const width = particle.width;
    const lifetime = particle.lifetime;
    
    // Check if width is exactly zero
    const hasZeroWidth = width === 0;
    
    // Check if lifetime is infinite or undefined (stable)
    const hasInfiniteLifetime = lifetime === null || lifetime === undefined || lifetime === Infinity;
    
    return hasZeroWidth && hasInfiniteLifetime;
  }

  function formatScientificLatex(value, precision = 3) {
    if (value === null || value === undefined) return 'Unknown';
    if (value === 0) return '0';
    
    const exp = value.toExponential(precision);
    const match = exp.match(/^(-?\d\.?\d*)e([+-]?\d+)$/);
    if (match) {
      const [, mantissa, exponent] = match;
      const cleanMantissa = parseFloat(mantissa).toString();
      const cleanExponent = parseInt(exponent).toString();
      return `${cleanMantissa} \\times 10^{${cleanExponent}}`;
    }
    return exp;
  }

  function formatMassWithUnit(mass) {
    if (mass === null || mass === undefined) return { value: 'Unknown', unit: '', isLatex: false };
    if (mass === 0) return { value: '0', unit: 'MeV', isLatex: false };
    
    // Use GeV for masses >= 1000 MeV
    if (Math.abs(mass) >= 1000) {
      const gev = mass / 1000;
      if (Math.abs(gev) < 0.001 || Math.abs(gev) > 10000) {
        return { value: formatScientificLatex(gev), unit: 'GeV', isLatex: true };
      }
      return { value: gev.toFixed(gev >= 100 ? 1 : 3), unit: 'GeV', isLatex: false };
    }
    
    // Use MeV for smaller masses
    if (Math.abs(mass) < 0.001 || Math.abs(mass) > 10000) {
      return { value: formatScientificLatex(mass), unit: 'MeV', isLatex: true };
    }
    return { value: mass.toFixed(mass >= 100 ? 2 : 6), unit: 'MeV', isLatex: false };
  }

  function formatMass(mass) {
    const formatted = formatMassWithUnit(mass);
    return formatted.value;
  }

  function formatLifetime(lifetime) {
    if (lifetime === null || lifetime === undefined) return 'Unknown';
    if (lifetime === Infinity || lifetime === -1) return 'Stable';
    return formatScientificLatex(lifetime);
  }

  function formatCharge(charge, threeCharge) {
    if (charge === null || charge === undefined) return 'Unknown';
    if (charge === 0) return '0';
    
    // Use three-charge parameter for exact fractional charges
    if (threeCharge !== null && threeCharge !== undefined) {
      const sign = threeCharge < 0 ? '-' : '';
      const abs_three_charge = Math.abs(threeCharge);
      
      if (abs_three_charge === 1) {
        return `${sign}\\frac{1}{3}`;
      } else if (abs_three_charge === 2) {
        return `${sign}\\frac{2}{3}`;
      } else if (abs_three_charge === 3) {
        return `${sign}1`;
      } else if (abs_three_charge === 6) {
        return `${sign}2`;
      } else if (abs_three_charge === 9) {
        return `${sign}3`;
      }
    }
    
    // For other values, round to reasonable precision
    return charge.toFixed(3);
  }

  function formatNumber(value) {
    if (value === null || value === undefined) return 'Unknown';
    if (value === 0) return '0';
    
    // For integers, show as-is
    if (Number.isInteger(value)) {
      return value.toString();
    }
    
    // For decimals, use reasonable precision
    if (Math.abs(value) < 0.001 || Math.abs(value) > 10000) {
      return formatScientificLatex(value);
    }
    
    return value.toFixed(3);
  }

  $: particleType = getParticleType(particle);
  
  function handleAntiparticleClick() {
    if (particle.anti_particle_pdgid && particle.anti_particle_pdgid !== particle.pdgid) {
      dispatch('antiparticleClick', { 
        pdgid: particle.anti_particle_pdgid,
        name: particle.anti_particle_name
      });
    }
  }
</script>

<div class="card animate-slide-up">
  <div class="flex items-start justify-between mb-6">
    <div class="flex items-center space-x-4">
      <div class="w-16 h-16 bg-gradient-to-br from-primary-500 to-purple-600 rounded-xl flex items-center justify-center text-white text-2xl font-bold">
        {particle.pdgid}
      </div>
      <div>
        <div class="flex items-center space-x-3">
          <h2 class="text-2xl font-bold text-gray-900">{particle.name}</h2>
          {#if getWikipediaUrl(particle)}
            <a 
              href={getWikipediaUrl(particle)} 
              target="_blank" 
              rel="noopener noreferrer"
              class="text-blue-600 hover:text-blue-800 transition-colors duration-200 text-sm font-medium"
              title="View on Wikipedia"
            >
              Wikipedia
            </a>
          {/if}
        </div>
        {#if particle.descriptive_name && particle.descriptive_name !== particle.name}
          <div class="text-lg text-gray-600 mt-1">
            {particle.descriptive_name}
          </div>
        {/if}
        {#if particle.latex_name && particle.latex_name !== particle.name}
          <div class="text-lg text-gray-600 mt-1">
            <LaTeX math={particle.latex_name} className="text-lg" />
          </div>
        {/if}
        <div class="flex items-center space-x-2 mt-2">
          <span class="particle-badge particle-{particleType}">
            Category: {particleType.charAt(0).toUpperCase() + particleType.slice(1)}
          </span>
          {#if isStable(particle)}
            <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
              Stable
            </span>
          {:else}
            <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-orange-100 text-orange-800">
              Unstable
            </span>
          {/if}
        </div>
      </div>
    </div>
  </div>

  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <!-- Basic Properties -->
    <div class="space-y-4">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">Basic Properties</h3>

      <div class="space-y-3">
        <div class="flex justify-between items-center py-2 border-b border-gray-200">
          <span class="text-gray-600">PDG ID</span>
          <span class="font-mono font-semibold text-gray-900">
            <LaTeX math={formatNumber(particle.pdgid)} />
          </span>
        </div>

        <div class="flex justify-between items-center py-2 border-b border-gray-200">
          <span class="text-gray-600">Electric Charge</span>
          <span class="font-mono font-semibold text-gray-900">
            <LaTeX math={formatCharge(particle.charge, particle.three_charge)} /> e
          </span>
        </div>

        {#if particle.three_charge !== null}
          <div class="flex justify-between items-center py-2 border-b border-gray-200">
            <span class="text-gray-600">Three-Charge</span>
            <span class="font-mono font-semibold text-gray-900">
              <LaTeX math={formatNumber(particle.three_charge)} />
            </span>
          </div>
        {/if}

        {#if particle.spin !== null}
          <div class="flex justify-between items-center py-2 border-b border-gray-200">
            <span class="text-gray-600">Spin</span>
            <span class="font-mono font-semibold text-gray-900">
              <LaTeX math={formatNumber(particle.spin)} />
            </span>
          </div>
        {/if}
      </div>
    </div>

    <!-- Mass and Energy -->
    <div class="space-y-4">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">Mass & Energy</h3>

      <div class="space-y-3">
        <div class="flex justify-between items-center py-2 border-b border-gray-200">
          <span class="text-gray-600">Mass</span>
          <span class="font-mono font-semibold text-gray-900">
            <LaTeX math={formatMassWithUnit(particle.mass).value} /> {formatMassWithUnit(particle.mass).unit}/c²
          </span>
        </div>

        {#if particle.width !== null}
          <div class="flex justify-between items-center py-2 border-b border-gray-200">
            <span class="text-gray-600">Width</span>
            <span class="font-mono font-semibold text-gray-900">
              <LaTeX math={formatMassWithUnit(particle.width).value} /> {formatMassWithUnit(particle.width).unit}
            </span>
          </div>
        {/if}

        {#if particle.lifetime !== null}
          <div class="flex justify-between items-center py-2 border-b border-gray-200">
            <span class="text-gray-600">Lifetime</span>
            <span class="font-mono font-semibold text-gray-900">
              <LaTeX math={formatLifetime(particle.lifetime)} /> s
            </span>
          </div>
        {/if}

        {#if particle.ctau !== null && particle.ctau !== 0}
          <div class="flex justify-between items-center py-2 border-b border-gray-200">
            <span class="text-gray-600">cτ (decay length)</span>
            <span class="font-mono font-semibold text-gray-900">
              <LaTeX math={formatNumber(particle.ctau)} /> mm
            </span>
          </div>
        {/if}
      </div>
    </div>
  </div>

  <!-- Quantum Numbers -->
  {#if particle.parity !== null || particle.c_parity !== null || particle.g_parity !== null}
    <div class="mt-8">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">Quantum Numbers</h3>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {#if particle.parity !== null}
          <div class="bg-gray-50 rounded-lg p-4 text-center">
            <div class="text-sm text-gray-600 mb-1">Parity</div>
            <div class="text-xl font-bold text-gray-900">{particle.parity > 0 ? '+' : '-'}</div>
          </div>
        {/if}

        {#if particle.c_parity !== null}
          <div class="bg-gray-50 rounded-lg p-4 text-center">
            <div class="text-sm text-gray-600 mb-1">C-Parity</div>
            <div class="text-xl font-bold text-gray-900">{particle.c_parity > 0 ? '+' : '-'}</div>
          </div>
        {/if}

        {#if particle.g_parity !== null}
          <div class="bg-gray-50 rounded-lg p-4 text-center">
            <div class="text-sm text-gray-600 mb-1">G-Parity</div>
            <div class="text-xl font-bold text-gray-900">{particle.g_parity > 0 ? '+' : '-'}</div>
          </div>
        {/if}
      </div>
    </div>
  {/if}

  <!-- Antiparticle -->
  {#if particle.anti_particle_pdgid !== null && particle.anti_particle_pdgid !== particle.pdgid}
    <div class="mt-8">
      <button 
        on:click={handleAntiparticleClick}
        class="w-full p-4 bg-blue-50 rounded-lg border border-blue-200 hover:bg-blue-100 transition-colors duration-200 cursor-pointer group"
      >
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div class="text-left">
              <div class="text-sm font-medium text-blue-800">Antiparticle</div>
              {#if particle.anti_particle_name}
                <div class="text-blue-600 font-medium">{particle.anti_particle_name}</div>
              {/if}
              <div class="text-blue-600 text-sm">PDG ID: {particle.anti_particle_pdgid}</div>
            </div>
          </div>
          <svg class="w-5 h-5 text-blue-600 group-hover:translate-x-1 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </div>
      </button>
    </div>
  {/if}

</div>
