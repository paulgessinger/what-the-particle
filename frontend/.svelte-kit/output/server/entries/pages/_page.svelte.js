import { c as create_ssr_component, d as createEventDispatcher, f as add_attribute, h as each, e as escape, v as validate_component } from "../../chunks/ssr.js";
const SearchBar = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let isValidPdgId;
  let { searchQuery = "" } = $$props;
  let { loading = false } = $$props;
  createEventDispatcher();
  if ($$props.searchQuery === void 0 && $$bindings.searchQuery && searchQuery !== void 0)
    $$bindings.searchQuery(searchQuery);
  if ($$props.loading === void 0 && $$bindings.loading && loading !== void 0)
    $$bindings.loading(loading);
  isValidPdgId = searchQuery.trim() !== "" && !isNaN(parseInt(searchQuery.trim()));
  return `<div class="w-full"><div class="relative"><div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none" data-svelte-h="svelte-12dtj5x"><svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg></div> <input type="text" placeholder="Enter PDG ID (e.g., 11 for electron, 2212 for proton)" class="input-field pl-12 pr-24 text-lg h-14" ${loading ? "disabled" : ""}${add_attribute("value", searchQuery, 0)}> <div class="absolute inset-y-0 right-0 flex items-center pr-3"><button ${!isValidPdgId || loading ? "disabled" : ""} class="btn-primary px-6 h-10 text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2">${loading ? `<div class="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full"></div> <span data-svelte-h="svelte-1v71xds">Searching...</span>` : `<span data-svelte-h="svelte-iecwuy">Search</span> <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path></svg>`}</button></div></div> ${searchQuery.trim() !== "" && !isValidPdgId ? `<p class="mt-2 text-sm text-red-600 dark:text-red-400" data-svelte-h="svelte-1cnmfnd">Please enter a valid numeric PDG ID</p>` : ``} <div class="mt-4 text-center"><p class="text-sm text-gray-500 dark:text-gray-400">Don&#39;t know PDG IDs? Try some examples: 
      <button class="text-primary-600 hover:text-primary-700 font-medium" data-svelte-h="svelte-7ecxfn">11</button>,
      <button class="text-primary-600 hover:text-primary-700 font-medium" data-svelte-h="svelte-76i4cl">2212</button>,
      <button class="text-primary-600 hover:text-primary-700 font-medium" data-svelte-h="svelte-1g61h5j">22</button>, or
      <button class="text-primary-600 hover:text-primary-700 font-medium" data-svelte-h="svelte-eib2v1">211</button></p></div></div>`;
});
function getParticleEmoji(name) {
  const lowerName = name.toLowerCase();
  if (lowerName.includes("electron"))
    return "🔵";
  if (lowerName.includes("muon"))
    return "🟣";
  if (lowerName.includes("photon"))
    return "💡";
  if (lowerName.includes("proton"))
    return "🔴";
  if (lowerName.includes("neutron"))
    return "⚪";
  if (lowerName.includes("pion"))
    return "🟠";
  if (lowerName.includes("quark"))
    return "🟦";
  return "⚛️";
}
function formatMassShort(mass) {
  if (mass === null || mass === void 0)
    return "";
  if (mass === 0)
    return "0 MeV";
  if (Math.abs(mass) < 1) {
    return `${(mass * 1e3).toFixed(1)} keV`;
  }
  if (Math.abs(mass) > 1e3) {
    return `${(mass / 1e3).toFixed(1)} GeV`;
  }
  return `${mass.toFixed(1)} MeV`;
}
const PopularParticles = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let { particles = [] } = $$props;
  createEventDispatcher();
  if ($$props.particles === void 0 && $$bindings.particles && particles !== void 0)
    $$bindings.particles(particles);
  return `<div class="card"><h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center space-x-2" data-svelte-h="svelte-860tbh"><svg class="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"></path></svg> <span>Popular Particles</span></h3> ${particles.length === 0 ? `<div class="flex items-center justify-center py-8" data-svelte-h="svelte-1e77uth"><div class="animate-spin w-6 h-6 border-2 border-primary-600 border-t-transparent rounded-full"></div></div>` : `<div class="space-y-2">${each(particles, (particle) => {
    return `<button class="w-full p-3 rounded-lg bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors duration-200 text-left group"><div class="flex items-center justify-between"><div class="flex items-center space-x-3"><span class="text-lg">${escape(getParticleEmoji(particle.name))}</span> <div><div class="font-medium text-gray-900 dark:text-white group-hover:text-primary-600">${escape(particle.name)}</div> <div class="text-xs text-gray-500 dark:text-gray-400 font-mono">PDG: ${escape(particle.pdgid)}</div> </div></div> <div class="text-right">${particle.mass !== null ? `<div class="text-xs text-gray-600 dark:text-gray-300 font-mono">${escape(formatMassShort(particle.mass))} </div>` : ``} ${particle.charge !== null ? `<div class="text-xs text-gray-500 dark:text-gray-400">Q: ${escape(particle.charge > 0 ? "+" : "")}${escape(particle.charge)}e
                </div>` : ``} </div></div> </button>`;
  })}</div> <div class="mt-6 pt-4 border-t border-gray-200 dark:border-gray-700" data-svelte-h="svelte-1fm2u33"><p class="text-xs text-gray-500 dark:text-gray-400 text-center">Click any particle to view detailed information</p></div>`}</div>`;
});
const Page = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let searchQuery = "";
  let loading = false;
  let popularParticles = [];
  let $$settled;
  let $$rendered;
  let previous_head = $$result.head;
  do {
    $$settled = true;
    $$result.head = previous_head;
    $$rendered = `${$$result.head += `<!-- HEAD_svelte-11ajzib_START -->${$$result.title = `<title>Particle Explorer - Discover Fundamental Particles</title>`, ""}<meta name="description" content="Explore the world of particle physics. Search for particles by PDG ID and discover their properties, masses, charges, and more."><!-- HEAD_svelte-11ajzib_END -->`, ""} <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-900 dark:to-gray-800"> <div class="relative overflow-hidden"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16"><div class="text-center"><h1 class="text-4xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6 animate-fade-in" data-svelte-h="svelte-s4egrd">Explore the <span class="bg-gradient-to-r from-primary-600 to-purple-600 bg-clip-text text-transparent">Quantum Universe</span></h1> <p class="text-xl text-gray-600 dark:text-gray-300 mb-12 max-w-3xl mx-auto animate-fade-in" data-svelte-h="svelte-1v6rknh">Discover fundamental particles using PDG IDs. Search through the complete database of quarks, leptons, bosons, and more with detailed physics properties.</p>  <div class="max-w-2xl mx-auto mb-16 animate-slide-up">${validate_component(SearchBar, "SearchBar").$$render(
      $$result,
      { loading, searchQuery },
      {
        searchQuery: ($$value) => {
          searchQuery = $$value;
          $$settled = false;
        }
      },
      {}
    )}</div></div></div>  <div class="absolute inset-0 overflow-hidden pointer-events-none" data-svelte-h="svelte-1vxx93e"><div class="absolute top-1/4 left-1/4 w-2 h-2 bg-primary-400 rounded-full animate-pulse-subtle"></div> <div class="absolute top-1/3 right-1/3 w-3 h-3 bg-purple-400 rounded-full animate-pulse-subtle" style="animation-delay: 0.5s;"></div> <div class="absolute bottom-1/4 left-1/3 w-1 h-1 bg-blue-400 rounded-full animate-pulse-subtle" style="animation-delay: 1s;"></div> <div class="absolute bottom-1/3 right-1/4 w-2 h-2 bg-green-400 rounded-full animate-pulse-subtle" style="animation-delay: 1.5s;"></div></div></div>  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-20"><div class="grid grid-cols-1 lg:grid-cols-3 gap-8"> <div class="lg:col-span-1">${validate_component(PopularParticles, "PopularParticles").$$render($$result, { particles: popularParticles }, {}, {})}</div>  <div class="lg:col-span-2">${`${`${`<div class="card text-center py-12" data-svelte-h="svelte-utgi89"><div class="text-6xl mb-4">🔍</div> <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">Search for a Particle</h3> <p class="text-gray-600 dark:text-gray-400 mb-6">Enter a PDG ID above to discover detailed particle information</p> <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-gray-500 dark:text-gray-400"><div><span class="font-medium">Examples:</span></div> <div>11 (electron)</div> <div>2212 (proton)</div> <div>22 (photon)</div></div></div>`}`}`}</div></div></div></div>`;
  } while (!$$settled);
  return $$rendered;
});
export {
  Page as default
};
