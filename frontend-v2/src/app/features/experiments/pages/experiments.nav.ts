import { NavSection } from '../../../shared/nav/nav.types';

export const EXPERIMENTS_NAV: NavSection[] = [
  { items: [
    { label: 'Public experiments', slug: 'public', icon: 'public' },
    { label: 'My experiments', slug: 'mine', icon: 'person' },
    { label: '+ Create an experiment', slug: 'create', icon: 'add' },
  ]},
  { title: 'Templates', items: [
    { label: 'Public templates', slug: 'templates/public', icon: 'view_module' },
    { label: 'My templates', slug: 'templates/mine', icon: 'folder_special' },
    { label: '+ Create a template', slug: 'templates/create', icon: 'add' },
  ]},
];
