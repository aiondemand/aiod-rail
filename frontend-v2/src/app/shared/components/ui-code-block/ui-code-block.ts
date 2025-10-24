import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Highlight } from 'ngx-highlightjs';

@Component({
  selector: 'ui-code-block',
  standalone: true,
  imports: [CommonModule, Highlight],
  styleUrls: ['./ui-code-block.scss'],
  template: `
    <div class="code-wrap">
      <pre class="cb-pre hljs" [attr.data-filename]="filename || null">
        <code
          class="cb-code"
          [highlight]="code || ''"
          [language]="lang"
          [style.maxHeight]="maxHeight || null"
        ></code>
      </pre>
    </div>
  `,
})
export class UiCodeBlock {
  @Input() code = '';
  @Input({ alias: 'lang' }) lang: string = 'plaintext';
  @Input() filename?: string;
  @Input() maxHeight?: string;
}
