import { Component, signal } from '@angular/core';

import { TopNavbar } from './core/layout/top-navbar/top-navbar';
import { Footer } from './core/layout/footer/footer';
import { MainLayout } from './core/layout/main-layout/main-layout';

@Component({
  selector: 'app-root',
  imports: [TopNavbar, Footer, MainLayout],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  protected readonly title = signal('AiodRail-frontend-v2');
}
