import { Component } from '@angular/core';
import { AssetCardComponent } from '../../../../shared/components/asset-card/asset-card';

@Component({
  selector: 'app-public',
  imports: [AssetCardComponent],
  templateUrl: './public.html',
  styleUrl: './public.scss',
})
export class PublicPage {}
