

export const index = 1;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/fallbacks/error.svelte.js')).default;
export const imports = ["_app/immutable/nodes/1.70ac5f7d.js","_app/immutable/chunks/scheduler.2d2d190c.js","_app/immutable/chunks/index.62dc93b3.js","_app/immutable/chunks/singletons.eee0e22c.js"];
export const stylesheets = [];
export const fonts = [];
