import { Component, Input, ChangeDetectionStrategy, OnChanges } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { RouterLink } from '@angular/router';
import { MatIconModule } from '@angular/material/icon';
import { MatTooltipModule } from '@angular/material/tooltip';
import { UiButton } from '../ui-button/ui-button';
import { Dataset } from '../../models/dataset';
import { formatPlatformName } from '../../helpers/formatting-helper';
import { Platform } from '../../models/platform';

type Visibility = 'public' | 'private' | 'unlisted' | '';

@Component({
  selector: 'ui-asset-card',
  standalone: true,
  imports: [CommonModule, RouterLink, DatePipe, UiButton, MatIconModule, MatTooltipModule],
  templateUrl: './asset-card.html',
  styleUrls: ['./asset-card.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AssetCardComponent implements OnChanges {
  @Input() source = '';
  @Input() title = '';
  @Input() date?: string | number | Date;
  @Input() description = '';
  @Input() link?: string | any[];
  @Input() visibility: Visibility = '';
  @Input() resource?: Dataset;

  @Input() approved?: boolean | null;
  @Input() archived?: boolean | null;
  @Input() state?: string | null;

  ngOnChanges() {
    if (this.resource) {
      this.source = this.resource.platform ?? this.source;
      this.title = this.resource.name ?? this.title;
      this.date = this.resource.date_published ?? this.date;

      const plain = this.resource.description?.plain?.trim();
      const html = this.resource.description?.html ?? '';
      const noTags = html
        .replace(/<[^>]+>/g, ' ')
        .replace(/\s+/g, ' ')
        .trim();
      this.description = plain || noTags || this.description;

      if (!this.link && this.resource.identifier) {
        this.link = ['/datasets', this.resource.identifier];
      }
    }
  }

  get sourceLabel(): string {
    const p: string | Platform = (this.resource?.platform as any) ?? this.source ?? '';
    return formatPlatformName(p);
  }
  get sourceClass(): string {
    const raw = (this.resource?.platform ?? this.source ?? '').toString();
    return `badge--${raw.toLowerCase()}`;
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
    return this.visibility ? this.visibility[0].toUpperCase() + this.visibility.slice(1) : '';
  }

  get showWaitingApproval(): boolean {
    if (this.archived === true) return false;
    return this.approved === false;
  }

  get approvalTooltip(): string {
    return 'Waiting for approval';
  }

  get showArchived(): boolean {
    return this.archived === true;
  }
  get archivedTooltip(): string {
    return 'This item is archived';
  }
}
