

export const index = 0;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/_layout.svelte.js')).default;
export const imports = ["_app/immutable/nodes/0.ef6a59b0.js","_app/immutable/chunks/scheduler.2d2d190c.js","_app/immutable/chunks/index.62dc93b3.js"];
export const stylesheets = ["_app/immutable/assets/0.49f47a38.css"];
export const fonts = [];
