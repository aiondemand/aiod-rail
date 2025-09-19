import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Header } from './core/layout/header/header';
import { Footer } from './core/layout/footer/footer';
import { MainLayout } from './core/layout/main-layout/main-layout';

@Component({
  selector: 'app-root',
  imports: [Header, Footer, MainLayout],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  protected readonly title = signal('AiodRail-frontend-v2');
}
