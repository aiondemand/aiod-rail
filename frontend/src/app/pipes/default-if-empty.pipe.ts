import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'defaultIfEmpty'
})
export class DefaultIfEmptyPipe implements PipeTransform {

  transform(value: any, default_value: string): string {
    return value?.toString() || default_value;
  }

}
