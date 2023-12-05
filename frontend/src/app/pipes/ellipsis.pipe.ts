import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'ellipsis'
})
export class EllipsisPipe implements PipeTransform {

  transform(value: string, limit: number): any {
    if(limit && value.length > limit) {
      return value.substring(0, limit).concat('...');
    }
    return value;
  }
}