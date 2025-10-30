import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

@Component({
  selector: 'ui-loading',
  standalone: true,
  imports: [CommonModule, MatProgressSpinnerModule],
  templateUrl: './ui-loading.html',
  styleUrls: ['./ui-loading.scss'],
})
export class UiLoadingComponent {
  @Input() show = false;

  @Input() diameter = 32;

  @Input() message: string | null = null;

  @Input() ariaLabel = 'Loading';
}
