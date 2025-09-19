import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';

type ButtonVariant = 'primary' | 'ghost' | 'outline' | 'danger' | 'menu';
type ButtonSize = 'sm' | 'md' | 'lg';
type ButtonType = 'button' | 'submit' | 'reset';

@Component({
  selector: 'ui-button',
  standalone: true,
  templateUrl: './ui-button.html',
  styleUrls: ['./ui-button.scss'],
  imports: [CommonModule],
})
export class UiButton {
  @Input() variant: ButtonVariant = 'primary';
  @Input() size: ButtonSize = 'md';
  @Input() type: ButtonType = 'button';
  @Input() disabled = false;
  @Input() loading = false;
  @Input() fullWidth = false;
  @Input() ariaLabel?: string;
}
