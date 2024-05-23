import { Injectable } from '@angular/core';
import { FormControl } from '@angular/forms';
import { PageEvent } from '@angular/material/paginator';
import { ActivatedRoute, Router } from '@angular/router';
import { Observable, catchError, count, firstValueFrom, of } from 'rxjs';
import { ExperimentTemplate } from 'src/app/models/experiment-template';
import { BackendApiService } from 'src/app/services/backend-api.service';
import { SnackBarService } from 'src/app/services/snack-bar.service';
import { environment } from 'src/environments/environment';

@Injectable()
export  abstract class ExperimentTemplateListBaseComponent {
  protected experimentTemplates$: Observable<ExperimentTemplate[] | null>;
  protected total_template_count$: Observable<number>;
  protected pagination = {
    pageSize: environment.DEFAULT_PAGE_SIZE,
    pageIndex: 0,
    length: 0
  }
  protected searchQuery: string = "";
  
  protected filterOpened: boolean = false;
  protected chosenDockerImages: FormControl = new FormControl("");
  protected chosenModelPlatforms: FormControl = new FormControl("");
  protected chosenDatasetPlatforms: FormControl = new FormControl("");

  protected dockerImageList: string[] = [
    "Python:3.8",
    "Python:3.9",
    "Python:3.10",
  ];
  protected platforms: string[] = [
    "HuggingFace",
    "OpenML",
    "Zenodo"
  ]

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

        this.updateTemplates();
    });

  }

  handlePageEvent(e: PageEvent) {
    this.pagination.pageSize = e.pageSize;
    this.pagination.pageIndex = e.pageIndex;

    this.updateTemplates();
  }

  searchTemplates(query: string) {
    if (query.length == 0 && this.searchQuery == query) {
      return;
    }

    this.searchQuery = query;
    this.pagination.pageIndex = 0;

    this.updateTemplates();
  }

  updateTemplates() {
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

    this.experimentTemplates$ = this.getExperimentTemplates().pipe(
      catchError((error) => {
        if (error.status == 401) {
          this.snackBar.showError("An authorization error occurred. Try logging out and then logging in again.");
        }
        return of(null);
      })
    );

    firstValueFrom(this.getExperimentTemplatesCount())
      .then(count => this.pagination.length = count)
      .catch(err => console.error(err));
  }

  protected abstract getExperimentTemplates(): Observable<ExperimentTemplate[]>;

  protected abstract getExperimentTemplatesCount(): Observable<number>
}