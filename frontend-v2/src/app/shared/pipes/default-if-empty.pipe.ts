import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'defaultIfEmpty', standalone: true })
export class DefaultIfEmptyPipe implements PipeTransform {
  transform(value: any, fallback: string): string {
    const v = value?.toString?.() ?? '';
    return v.trim().length ? v : fallback;
  }
}
