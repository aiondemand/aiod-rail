import { NavSection } from '../../../shared/nav/nav.types';

export const DOCS_NAV: NavSection[] = [
  { items: [ { label: 'What is RAIL?', slug: 'about', icon: 'info' } ] },
  {
    title: 'Main concepts of RAIL',
    titleSlug: 'main-concepts',
    items: [
      { label: 'Experiment Template', slug: 'main-concepts-template',     icon: 'view_kanban' },
      { label: 'Experiment',          slug: 'main-concepts-experiments',  icon: 'biotech' },
      { label: 'Experiment Run',      slug: 'main-concepts-run',          icon: 'play_circle' },
    ],
  },
];
