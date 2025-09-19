import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { BaseDocComponent } from '../../../../shared/components/base-doc/base-doc';
import { MatTabsModule } from '@angular/material/tabs';


@Component({
  selector: 'app-main-concepts-page',
  imports: [CommonModule, RouterLink, BaseDocComponent, MatTabsModule],
  templateUrl: './main-concepts-page.html',
  styleUrl: './main-concepts-page.scss'
})
export class MainConceptsPage {

}
