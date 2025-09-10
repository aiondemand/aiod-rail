import { Component, OnInit } from '@angular/core';
import { PageEvent } from '@angular/material/paginator';
import { ActivatedRoute, Router } from '@angular/router';
import { Observable, firstValueFrom } from 'rxjs';
import { Dataset } from 'src/app/models/dataset';
import { BackendApiService } from 'src/app/services/backend-api.service';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-dataset-list',
  templateUrl: './dataset-list.component.html',
  styleUrls: ['./dataset-list.component.scss']
})
export class DatasetListComponent implements OnInit {
  datasets$: Observable<Dataset[]>;
  total_dataset_count$: Observable<number>;
  pagination = {
    pageSize: environment.DEFAULT_PAGE_SIZE,
    pageIndex: 0,
    length: 0
  }
  searchQuery: string = "";
  isEnhanced: boolean = false;

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
  }

  handlePageEvent(e: PageEvent) {
    this.pagination.pageSize = e.pageSize;
    this.pagination.pageIndex = e.pageIndex;

    this.updateDatasets();
  }

  searchDatasets(query: string) {
    if (query.length == 0 && this.searchQuery == query) {
      return;
    }

    this.searchQuery = query;
    this.pagination.pageIndex = 0;

    this.updateDatasets();
  }

  private updateDatasets() {
    interface QueryParams {
      pageSize: number,
      pageIndex: number,
      searchQuery?: string
    }

    let queryParams: QueryParams = {
      pageSize: this.pagination.pageSize,
      pageIndex: this.pagination.pageIndex
    };
    if (this.searchQuery.length > 0) {
      queryParams.searchQuery = this.searchQuery
    }

    this.router.navigate([], {
      relativeTo: this.route,
      queryParams: queryParams,
      queryParamsHandling: 'merge'
    });

    this.datasets$ = this.backend.getDatasets(
      this.searchQuery,
      {
        offset: this.pagination.pageIndex * this.pagination.pageSize,
        limit: this.pagination.pageSize
      },
      this.isEnhanced
    );

    firstValueFrom(this.backend.getDatasetsCount(this.searchQuery, this.isEnhanced))
      .then(count => this.pagination.length = count)
      .catch(err => console.error(err));
  }
}
