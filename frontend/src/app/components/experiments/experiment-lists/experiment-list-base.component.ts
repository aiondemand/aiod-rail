import { Injectable } from '@angular/core';
import { PageEvent } from '@angular/material/paginator';
import { ActivatedRoute, Router } from '@angular/router';
import { Observable, catchError, firstValueFrom, of } from 'rxjs';
import { Experiment } from 'src/app/models/experiment';
import { BackendApiService } from 'src/app/services/backend-api.service';
import { SnackBarService } from 'src/app/services/snack-bar.service';
import { environment } from 'src/environments/environment';

@Injectable()
export abstract class ExperimentListBaseComponent {
  protected experiments$: Observable<Experiment[] | null>;
  protected pagination = {
    pageSize: environment.DEFAULT_PAGE_SIZE,
    pageIndex: 0,
    length: 0
  }
  protected searchQuery: string = "";

  constructor(
    protected backend: BackendApiService,
    protected route: ActivatedRoute,
    protected router: Router,
    private snackBar: SnackBarService,
  ) { }

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.pagination.pageSize = params['pageSize']
        ? parseInt(params['pageSize']) : 10;
      this.pagination.pageIndex = params['pageIndex']
        ? parseInt(params['pageIndex']) : 0;

        this.updateExperiments();
    });
  }

  handlePageEvent(e: PageEvent) {
    this.pagination.pageSize = e.pageSize;
    this.pagination.pageIndex = e.pageIndex;
    
    this.updateExperiments();
  }

  searchExperiments(query: string) {
    if (query.length == 0 && this.searchQuery == query) {
      return;
    }

    this.searchQuery = query;
    this.pagination.pageIndex = 0;

    this.updateExperiments(); 
  }

  updateExperiments() {
    interface QueryParams {
      pageSize: number,
      pageIndex: number,
      searchQuery?: string
    }

    let queryParams: QueryParams = {
      pageSize: this.pagination.pageSize,
      pageIndex: this.pagination.pageIndex
    }
    if (this.searchQuery.length > 0) {
      queryParams.searchQuery = this.searchQuery;
    }    

    this.router.navigate([], {
      relativeTo: this.route,
      queryParams: queryParams,
      queryParamsHandling: 'merge'
    });

    this.experiments$  = this.getExperiments().pipe(
      catchError(error => {
        if (error.status == 401) {
          this.snackBar.showError("An authorization error occurred. Try logging out and then logging in again.");
        }
        return of(null);
      })
    );

    firstValueFrom(this.getExperimentsCount())
      .then(count => this.pagination.length = count)
      .catch(err => console.error(err));
  }

  protected abstract getExperiments(): Observable<Experiment[]>;

  protected abstract getExperimentsCount(): Observable<number>;
}
