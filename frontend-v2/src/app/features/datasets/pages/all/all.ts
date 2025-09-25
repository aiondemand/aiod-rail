import { Component } from '@angular/core';
import { AssetCardComponent } from '../../../../shared/components/asset-card/asset-card';

@Component({
  selector: 'app-all',
  imports: [AssetCardComponent],
  templateUrl: './all.html',
  styleUrl: './all.scss',
})
export class AllDatasetsPage {}
