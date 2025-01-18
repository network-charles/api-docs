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
					label: 'Getting started',
					items: [
						// Each item here is one entry in the navigation menu.
						'getting-started/introduction',
						'getting-started/set-up'
					],
				},
				{
					label: 'Concept',
					autogenerate: { directory: 'concept' },
				},
				{
					label: 'Endpoints',
					items: [
						// Each item here is one entry in the navigation menu.
						{
							label: 'Currency Exchange Rate', slug: 'endpoints/currency-exchange-rate/currency-exchange-rate'
						},
					],
				},
				{
					label: 'Reference',
					autogenerate: { directory: 'reference' },
				},
				{
					label: 'Governance',
					autogenerate: { directory: 'governance' },
				},
			],
		}),
	],
});
