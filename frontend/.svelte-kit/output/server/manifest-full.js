export const manifest = (() => {
function __memo(fn) {
	let value;
	return () => value ??= (value = fn());
}

return {
	appDir: "_app",
	appPath: "_app",
	assets: new Set([".gitkeep"]),
	mimeTypes: {},
	_: {
		client: {"start":"_app/immutable/entry/start.b48acadc.js","app":"_app/immutable/entry/app.394ec369.js","imports":["_app/immutable/entry/start.b48acadc.js","_app/immutable/chunks/scheduler.2d2d190c.js","_app/immutable/chunks/singletons.37de2947.js","_app/immutable/entry/app.394ec369.js","_app/immutable/chunks/scheduler.2d2d190c.js","_app/immutable/chunks/index.62dc93b3.js"],"stylesheets":[],"fonts":[]},
		nodes: [
			__memo(() => import('./nodes/0.js')),
			__memo(() => import('./nodes/1.js')),
			__memo(() => import('./nodes/2.js'))
		],
		routes: [
			{
				id: "/",
				pattern: /^\/$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 2 },
				endpoint: null
			}
		],
		matchers: async () => {
			
			return {  };
		}
	}
}
})();
