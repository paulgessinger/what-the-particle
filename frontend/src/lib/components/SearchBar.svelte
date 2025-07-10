<script>
  import { createEventDispatcher } from 'svelte';
  
  export let searchQuery = '';
  export let loading = false;
  
  const dispatch = createEventDispatcher();
  
  function handleSubmit() {
    const pdgId = parseInt(searchQuery.trim());
    if (isNaN(pdgId)) {
      return;
    }
    dispatch('search', { pdgId });
  }
  
  function handleKeydown(event) {
    if (event.key === 'Enter') {
      handleSubmit();
    }
  }
  
  $: isValidPdgId = searchQuery.trim() !== '' && !isNaN(parseInt(searchQuery.trim()));
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
      placeholder="Enter PDG ID (e.g., 11 for electron, 2212 for proton)"
      class="input-field pl-12 pr-24 text-lg h-14"
      disabled={loading}
    />
    
    <div class="absolute inset-y-0 right-0 flex items-center pr-3">
      <button
        on:click={handleSubmit}
        disabled={!isValidPdgId || loading}
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
  
  {#if searchQuery.trim() !== '' && !isValidPdgId}
    <p class="mt-2 text-sm text-red-600 dark:text-red-400">Please enter a valid numeric PDG ID</p>
  {/if}
  
  <div class="mt-4 text-center">
    <p class="text-sm text-gray-500 dark:text-gray-400">
      Don't know PDG IDs? Try some examples: 
      <button on:click={() => {searchQuery = '11'; handleSubmit();}} class="text-primary-600 hover:text-primary-700 font-medium">11</button>,
      <button on:click={() => {searchQuery = '2212'; handleSubmit();}} class="text-primary-600 hover:text-primary-700 font-medium">2212</button>,
      <button on:click={() => {searchQuery = '22'; handleSubmit();}} class="text-primary-600 hover:text-primary-700 font-medium">22</button>, or
      <button on:click={() => {searchQuery = '211'; handleSubmit();}} class="text-primary-600 hover:text-primary-700 font-medium">211</button>
    </p>
  </div>
</div>