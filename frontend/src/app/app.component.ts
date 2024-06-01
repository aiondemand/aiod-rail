import { Component, inject } from '@angular/core';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { Observable } from 'rxjs';
import { map, shareReplay } from 'rxjs/operators';
import { AuthService } from './services/auth.service';
import { BackendApiService } from './services/backend-api.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  private breakpointObserver = inject(BreakpointObserver);
  leftSidebarMinimized = false;

  constructor(private authService: AuthService) {}

  isHandset$: Observable<boolean> = this.breakpointObserver.observe(Breakpoints.Handset)
    .pipe(
      map(result => result.matches),
      shareReplay()
    );

  get isLoggedIn(): boolean {
    return this.authService.isLoggedIn;
  }

  get isAdminUser(): boolean {
    return this.authService.isLoggedIn && this.authService.hasAdminRole;
  }
}
