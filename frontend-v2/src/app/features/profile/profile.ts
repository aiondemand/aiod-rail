import { Component, computed, effect, inject, PLATFORM_ID, signal } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { catchError, firstValueFrom, of } from 'rxjs';

import { UiButton } from '../../shared/components/ui-button/ui-button';
import { UiLoadingComponent } from '../../shared/components/ui-loading/ui-loading';
import { UiErrorComponent } from '../../shared/components/ui-error/ui-error';

import { AuthService } from '../../core/auth/auth.service';
import { BackendApiService } from '../../shared/services/backend-api.service';
import { SnackBarService } from '../../shared/services/snack-bar.service';

type UserRailProfile = { email: string; api_key?: string | null };

@Component({
  standalone: true,
  selector: 'app-profile-page',
  imports: [
    CommonModule,
    MatIconModule,
    MatTooltipModule,
    MatFormFieldModule,
    MatInputModule,
    UiButton,
    UiLoadingComponent,
    UiErrorComponent,
  ],
  templateUrl: './profile.html',
  styleUrls: ['./profile.scss'],
})
export class ProfilePage {
  private auth = inject(AuthService);
  private backend = inject(BackendApiService);
  private snack = inject(SnackBarService);
  private platformId = inject(PLATFORM_ID);

  readonly isLoggedIn = computed(() => this.auth.isLoggedIn());
  readonly userName = computed(() => this.auth.userName());

  readonly profile = signal<UserRailProfile | null>(null);
  readonly loading = signal(true);
  readonly showKey = signal(false);

  constructor() {
    effect(
      () => {
        const canRun = isPlatformBrowser(this.platformId) && this.isLoggedIn();
        if (canRun) {
          this.loadProfile();
        } else {
          this.profile.set(null);
          this.loading.set(false);
        }
      },
      { allowSignalWrites: true }
    );
  }

  private async loadProfile() {
    this.loading.set(true);
    try {
      const p = await firstValueFrom(
        this.backend.getUserProfile().pipe(
          catchError((err) => {
            console.error('[profile] load error:', err);
            this.snack.showError('Failed to load user profile');
            return of(null);
          })
        )
      );
      this.profile.set(p);
    } finally {
      this.loading.set(false);
    }
  }

  async createOrUpdateApiKey() {
    const key = await firstValueFrom(
      this.backend.createOrUpdateUserApiKey().pipe(
        catchError((err) => {
          console.error('[profile] api key error:', err);
          this.snack.showError('Failed to generate API key');
          return of(null);
        })
      )
    );
    if (!key) return;
    const cur = this.profile();
    if (cur) this.profile.set({ ...cur, api_key: key });
    this.snack.show('New API key generated');
  }

  copyApiKeyToClipboard() {
    const key = this.profile()?.api_key ?? '';
    if (!key) return;
    if (!isPlatformBrowser(this.platformId) || !('clipboard' in navigator)) {
      this.snack.showError('Clipboard is not available in this environment');
      return;
    }
    navigator.clipboard.writeText(key).then(
      () => this.snack.show('API key copied to clipboard'),
      () => this.snack.showError('Failed to copy API key to clipboard')
    );
  }
}
