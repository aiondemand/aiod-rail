import { Injectable } from '@angular/core';
import { FormControl } from '@angular/forms';
import { PageEvent } from '@angular/material/paginator';
import { ActivatedRoute, Router } from '@angular/router';
import { Observable, catchError, of } from 'rxjs';
import { ExperimentTemplate } from 'src/app/models/experiment-template';
import { BackendApiService } from 'src/app/services/backend-api.service';
import { SnackBarService } from 'src/app/services/snack-bar.service';
import { environment } from 'src/environments/environment';

@Injectable()
export  abstract class ExperimentTemplateListBaseComponent {
  protected experimentTemplates$: Observable<ExperimentTemplate[] | null>;
  protected pagination = {
    pageSize: environment.DEFAULT_PAGE_SIZE,
    pageIndex: 0,
    length: 0
  }
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

    this.getExperimentTemplatesCount().subscribe(count => {
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
    
    this.updateTemplates();    
  }

  updateTemplates() {
    this.experimentTemplates$ = this.updateExperimentTemplates().pipe(
      catchError((error) => {
        if (error.status == 401) {
          this.snackBar.showError("An authorization error occured. Try logging out and then logging in again.");
        }
        return of(null);
      })
    );
  }

  protected abstract updateExperimentTemplates(): Observable<ExperimentTemplate[]>;

  protected abstract getExperimentTemplatesCount(): Observable<number>
}