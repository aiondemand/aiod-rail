import { Component } from '@angular/core';
import { catchError, EMPTY, firstValueFrom } from 'rxjs';
import { UserRailProfile } from 'src/app/models/user-rail-profile';
import { BackendApiService } from 'src/app/services/backend-api.service';
import { SnackBarService } from 'src/app/services/snack-bar.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent {
  profile: UserRailProfile = { email: '' };
  showKey: boolean = false;

  constructor(
    private backend: BackendApiService,
    private snackBar: SnackBarService
  ) { }

  async ngOnInit() {
    this.profile = await firstValueFrom(
      this.backend.getUserProfile().pipe(
        catchError(_ => {
        this.snackBar.showError("Failed to load user profile");
          return EMPTY;
        })
      )
    );
  }

  async createOrUpdateApiKey() {
    this.profile.api_key = await firstValueFrom(
      this.backend.createOrUpdateUserApiKey().pipe(
        catchError(_ => {
          this.snackBar.showError("Failed to generate API key");
          return EMPTY;
        })
      )
    );
  }

  copyApiKeyToClipboard() {
    navigator.clipboard.writeText(this.profile.api_key || '').then(() => {
      this.snackBar.show("API key copied to clipboard");
    }, () => {
      this.snackBar.showError("Failed to copy API key to clipboard");
    });
  }
}
