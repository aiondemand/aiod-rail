import { Pipe, PipeTransform } from '@angular/core';
import { formatPlatformName } from '../helpers/formatting-helper';
import { Platform } from '../models/platform';

@Pipe({
  name: 'formatPlatformName'
})
export class FormatPlatformNamePipe implements PipeTransform {

  transform(value: string | Platform, ...args: unknown[]): string {
    return formatPlatformName(value);
  }
}
