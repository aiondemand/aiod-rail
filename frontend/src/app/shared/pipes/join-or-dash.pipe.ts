import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'joinOrDash', standalone: true })
export class JoinOrDashPipe implements PipeTransform {
  transform(arr: any[] | undefined, sep = ', ', dash = '—'): string {
    return arr && arr.length ? arr.join(sep) : dash;
  }
}
