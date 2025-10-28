import { Component, computed, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatTooltipModule } from '@angular/material/tooltip';
import { RouterLink } from '@angular/router';
import { AuthService } from '../../../core/auth/auth.service';
import { UiButton } from '../ui-button/ui-button';
import { MatIcon } from '@angular/material/icon';

@Component({
  selector: 'app-login-logout',
  standalone: true,
  imports: [CommonModule, MatButtonModule, MatTooltipModule, RouterLink, UiButton, MatIcon],
  templateUrl: './login-logout.html',
  styleUrls: ['./login-logout.scss'],
})
export class LoginLogoutComponent {
  private auth = inject(AuthService);

  isLoggedIn = computed(() => this.auth.isLoggedInUI());
  userName = computed(() => this.auth.userName());

  login() {
    this.auth.login();
  }
  logout() {
    this.auth.logout();
  }
}
