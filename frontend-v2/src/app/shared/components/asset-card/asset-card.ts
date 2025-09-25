import { Component, Input, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { RouterLink } from '@angular/router';
import { MatIconModule } from '@angular/material/icon';
import { MatTooltipModule } from '@angular/material/tooltip';
import { UiButton } from '../ui-button/ui-button';

type Visibility = 'public' | 'private' | 'unlisted' | '';

@Component({
  selector: 'ui-asset-card',
  standalone: true,
  imports: [CommonModule, RouterLink, DatePipe, UiButton, MatIconModule, MatTooltipModule],
  templateUrl: './asset-card.html',
  styleUrls: ['./asset-card.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AssetCardComponent {
  @Input() source = '';
  @Input() title = '';
  @Input() date?: string | number | Date;
  @Input() description = '';
  @Input({ required: true }) link!: string | any[];
  @Input() visibility: Visibility = '';

  get sourceLabel(): string {
    return (this.source || '')
      .replace(/[-_]/g, ' ')
      .replace(/\w\S*/g, (s) => s[0].toUpperCase() + s.slice(1).toLowerCase());
  }
  get sourceClass(): string {
    return `badge--${(this.source || '').toLowerCase()}`;
  }

  get visibilityIcon(): string {
    switch (this.visibility) {
      case 'public':
        return 'public';
      case 'private':
        return 'lock';
      case 'unlisted':
        return 'public_off';
      default:
        return '';
    }
  }
  get visibilityLabel(): string {
    if (!this.visibility) return '';
    return this.visibility[0].toUpperCase() + this.visibility.slice(1);
  }
}
