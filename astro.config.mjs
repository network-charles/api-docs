// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	site: 'https://network-charles.github.io',
  	base: 'api-docs',
	integrations: [
		starlight({
			title: 'My Docs',
			social: {
				github: 'https://github.com/withastro/starlight',
			},
			sidebar: [
				{
					label: 'Introduction',
					items: [
						{ label: 'Introduction', slug: 'introduction' },
					]
				},
				{
					label: 'Endpoints',
					items: [
						// Each item here is one entry in the navigation menu.
						{
							label: 'Currency Exchange Rate', slug: 'endpoints/currency_exchange_rate/currency_exchange_rate' },
					],
				},
				// {
				// 	label: 'Reference',
				// 	autogenerate: { directory: 'reference' },
				// },
			],
		}),
	],
});
