// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	site: 'https://network-charles.github.io',
  	base: 'api-docs',
	integrations: [
		starlight({
			title: 'My API Docs Project',
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
					autogenerate: { directory: 'endpoints' },
				},
				{
					label: 'Tasks',
					autogenerate: { directory: 'tasks' },
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
