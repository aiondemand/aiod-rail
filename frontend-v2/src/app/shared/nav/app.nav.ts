import { NavSection } from './nav.types';

export const APP_NAV: NavSection[] = [
  {
    title: 'Docs',
    icon: 'article',
    expanded: true,
    items: [
      { label: 'What is RAIL?', slug: '/docs/about', icon: 'info' },
      { label: 'Main concepts', slug: '/docs/main-concepts', icon: 'category' },
      { label: 'Experiment Template', slug: '/docs/main-concepts-template', icon: 'dashboard' },
      { label: 'Experiment', slug: '/docs/main-concepts-experiments', icon: 'biotech' },
      {
        label: 'Experiment Run',
        slug: '/docs/main-concepts-run',
        icon: 'play_circle',
        dividerAfter: true,
      },
      { label: 'RAIL SDKs', slug: '/docs/rail-sdks', icon: 'integration_instructions' },
      { label: 'Outer SDK', slug: '/docs/outer-sdk', icon: 'device_hub' },
      { label: 'Inner SDKs', slug: '/docs/inner-sdk', icon: 'memory' }, /// external https://www.google.com/
    ],
  },
  {
    title: 'Experiments',
    icon: 'science',
    expanded: true,
    items: [
      { label: 'Public experiments', slug: '/experiments/public', icon: 'public' },
      { label: 'My experiments', slug: '/experiments/my-experiments', icon: 'person' },
      {
        label: 'Create experiment',
        slug: '/experiments/create-experiment',
        icon: 'add',
        dividerAfter: true,
      },
      { label: 'Public templates', slug: '/experiments/templates', icon: 'public' },
      { label: 'My templates', slug: '/experiments/my-templates', icon: 'person' },
      {
        label: 'Create template',
        slug: '/experiments/create-template',
        icon: 'add',
      },
    ],
  },
  {
    title: 'Datasets',
    icon: 'grid_view',
    expanded: true,
    items: [
      { label: 'All datasets', slug: '/datasets/all', icon: 'dataset' },
      { label: 'My datasets', slug: '/datasets/my-datasets', icon: 'folder_shared' },
      { label: 'Create', slug: '/datasets/create-dataset', icon: 'add' },
    ],
  },
];
