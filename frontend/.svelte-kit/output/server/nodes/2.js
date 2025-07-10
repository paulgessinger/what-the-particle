

export const index = 2;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/_page.svelte.js')).default;
export const imports = ["_app/immutable/nodes/2.02037524.js","_app/immutable/chunks/scheduler.2d2d190c.js","_app/immutable/chunks/index.62dc93b3.js"];
export const stylesheets = [];
export const fonts = [];
