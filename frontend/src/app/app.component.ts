import { Component, inject } from '@angular/core';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { Observable } from 'rxjs';
import { filter, map, mergeMap, shareReplay } from 'rxjs/operators';
import { AuthService } from './services/auth.service';
import { BackendApiService } from './services/backend-api.service';
import { Meta } from '@angular/platform-browser';
import { ActivatedRoute, NavigationEnd, Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  private breakpointObserver = inject(BreakpointObserver);
  leftSidebarMinimized = false;

  constructor(
    private authService: AuthService,
    private meta: Meta,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.setGlobalMeta();
    this.setupRouteMeta();
  }

  setGlobalMeta() {
    // TODO
    // Once we actually make frequent changes to the static content of our websites
    // we would need to change this hardcoded value for a dynamically calculated one
    this.meta.updateTag({
      property: 'article:modified_time',
      content: '2025-06-01T00:00:00+00:0'
    });
  }

  setupRouteMeta() {
    // Based on the URL we decide whether we would advise a crawler to go over the data or not...
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd),
      map(() => this.route),
      map(route => {
        while (route.firstChild) route = route.firstChild;
        return route;
      }),
      mergeMap(route => route.data)
    ).subscribe(data => {
      // Apply custom meta based on route data
      console.log(data);
      if (data["crawlMeta"]) {
        this.meta.updateTag({
          name: 'x-dont-crawl',
          content: data["crawlMeta"]
        });
      }
      else  {
        this.meta.removeTag('name="x-dont-crawl"');
      }
    });
  }

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
