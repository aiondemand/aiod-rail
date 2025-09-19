import { Component, Input, signal } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';

export interface NavItem {
  label: string;
  icon?: string;
  slug?: string; // internal link -> [baseLink, slug]
  href?: string; // external link
  command?: () => void; // action without navigation
  suffixIcon?: string;
  suffixCommand?: () => void;
  disabled?: boolean;
  activeExact?: boolean;
  children?: NavItem[];
}

export interface NavSection {
  title?: string;
  icon?: string;
  slug?: string; // internal clickable title
  href?: string; // external clickalbe title
  command?: () => void; // action
  activeExact?: boolean;

  collapsible?: boolean; // default true
  expanded?: boolean; // default true

  items: NavItem[];
}

@Component({
  selector: 'ui-sidenav',
  standalone: true,
  imports: [RouterLink, RouterLinkActive],
  templateUrl: './ui-sidenav.html',
  styleUrls: ['./ui-sidenav.scss'],
})
export class UiSidenav {
  @Input() baseLink = '';
  @Input() sections: NavSection[] = [];
  @Input() collapsed = false;
  @Input() stickyTop = 72;

  cssTop = signal('72px');
  ngOnChanges() {
    this.cssTop.set(`${this.stickyTop}px`);
  }

  onMainClick(it: NavItem | NavSection, ev: Event) {
    if ((it as NavItem).disabled) {
      ev.preventDefault();
      return;
    }
    if (it.command && !it['href'] && !it['slug']) {
      ev.preventDefault();
      it.command();
    }
  }
}
