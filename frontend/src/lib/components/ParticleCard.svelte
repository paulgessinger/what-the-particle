<script>
  export let particle;
  
  function getParticleType(name) {
    const lowerName = name.toLowerCase();
    if (lowerName.includes('electron') || lowerName.includes('e-') || lowerName.includes('e+')) return 'electron';
    if (lowerName.includes('muon') || lowerName.includes('mu')) return 'muon';
    if (lowerName.includes('photon') || lowerName.includes('gamma')) return 'photon';
    if (lowerName.includes('proton') || lowerName.includes('p+')) return 'proton';
    if (lowerName.includes('neutron') || lowerName.includes('n0')) return 'neutron';
    if (lowerName.includes('pion') || lowerName.includes('pi')) return 'pion';
    return 'default';
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
  
  $: particleType = getParticleType(particle.name);
</script>

<div class="card animate-slide-up">
  <div class="flex items-start justify-between mb-6">
    <div class="flex items-center space-x-4">
      <div class="w-16 h-16 bg-gradient-to-br from-primary-500 to-purple-600 rounded-xl flex items-center justify-center text-white text-2xl font-bold">
        {particle.pdgid}
      </div>
      <div>
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white">{particle.name}</h2>
        {#if particle.latex_name && particle.latex_name !== particle.name}
          <p class="text-lg text-gray-600 dark:text-gray-400 font-mono">{particle.latex_name}</p>
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
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Basic Properties</h3>
      
      <div class="space-y-3">
        <div class="flex justify-between items-center py-2 border-b border-gray-200 dark:border-gray-700">
          <span class="text-gray-600 dark:text-gray-400">PDG ID</span>
          <span class="font-mono font-semibold text-gray-900 dark:text-white">{particle.pdgid}</span>
        </div>
        
        <div class="flex justify-between items-center py-2 border-b border-gray-200 dark:border-gray-700">
          <span class="text-gray-600 dark:text-gray-400">Electric Charge</span>
          <span class="font-mono font-semibold text-gray-900 dark:text-white">{formatCharge(particle.charge)} e</span>
        </div>
        
        {#if particle.three_charge !== null}
          <div class="flex justify-between items-center py-2 border-b border-gray-200 dark:border-gray-700">
            <span class="text-gray-600 dark:text-gray-400">Three-Charge</span>
            <span class="font-mono font-semibold text-gray-900 dark:text-white">{particle.three_charge}</span>
          </div>
        {/if}
        
        {#if particle.spin !== null}
          <div class="flex justify-between items-center py-2 border-b border-gray-200 dark:border-gray-700">
            <span class="text-gray-600 dark:text-gray-400">Spin</span>
            <span class="font-mono font-semibold text-gray-900 dark:text-white">{particle.spin}</span>
          </div>
        {/if}
      </div>
    </div>

    <!-- Mass and Energy -->
    <div class="space-y-4">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Mass & Energy</h3>
      
      <div class="space-y-3">
        <div class="flex justify-between items-center py-2 border-b border-gray-200 dark:border-gray-700">
          <span class="text-gray-600 dark:text-gray-400">Mass</span>
          <span class="font-mono font-semibold text-gray-900 dark:text-white">{formatMass(particle.mass)} MeV/c²</span>
        </div>
        
        {#if particle.width !== null}
          <div class="flex justify-between items-center py-2 border-b border-gray-200 dark:border-gray-700">
            <span class="text-gray-600 dark:text-gray-400">Width</span>
            <span class="font-mono font-semibold text-gray-900 dark:text-white">{formatMass(particle.width)} MeV</span>
          </div>
        {/if}
        
        {#if particle.lifetime !== null}
          <div class="flex justify-between items-center py-2 border-b border-gray-200 dark:border-gray-700">
            <span class="text-gray-600 dark:text-gray-400">Lifetime</span>
            <span class="font-mono font-semibold text-gray-900 dark:text-white">{formatLifetime(particle.lifetime)} s</span>
          </div>
        {/if}
        
        {#if particle.ctau !== null && particle.ctau !== 0}
          <div class="flex justify-between items-center py-2 border-b border-gray-200 dark:border-gray-700">
            <span class="text-gray-600 dark:text-gray-400">cτ (decay length)</span>
            <span class="font-mono font-semibold text-gray-900 dark:text-white">{formatMass(particle.ctau)} mm</span>
          </div>
        {/if}
      </div>
    </div>
  </div>

  <!-- Quantum Numbers -->
  {#if particle.parity !== null || particle.c_parity !== null || particle.g_parity !== null}
    <div class="mt-8">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Quantum Numbers</h3>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {#if particle.parity !== null}
          <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4 text-center">
            <div class="text-sm text-gray-600 dark:text-gray-400 mb-1">Parity</div>
            <div class="text-xl font-bold text-gray-900 dark:text-white">{particle.parity > 0 ? '+' : '-'}</div>
          </div>
        {/if}
        
        {#if particle.c_parity !== null}
          <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4 text-center">
            <div class="text-sm text-gray-600 dark:text-gray-400 mb-1">C-Parity</div>
            <div class="text-xl font-bold text-gray-900 dark:text-white">{particle.c_parity > 0 ? '+' : '-'}</div>
          </div>
        {/if}
        
        {#if particle.g_parity !== null}
          <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4 text-center">
            <div class="text-sm text-gray-600 dark:text-gray-400 mb-1">G-Parity</div>
            <div class="text-xl font-bold text-gray-900 dark:text-white">{particle.g_parity > 0 ? '+' : '-'}</div>
          </div>
        {/if}
      </div>
    </div>
  {/if}

  <!-- Antiparticle -->
  {#if particle.anti_particle_pdgid !== null && particle.anti_particle_pdgid !== particle.pdgid}
    <div class="mt-8 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
      <div class="flex items-center space-x-3">
        <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <div>
          <div class="text-sm font-medium text-blue-800 dark:text-blue-200">Antiparticle</div>
          <div class="text-blue-600 dark:text-blue-300">PDG ID: {particle.anti_particle_pdgid}</div>
        </div>
      </div>
    </div>
  {/if}

  <!-- Status -->
  {#if particle.status}
    <div class="mt-6 text-sm text-gray-500 dark:text-gray-400">
      Status: {particle.status}
    </div>
  {/if}
</div>