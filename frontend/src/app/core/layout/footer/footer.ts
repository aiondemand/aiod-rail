import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { UiButton } from '../../../shared/components/ui-button/ui-button';

@Component({
  selector: 'app-footer',
  standalone: true,
  imports: [RouterLink, UiButton],
  templateUrl: './footer.html',
  styleUrls: ['./footer.scss'],
})
export class Footer {}
