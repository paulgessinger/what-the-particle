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

  function formatMass(mass) {
    if (mass === null || mass === undefined) return 'Unknown';
    if (mass === 0) return '0';
    // Convert to scientific notation for very small or large numbers
    if (Math.abs(mass) < 0.001 || Math.abs(mass) > 10000) {
      return mass.toExponential(3);
    }
    return mass.toFixed(6);
  }

  function formatLifetime(lifetime) {
    if (lifetime === null || lifetime === undefined) return 'Unknown';
    if (lifetime === Infinity || lifetime === -1) return 'Stable';
    return lifetime.toExponential(3);
  }

  function formatCharge(charge) {
    if (charge === null || charge === undefined) return 'Unknown';
    if (charge === 0) return '0';
    if (charge === 1) return '+1';
    if (charge === -1) return '-1';
    return charge > 0 ? `+${charge}` : charge.toString();
  }

  $: particleType = getParticleType(particle);
  
  function handleAntiparticleClick() {
    if (particle.anti_particle_pdgid && particle.anti_particle_pdgid !== particle.pdgid) {
      dispatch('antiparticleClick', { pdgid: particle.anti_particle_pdgid });
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
        <h2 class="text-2xl font-bold text-gray-900">{particle.name}</h2>
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
        <span class="particle-badge particle-{particleType} mt-2">
          {particleType.charAt(0).toUpperCase() + particleType.slice(1)}
        </span>
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
          <span class="font-mono font-semibold text-gray-900">{particle.pdgid}</span>
        </div>

        <div class="flex justify-between items-center py-2 border-b border-gray-200">
          <span class="text-gray-600">Electric Charge</span>
          <span class="font-mono font-semibold text-gray-900">{formatCharge(particle.charge)} e</span>
        </div>

        {#if particle.three_charge !== null}
          <div class="flex justify-between items-center py-2 border-b border-gray-200">
            <span class="text-gray-600">Three-Charge</span>
            <span class="font-mono font-semibold text-gray-900">{particle.three_charge}</span>
          </div>
        {/if}

        {#if particle.spin !== null}
          <div class="flex justify-between items-center py-2 border-b border-gray-200">
            <span class="text-gray-600">Spin</span>
            <span class="font-mono font-semibold text-gray-900">{particle.spin}</span>
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
          <span class="font-mono font-semibold text-gray-900">{formatMass(particle.mass)} MeV/c²</span>
        </div>

        {#if particle.width !== null}
          <div class="flex justify-between items-center py-2 border-b border-gray-200">
            <span class="text-gray-600">Width</span>
            <span class="font-mono font-semibold text-gray-900">{formatMass(particle.width)} MeV</span>
          </div>
        {/if}

        {#if particle.lifetime !== null}
          <div class="flex justify-between items-center py-2 border-b border-gray-200">
            <span class="text-gray-600">Lifetime</span>
            <span class="font-mono font-semibold text-gray-900">{formatLifetime(particle.lifetime)} s</span>
          </div>
        {/if}

        {#if particle.ctau !== null && particle.ctau !== 0}
          <div class="flex justify-between items-center py-2 border-b border-gray-200">
            <span class="text-gray-600">cτ (decay length)</span>
            <span class="font-mono font-semibold text-gray-900">{formatMass(particle.ctau)} mm</span>
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
              <div class="text-blue-600">PDG ID: {particle.anti_particle_pdgid}</div>
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
