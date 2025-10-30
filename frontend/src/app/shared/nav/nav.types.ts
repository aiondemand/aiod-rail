export interface NavItem {
  label: string;
  slug: string;
  icon?: string;
  dividerAfter?: boolean;
}

export interface NavSection {
  title?: string;
  titleSlug?: string;
  icon?: string;         //(material symbols)

  items: NavItem[];

  collapsible?: boolean; // default: true
  expanded?: boolean;    // default: true
}
