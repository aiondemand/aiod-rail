import { Pipe, PipeTransform } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

@Pipe({
  name: 'linkify',
  standalone: true,
  pure: true,
})
export class LinkifyPipe implements PipeTransform {
  constructor(private sani: DomSanitizer) {}

  transform(value: string | null | undefined): SafeHtml {
    if (!value) return '';
    const text = String(value);

    // URL regex: zachytí http(s)://... alebo www....
    // a oddelí prípadnú koncovú interpunkciu (.,;:!?) a uzatváraciu zátvorku
    const urlRe = /(?:(https?:\/\/|www\.)[^\s<>"')]+)([)\]\}\.,;:!?]*)(?=\s|$)/gi;

    const html = text.replace(urlRe, (_, protoOrWww: string, trail: string) => {
      let url = _;
      // ak začína na www., doplň http
      const href = protoOrWww.toLowerCase().startsWith('http') ? url : `http://${url}`;
      // odstráň trailing interpunkciu z href (vrátime ju za odkaz)
      const m = href.match(/^(.*?)([)\]\}\.,;:!?]*)$/);
      const cleanHref = m ? m[1] : href;
      const suffix = (m ? m[2] : '') + (trail || '');

      return `<a href="${cleanHref}"
                 target="_blank"
                 rel="noopener noreferrer nofollow">${_}</a>${suffix}`;
    });

    // konverzia nových riadkov na <br> (ak chceš zachovať zalomenia)
    const withBreaks = html.replace(/\n/g, '<br>');

    return this.sani.bypassSecurityTrustHtml(withBreaks);
  }
}
