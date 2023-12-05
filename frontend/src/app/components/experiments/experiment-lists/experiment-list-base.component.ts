import { Injectable } from '@angular/core';
import { PageEvent } from '@angular/material/paginator';
import { ActivatedRoute, Router } from '@angular/router';
import { Observable } from 'rxjs';
import { Experiment } from 'src/app/models/experiment';
import { BackendApiService } from 'src/app/services/backend-api.service';
import { environment } from 'src/environments/environment';

@Injectable()
export  abstract class ExperimentListBaseComponent {
  protected experiments$: Observable<Experiment[]>;
  protected pagination = {
    pageSize: environment.DEFAULT_PAGE_SIZE,
    pageIndex: 0,
    length: 0
  }

  constructor(
    protected backend: BackendApiService,
    protected route: ActivatedRoute,
    protected router: Router
  ) { }

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.pagination.pageSize = params['pageSize']
        ? parseInt(params['pageSize']) : 10;
      this.pagination.pageIndex = params['pageIndex']
        ? parseInt(params['pageIndex']) : 0;

        this.experiments$ = this.updateExperiments();
    });

    this.getExperimentsCount().subscribe(count => {
      this.pagination.length = count;
    });
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

    this.experiments$  = this.updateExperiments();
  }

  protected abstract updateExperiments(): Observable<Experiment[]>;

  protected abstract getExperimentsCount(): Observable<number>
}