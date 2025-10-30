import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { BaseDocComponent } from '../../../../shared/components/base-doc/base-doc';
import { MatTabsModule } from '@angular/material/tabs';
import { MarkdownComponent } from 'ngx-markdown';

@Component({
  selector: 'app-main-concepts-template-page',
  imports: [CommonModule, RouterLink, BaseDocComponent, MatTabsModule, MarkdownComponent],
  templateUrl: './main-concepts-template-page.html',
  styleUrl: './main-concepts-template-page.scss'
})
export class MainConceptsTemplatePage {

}
