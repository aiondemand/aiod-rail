import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatSelectModule } from '@angular/material/select';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { UiButton } from '../ui-button/ui-button';

@Component({
  selector: 'ui-search-toolbar',
  standalone: true,
  imports: [CommonModule, MatSelectModule, MatIconModule, MatProgressSpinnerModule, UiButton],
  templateUrl: './search-toolbar.html',
  styleUrls: ['./search-toolbar.scss'],
})
export class SearchToolbarComponent {
  /* ---- Inputs ---- */
  @Input() query = '';
  @Input() placeholder = 'Full-text search';
  @Input() showSearch = true;

  /** Enhanced checkbox */
  @Input() showEnhanced = false;
  @Input() enhanced = false;

  @Input() pageSize = 10;
  @Input() pageIndex = 0;

  /** Count */
  @Input() length: number | undefined = undefined;

  /** Loading state of LIST */
  @Input() loading = false;

  /** Loading state COUNT */
  @Input() countLoading = false;

  /** pagesize options */
  @Input() pageSizeOptions: number[] = [10, 25, 50, 100];

  /* ---- Outputs ---- */
  @Output() search = new EventEmitter<string>();
  @Output() enhancedChange = new EventEmitter<boolean>();
  @Output() pageSizeChange = new EventEmitter<number>();
  @Output() pageIndexChange = new EventEmitter<number>();

  /* ---- Derived / helpers ---- */
  get offset(): number {
    return this.pageIndex * this.pageSize;
  }
  get canPrev(): boolean {
    return this.pageIndex > 0;
  }
  get canNext(): boolean {
    if (typeof this.length !== 'number') return false;
    return this.offset + this.pageSize < this.length;
  }
  get from(): number {
    if (typeof this.length !== 'number') return 0;
    return this.length === 0 ? 0 : this.offset + 1;
  }
  get to(): number {
    // pageSize
    if (typeof this.length !== 'number') return this.pageSize;
    return Math.min(this.offset + this.pageSize, this.length);
  }

  onSearch(value: string) {
    this.search.emit((value ?? '').trim());
  }
  toggleEnhanced(on: boolean) {
    this.enhancedChange.emit(on);
  }
  changePageSize(ps: number) {
    this.pageSizeChange.emit(ps);
  }
  prevPage() {
    if (!this.canPrev || this.loading) return;
    this.pageIndexChange.emit(this.pageIndex - 1);
  }
  nextPage() {
    if (!this.canNext || this.loading) return;
    this.pageIndexChange.emit(this.pageIndex + 1);
  }
}
