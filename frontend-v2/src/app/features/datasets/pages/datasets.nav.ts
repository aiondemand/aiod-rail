import { NavSection } from '../../../shared/nav/nav.types';

export const DATASETS_NAV: NavSection[] = [
  { items: [
    { label: 'All datasets', slug: '', icon: 'dataset' },
    { label: 'My datasets', slug: 'mine', icon: 'folder_shared' },
    { label: '+ Create dataset', slug: 'create', icon: 'add' },
  ]},
];
