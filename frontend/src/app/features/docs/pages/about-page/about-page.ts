import { Component, ChangeDetectionStrategy, ElementRef, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { BaseDocComponent } from '../../../../shared/components/base-doc/base-doc';
import { MatTabsModule } from '@angular/material/tabs';
import { MarkdownComponent } from 'ngx-markdown';

@Component({
  selector: 'app-about-page',
  standalone: true,
  imports: [CommonModule, RouterLink, BaseDocComponent, MatTabsModule, MarkdownComponent],
  templateUrl: './about-page.html',
  styleUrls: ['./about-page.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AboutPage {}
