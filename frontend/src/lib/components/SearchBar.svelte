<script>
  import { createEventDispatcher } from 'svelte';

  export let searchQuery = '';
  export let loading = false;

  const dispatch = createEventDispatcher();

  function handleSubmit() {
    const query = searchQuery.trim();
    if (!query) {
      return;
    }
    
    // Check if it's a numeric PDG ID
    const pdgId = parseInt(query);
    if (!isNaN(pdgId)) {
      dispatch('search', { pdgId });
    } else {
      // Text search
      dispatch('search', { textQuery: query });
    }
  }

  function handleKeydown(event) {
    if (event.key === 'Enter') {
      handleSubmit();
    }
  }

  $: isValidSearch = searchQuery.trim() !== '';
</script>

<div class="w-full">
  <div class="relative">
    <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
      <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
      </svg>
    </div>

    <input
      type="text"
      bind:value={searchQuery}
      on:keydown={handleKeydown}
      placeholder="Enter particle name or PDG ID (e.g., 'electron', 'muon', or '11', '2212')"
      class="input-field pl-12 pr-24 text-lg h-14"
      disabled={loading}
    />

    <div class="absolute inset-y-0 right-0 flex items-center pr-3">
      <button
        on:click={handleSubmit}
        disabled={!isValidSearch || loading}
        class="btn-primary px-6 h-10 text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
      >
        {#if loading}
          <div class="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full"></div>
          <span>Searching...</span>
        {:else}
          <span>Search</span>
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
          </svg>
        {/if}
      </button>
    </div>
  </div>


  <div class="mt-4 text-center">
    <p class="text-sm text-gray-500 dark:text-gray-400">
      Try searching by name:
      <button on:click={() => {searchQuery = 'electron'; handleSubmit();}} class="text-primary-600 hover:text-primary-700 font-medium">electron</button>,
      <button on:click={() => {searchQuery = 'muon'; handleSubmit();}} class="text-primary-600 hover:text-primary-700 font-medium">muon</button>,
      <button on:click={() => {searchQuery = 'proton'; handleSubmit();}} class="text-primary-600 hover:text-primary-700 font-medium">proton</button>, or by PDG ID:
      <button on:click={() => {searchQuery = '11'; handleSubmit();}} class="text-primary-600 hover:text-primary-700 font-medium">11</button>,
      <button on:click={() => {searchQuery = '2212'; handleSubmit();}} class="text-primary-600 hover:text-primary-700 font-medium">2212</button>
    </p>
  </div>
</div>
