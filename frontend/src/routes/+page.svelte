<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { base } from '$app/paths';
  import SearchBar from '../lib/components/SearchBar.svelte';
  import PopularParticles from '../lib/components/PopularParticles.svelte';

  let searchQuery = '';
  let loading = false;
  let error = null;
  let popularParticles = [];
  let nameMapping = null;

  onMount(async () => {
    // Load popular particles and name mapping on mount
    try {
      const [popularResponse, nameMappingResponse] = await Promise.all([
        fetch(`${base}/particles/popular.json`),
        fetch(`${base}/particles/name-mapping.json`)
      ]);
      
      if (popularResponse.ok) {
        const popularData = await popularResponse.json();
        popularParticles = popularData.particles;
      } else {
        console.error('Failed to load popular particles');
      }
      
      if (nameMappingResponse.ok) {
        nameMapping = await nameMappingResponse.json();
      } else {
        console.error('Failed to load name mapping');
      }
    } catch (err) {
      console.error('Failed to load data:', err);
    }
  });

  function handleSearch(event) {
    if (event.detail.pdgId) {
      goto(`${base}/pdgid/${event.detail.pdgId}`);
    } else if (event.detail.textQuery) {
      searchParticleByText(event.detail.textQuery);
    }
  }

  async function searchParticleByText(query) {
    if (!query || !nameMapping) return;

    loading = true;
    error = null;

    try {
      const queryLower = query.toLowerCase().trim();
      
      // Check for exact match first
      let pdgIds = nameMapping[queryLower];
      
      // If no exact match, try fuzzy matching
      if (!pdgIds) {
        const searchKeys = Object.keys(nameMapping);
        const fuzzyMatch = searchKeys.find(key => 
          key.includes(queryLower) || queryLower.includes(key)
        );
        if (fuzzyMatch) {
          pdgIds = nameMapping[fuzzyMatch];
        }
      }
      
      if (pdgIds && pdgIds.length > 0) {
        // If we get results, navigate to the first one with search parameter
        goto(`${base}/pdgid/${pdgIds[0]}?search=${encodeURIComponent(query)}`);
      } else {
        error = `No particles found matching "${query}"`;
        loading = false;
      }
    } catch (err) {
      error = 'Failed to search particles';
      loading = false;
    }
  }

  function handlePopularParticleClick(particle) {
    // Use descriptive name if available, otherwise PDG ID
    const searchTerm = particle.descriptive_name && particle.descriptive_name !== particle.name 
      ? particle.descriptive_name 
      : particle.pdgid.toString();
    goto(`${base}/pdgid/${particle.pdgid}?search=${encodeURIComponent(searchTerm)}`);
  }
</script>

<svelte:head>
  <title>Particle Explorer - Discover Fundamental Particles</title>
  <meta name="description" content="Explore the world of particle physics. Search for particles by PDG ID and discover their properties, masses, charges, and more." />
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
  <!-- Hero Section -->
  <div class="relative overflow-hidden">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
      <div class="text-center">
        <h1 class="text-4xl md:text-6xl font-bold text-gray-900 mb-6 animate-fade-in">
          Explore the <span class="bg-gradient-to-r from-primary-600 to-purple-600 bg-clip-text text-transparent">Quantum Universe</span>
        </h1>
        <p class="text-xl text-gray-600 mb-12 max-w-3xl mx-auto animate-fade-in">
          Discover fundamental particles using PDG IDs. Search through the complete database of quarks, leptons, bosons, and more with detailed physics properties.
        </p>

        <!-- Search Interface -->
        <div class="max-w-2xl mx-auto mb-16 animate-slide-up">
          <SearchBar bind:searchQuery on:search={handleSearch} {loading} />
        </div>
      </div>
    </div>

    <!-- Floating particles background -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-1/4 left-1/4 w-2 h-2 bg-primary-400 rounded-full animate-pulse-subtle"></div>
      <div class="absolute top-1/3 right-1/3 w-3 h-3 bg-purple-400 rounded-full animate-pulse-subtle" style="animation-delay: 0.5s;"></div>
      <div class="absolute bottom-1/4 left-1/3 w-1 h-1 bg-blue-400 rounded-full animate-pulse-subtle" style="animation-delay: 1s;"></div>
      <div class="absolute bottom-1/3 right-1/4 w-2 h-2 bg-green-400 rounded-full animate-pulse-subtle" style="animation-delay: 1.5s;"></div>
    </div>
  </div>

  <!-- Main Content -->
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Main Content Area -->
      <div class="lg:col-span-2 lg:order-1 order-2">
        {#if loading}
          <div class="card text-center py-12">
            <div class="animate-spin w-8 h-8 border-4 border-primary-600 border-t-transparent rounded-full mx-auto mb-4"></div>
            <p class="text-gray-600">Searching particle database...</p>
          </div>
        {:else if error}
          <div class="card border-red-200 bg-red-50">
            <div class="flex items-center space-x-3">
              <div class="flex-shrink-0">
                <svg class="w-6 h-6 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <h3 class="text-lg font-medium text-red-800">Particle Not Found</h3>
                <p class="text-red-600">{error}</p>
              </div>
            </div>
          </div>
        {:else}
          <div class="card text-center py-8 md:py-12">
            <div class="text-4xl md:text-6xl mb-3 md:mb-4">🔍</div>
            <h3 class="text-lg md:text-xl font-semibold text-gray-900 mb-2">Search for a Particle</h3>
            <p class="text-gray-600 mb-4 md:mb-6 text-sm md:text-base">Enter a PDG ID above to discover detailed particle information</p>
            <div class="grid grid-cols-1 md:grid-cols-4 gap-2 md:gap-4 text-xs md:text-sm text-gray-500">
              <div class="md:col-span-1">
                <span class="font-medium">Examples:</span>
              </div>
              <div>11 (electron)</div>
              <div>2212 (proton)</div>
              <div>22 (photon)</div>
            </div>
          </div>
        {/if}
      </div>

      <!-- Popular Particles Sidebar -->
      <div class="lg:col-span-1 lg:order-2 order-1 hidden lg:block">
        <PopularParticles
          particles={popularParticles}
          on:particleClick={(e) => handlePopularParticleClick(e.detail)}
        />
      </div>
    </div>
  </div>
</div>
