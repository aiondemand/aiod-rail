import { Component, computed, inject, HostListener, OnInit } from '@angular/core';
import { CommonModule, DOCUMENT } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatTooltipModule } from '@angular/material/tooltip';
import { AuthService } from '../../../core/auth/auth.service';
import { UiButton } from '../ui-button/ui-button';

@Component({
  selector: 'app-login-logout',
  standalone: true,
  imports: [CommonModule, MatButtonModule, MatTooltipModule, UiButton],
  templateUrl: './login-logout.html',
  styleUrls: ['./login-logout.scss'],
})
export class LoginLogoutComponent implements OnInit {
  private auth = inject(AuthService);
  private doc = inject(DOCUMENT);

  isLoggedIn = computed(() => this.auth.isLoggedIn());
  userName = computed(() => this.auth.userName());

  sidebarOpen = false;

  sidebarTop = 0;

  ngOnInit(): void {
    this.updateSidebarTop();
    setTimeout(() => this.updateSidebarTop(), 0);
  }

  @HostListener('window:resize')
  onResize() {
    this.updateSidebarTop();
  }

  @HostListener('window:scroll')
  onScroll() {
    if (!this.sidebarOpen) return;
    this.updateSidebarTop();
  }

  private updateSidebarTop() {
    const header = this.doc.querySelector('header.topbar') as HTMLElement | null;
    if (!header) {
      this.sidebarTop = 0;
      return;
    }

    const rect = header.getBoundingClientRect();
    this.sidebarTop = rect.bottom;
  }

  toggleSidebar() {
    if (!this.isLoggedIn()) return;
    this.sidebarOpen = !this.sidebarOpen;

    if (this.sidebarOpen) {
      this.updateSidebarTop();
    }
  }

  closeSidebar() {
    this.sidebarOpen = false;
  }

  login() {
    this.auth.login();
  }

  logout() {
    this.sidebarOpen = false;
    this.auth.logout();
  }
}
