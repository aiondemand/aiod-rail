import { Component } from '@angular/core';
import { PageEvent } from '@angular/material/paginator';
import { ActivatedRoute, Router } from '@angular/router';
import { Observable, Subscription, firstValueFrom } from 'rxjs';
import { Dataset } from 'src/app/models/dataset';
import { BackendApiService } from 'src/app/services/backend-api.service';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-saved-datasets',
  templateUrl: './saved-datasets.component.html',
  styleUrls: ['./saved-datasets.component.scss']
})
export class SavedDatasetsComponent {
  datasets$: Observable<Dataset[]>;
  pagination = {
    pageSize: environment.DEFAULT_PAGE_SIZE,
    pageIndex: 0,
    length: 0 
  }

  subscription: Subscription;

  constructor(
    private backend: BackendApiService,
    private route: ActivatedRoute,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.pagination.pageSize = params['pageSize']
        ? parseInt(params['pageSize']) : 10;
      this.pagination.pageIndex = params['pageIndex']
        ? parseInt(params['pageIndex']) : 0;

      this.updateDatasets();
    });

    firstValueFrom(this.backend.getSavedDatasetsCount())
      .then(count => this.pagination.length = count)
      .catch(err => console.error(err));
  }

  ngOnDestroy(): void {
    this.subscription?.unsubscribe();
  }

  handlePageEvent(e: PageEvent) {
    this.pagination.length = e.length;
    this.pagination.pageSize = e.pageSize;
    this.pagination.pageIndex = e.pageIndex;

    // update the route
    this.router.navigate([], {
      relativeTo: this.route,
      queryParams: {
        pageSize: this.pagination.pageSize,
        pageIndex: this.pagination.pageIndex
      },
      queryParamsHandling: 'merge'
    });

    this.updateDatasets();
  }

  private updateDatasets() {
    this.datasets$ = this.backend.getSavedDatasets({
      offset: this.pagination.pageIndex * this.pagination.pageSize,
      limit: this.pagination.pageSize
    });
  }
}
