import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

import { BaseDocComponent } from '../../../../shared/components/base-doc/base-doc';
import { MatTabsModule } from '@angular/material/tabs';
import { MarkdownComponent } from 'ngx-markdown';

@Component({
  selector: 'app-main-concepts-run-page',
  imports: [CommonModule, BaseDocComponent, MatTabsModule, MarkdownComponent],
  templateUrl: './main-concepts-run-page.html',
  styleUrl: './main-concepts-run-page.scss',
})
export class MainConceptsRunPage {}
