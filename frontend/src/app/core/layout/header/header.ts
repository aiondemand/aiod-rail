import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { UiButton } from '../../../shared/components/ui-button/ui-button';
import { ThemeSwitch } from '../../../shared/components/theme-switch/theme-switch';
import { LoginLogoutComponent } from '../../../shared/components/login-logout/login-logout';

@Component({
  selector: 'app-header',
  imports: [RouterLink, RouterLinkActive, UiButton, ThemeSwitch, LoginLogoutComponent],
  templateUrl: './header.html',
  styleUrl: './header.scss',
})
export class Header {}
