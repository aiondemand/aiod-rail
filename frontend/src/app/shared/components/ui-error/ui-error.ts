import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { UiButton } from '../ui-button/ui-button';

@Component({
  selector: 'ui-error',
  standalone: true,
  imports: [CommonModule, MatIconModule, UiButton],
  templateUrl: './ui-error.html',
  styleUrls: ['./ui-error.scss'],
})
export class UiErrorComponent {
  @Input() show = false;
  @Input() message = 'Something went wrong.';
  @Input() details: string | string[] | null = null;
  @Input() retryable = true;
  @Input() retryLabel = 'Try again';
  @Input() closable = false;
  @Input() icon = 'error';

  @Input() ariaRole: 'alert' | 'status' = 'alert'; // alert = assertive
  @Input() ariaLive: 'assertive' | 'polite' = 'assertive';

  @Output() retry = new EventEmitter<void>();
  @Output() close = new EventEmitter<void>();

  onRetry() {
    this.retry.emit();
  }
  onClose() {
    this.close.emit();
  }

  asArray(v: string | string[]): string[] {
    return Array.isArray(v) ? v : [v];
  }
}
