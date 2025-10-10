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
}
