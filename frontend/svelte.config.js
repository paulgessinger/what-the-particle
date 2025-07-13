import adapter from '@sveltejs/adapter-static';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter({
			fallback: 'index.html'
		}),
		paths: {
			base: process.env.NODE_ENV === 'production' ? '/what-the-particle' : ''
		},
		prerender: {
			handleHttpError: ({ path, referrer, message }) => {
				// ignore favicon and other static file errors
				if (path.includes('favicon')) return;
				throw new Error(message);
			}
		}
	}
};

export default config;
