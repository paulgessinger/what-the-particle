<script>
  import { createEventDispatcher } from 'svelte';
  import LaTeX from './LaTeX.svelte';

  export let particles = [];

  const dispatch = createEventDispatcher();

  function handleParticleClick(particle) {
    dispatch('particleClick', particle);
  }

  function getParticleEmoji(name) {
    const lowerName = name.toLowerCase();
    if (lowerName.includes('electron')) return '🔵';
    if (lowerName.includes('muon')) return '🟣';
    if (lowerName.includes('photon')) return '💡';
    if (lowerName.includes('proton')) return '🔴';
    if (lowerName.includes('neutron')) return '⚪';
    if (lowerName.includes('pion')) return '🟠';
    if (lowerName.includes('quark')) return '🟦';
    return '⚛️';
  }

  function formatMassShort(mass) {
    if (mass === null || mass === undefined) return { value: '', unit: '', isLatex: false };
    if (mass === 0) return { value: '0', unit: 'MeV', isLatex: false };
    
    if (Math.abs(mass) < 1) {
      return { value: (mass * 1000).toFixed(1), unit: 'keV', isLatex: false };
    }
    if (Math.abs(mass) > 1000) {
      return { value: (mass / 1000).toFixed(1), unit: 'GeV', isLatex: false };
    }
    return { value: mass.toFixed(1), unit: 'MeV', isLatex: false };
  }

  function formatCharge(charge, threeCharge) {
    if (charge === null || charge === undefined) return '';
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
</script>

<div class="card">
  <h3 class="text-lg font-semibold text-gray-900 mb-4 flex items-center space-x-2">
    <svg class="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
    </svg>
    <span>Popular Particles</span>
  </h3>

  {#if particles.length === 0}
    <div class="flex items-center justify-center py-8">
      <div class="animate-spin w-6 h-6 border-2 border-primary-600 border-t-transparent rounded-full"></div>
    </div>
  {:else}
    <div class="space-y-2">
      {#each particles as particle}
        <button
          on:click={() => handleParticleClick(particle)}
          class="w-full p-3 rounded-lg bg-gray-50 hover:bg-gray-100 transition-colors duration-200 text-left group"
        >
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <span class="text-lg">{getParticleEmoji(particle.name)}</span>
              <div>
                <div class="font-medium text-gray-900 group-hover:text-primary-600">
                  {particle.name}
                </div>
                <div class="text-xs text-gray-500 font-mono">
                  PDG: <LaTeX math={particle.pdgid.toString()} />
                </div>
              </div>
            </div>
            <div class="text-right">
              {#if particle.mass !== null}
                <div class="text-xs text-gray-600 font-mono">
                  <LaTeX math={formatMassShort(particle.mass).value} /> {formatMassShort(particle.mass).unit}
                </div>
              {/if}
              {#if particle.charge !== null}
                <div class="text-xs text-gray-500">
                  Q: <LaTeX math={formatCharge(particle.charge, particle.three_charge)} />e
                </div>
              {/if}
            </div>
          </div>
        </button>
      {/each}
    </div>

    <div class="mt-6 pt-4 border-t border-gray-200">
      <p class="text-xs text-gray-500 text-center">
        Click any particle to view detailed information
      </p>
    </div>
  {/if}
</div>
